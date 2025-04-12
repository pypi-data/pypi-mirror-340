# Copyright 2025 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Metric 是 EBench 中用于评估视频质量的模块, 所有模型具备标准化的输入输出

  Args:
    src (str): image or video path

  Returns:
    dict: metric results. e.g. {'height': 1080, 'width':1920}

  Order:
    __call__(src) -> forward(frames, height, width, pix_fmt)

"""
import os
import glob
import cv2
import json
import numpy as np
from collections import OrderedDict

import thea

from ebench.core import utils
from ebench.core import media
from ebench.core.logger import log
from ebench.core import dataset


class Metric():

  def __init__(self, name):
    self._name = name

  def name(self):
    return self._name

  def forward(self, frames, height, width, pix_fmt):
    raise NotImplementedError(f"[METRIC] {self._name} not implemented")

  def __call__(self, src):
    if media.is_image(src):
      frame = cv2.imread(src)
      h, w = frame.shape[:2]
      return self.forward([frame,], height=h, width=w, pix_fmt='bgr24')

    elif media.is_video(src):
      vid = media.FFmpegAsyncReader(src, pix_fmt='yuv420p')
      h, w = vid.height, vid.width
      return self.forward(vid.frames, height=h, width=w, pix_fmt='yuv420p')


class Meta(Metric):

  def __init__(self):
    super().__init__(name='meta')

  def __call__(self, src):
    if media.is_image(src):
      frame = cv2.imread(src)
      h, w = frame.shape[:2]
      return {
          'filepath': src,
          'height': h,
          'width': w
      }

    elif media.is_video(src):
      vid = media.FFmpegAsyncReader(src, pix_fmt='yuv420p')
      h, w = vid.height, vid.width
      return {
          'filepath': src,
          'height': vid.height,
          'width': vid.width,
          'fps': vid.fps,
          'count': vid.count,
          'pix_fmt': vid.pix_fmt,
          'color_range': vid.color_range,
          'color_space': vid.color_space,
          'bitrate': vid.bitrate,
      }


class BigoQS(Metric):

  def __init__(self):
    super().__init__(name='vqa_v4_4')
    root = os.getenv("THEA_ROOT")
    if not os.path.exists(root):
      raise ValueError(f"THEA_ROOT:{root} is not set.")
    config = glob.glob(f'{root}/config/*-all.meta')[0]
    log.info(config)

    # build instance
    self.instance = thea.create(config, thea.THEA_LOG_INFO, "./", 1, f"{root}/models", False, 1)
    self.graph = thea.create_graph(self.instance, thea.THEA_GPU_0)
    self.inp = thea.create_op(self.graph, thea.THEA_OP_INPUT, thea.THEA_POWER_FULL, thea.THEA_INFER_FP32)  # nopep8
    self.vhm = thea.create_op(self.graph, thea.THEA_OP_VIDEO_HUMAN_MATTING_V5_LITE_VINO, thea.THEA_POWER_FULL, thea.THEA_INFER_FP32)  # nopep8
    self.vqa = thea.create_op(self.graph, thea.THEA_OP_VIDEO_QUALITY_ASSESS_V4_SPATIAL_EQM_VINO, thea.THEA_POWER_FULL, thea.THEA_INFER_FP32)  # nopep8
    self.vod = thea.create_op(self.graph, thea.THEA_OP_VIDEO_OBJECT_DETECT_V2_VINO, thea.THEA_POWER_FULL, thea.THEA_INFER_FP32)  # nopep8
    thea.bind_op(self.graph, self.vhm, 0, self.inp)
    thea.bind_op(self.graph, self.vod, 0, self.inp)
    thea.bind_op(self.graph, self.vqa, 0, self.inp)
    thea.bind_op(self.graph, self.vqa, 1, self.inp)
    thea.bind_op(self.graph, self.vqa, 2, self.vhm)
    thea.bind_op(self.graph, self.vqa, 3, self.vod)

    mode = np.array(1, dtype=np.int32)
    thea.set_op_attr(self.graph, self.vod, "ALIGN_MODE", mode)
    thea.freeze_graph(self.graph)

  def forward(self, frames, height, width, pix_fmt='bgr24'):
    assert pix_fmt in ['bgr24', 'rgb24', 'yuv420p'], f'pix_fmt {pix_fmt} not supported'
    labels = ['vqa', 'aes', 'tech', 'roi', 'aes_fg', 'aes_face', 'tech_fg', 'tech_face', 'sharp', 'sharp_fg', 'color_face',
              'color_skin', 'color_tone_fg', 'noise', 'noise_bg', 'noise_fg', 'noise_face', 'noise_hair', 'y_face', 'y_fg',
              'y_skin', 'y_hair', 'y_std_hair', 'y', 'y_min_ratio', 'y_max_ratio', 'ent_y', 'oe_prop_fg', 'oe_fg',
              'oe_prop_skin', 'oe_skin', 'oe_prop_face', 'oe_face', 'oe_prop_hair', 'oe_hair', 'fgr_ratio', 'face_ratio',
              'human_pos', 'goden_fgr', 'block', 'block_bg', 'block_fg', 'block_face', 'block_hair', 'blur', 'blur_bg',
              'blur_fg', 'blur_face', 'blur_hair', 'cont_amee', 'cont_eme', 'cont_conl', 'color_hue_fg', 'color_sat_fg',
              'color_face_a', 'color_face_b', 'color_skin_a', 'color_skin_b', 'color_hair_a', 'color_hair_b', 'env_edge_complx',
              'env_hair_sim', 'env_dpt']
    results = {k: [] for k in labels}

    for frame in frames:
      if pix_fmt == 'bgr24':
        b, g, r = cv2.split(frame)
        y, u, v = utils.bgr_to_yuv709v(b, g, r, height, width)
      elif pix_fmt == 'rgb24':
        r, g, b = cv2.split(frame)
        y, u, v = utils.bgr_to_yuv709v(b, g, r, height, width)
      elif pix_fmt == 'yuv420p':
        y = frame[:height * width].reshape(height, width)
        u = frame[height * width: height * width + height * width // 4].reshape(height // 2, width // 2)
        v = frame[height * width + height * width // 4: height * width + height * width // 4 + height * width // 4].reshape(height // 2, width // 2)  # nopep8
      else:
        raise ValueError(f'pix_fmt {pix_fmt} not supported')

      thea.flush_graph(self.graph)
      thea.set_op_input(self.graph, self.inp, [y, u, v], thea.THEA_BT_709_LIMITED)
      thea.inference_graph(self.graph)
      outs = np.zeros([1, 1, 1, 63], dtype=np.float32)
      thea.get_op_output(self.graph, self.vqa, [outs, ], thea.THEA_COLOR_NONE)
      outs = outs.reshape(-1).tolist()
      for i, label in enumerate(labels):
        results[label].append(outs[i])

    return results


LIST = {
    'vqa_v4_4': BigoQS,
    'meta': Meta,
}


class Comparator():

  def __init__(self, names, root, **kwargs):
    super().__init__()
    self.datasets = [dataset.Dataset(name=name, root=root) for name in names]
    self.matches = {}  # filename: [(img_path1, meta_path1), (img_path2, meta_path2)]
    # matched files
    for name in self.datasets[0].named_files:
      exist = True
      for i in range(1, len(self.datasets)):
        pair = self.datasets[i][name]
        if pair is None or len(pair) != 2 or pair[1] is None:
          exist = False
          break
      if exist:
        self.matches[name] = []
        for i in range(len(self.datasets)):
          self.matches[name].append(json.load(open(self.datasets[i][name][1])))
    log.info(f"[COMPARE] matched files: {len(self.matches)} vs baseline: {len(self.datasets[0].named_files)}")

  def pivot(self, row, cols, **kwargs):
    """Pivot table for dataset
    """
    row_interval = kwargs.get('row_interval', 1)
    full_file_path = f'_outputs/{log.pid()}.full.csv'
    pivot_file_path = f'_outputs/{log.pid()}.pivot.csv'

    row_evals = row.split('.')
    row_eval, row_eval_index = row_evals
    col_evals = [col.split('.') for col in cols]
    log.info(f"[PIVOT] using row index: {row_evals}")
    log.info(f"[PIVOT] using col index: {col_evals}")

    # (meta_path, row_value, col1.db1, col1.db2, col1.db3, col1.db3 - col1.db1, col1.db3 - col1.db2, ...)
    targets = []
    for name, metas in self.matches.items():
      target = [metas[0]['meta']['filepath'], ]
      row_value = utils.valid_mean(metas[0][row_eval][row_eval_index], min_v=0.0)
      target.append(row_value)
      for col_eval, col_eval_index in col_evals:
        col_values = []
        # default values
        for meta in metas:
          col_values.append(utils.valid_mean(meta[col_eval][col_eval_index], min_v=0.0))
        # diff between the last dataset and the other dataset
        target.extend(col_values)
        for col_val in col_values[:-1]:
          if col_values[-1] == -1:
            target.append(-1)
          else:
            target.append(col_values[-1] - col_val)
      targets.append(target)

    # csv-out
    with open(full_file_path, 'w') as f:
      full_title = ['filepath', row_eval_index, ]
      for col_eval, col_eval_index in col_evals:
        col_titles = []
        for i in range(len(self.datasets)):
          col_titles.append(f'{col_eval_index}@{self.datasets[i].name}')
        for i in range(len(self.datasets) - 1):
          col_titles.append(f'{col_eval_index}@{self.datasets[-1].name}-{self.datasets[i].name}')
        full_title.extend(col_titles)
      f.write(','.join(full_title) + '\n')
      for target in targets:
        f.write(','.join([str(col) for col in target]) + '\n')
      log.info(f"[PIVOT] export full file: {os.path.abspath(full_file_path)}")

    # aggregate by row interval
    targets = sorted(targets, key=lambda x: x[1], reverse=False)
    aggregated = OrderedDict()
    for target in targets:
      ind = target[1] // row_interval
      if ind not in aggregated:
        aggregated[ind] = []
      aggregated[ind].append(target[1:])

    # csv-out
    with open(pivot_file_path, 'w') as f:
      pivot_title = ['start', 'end', 'count', f'{row_eval_index}_mean'] + full_title[2:]
      f.write(','.join(pivot_title) + '\n')
      for ind in aggregated:
        aggregated[ind] = [
            ind *
            row_interval,
            (ind +
             1) *
            row_interval,
            len(
                aggregated[ind]),
            *
            np.mean(
                aggregated[ind],
                axis=0).tolist()]
        f.write(','.join([str(col) for col in aggregated[ind]]) + '\n')
      log.info(f"[PIVOT] export pivot file: {os.path.abspath(pivot_file_path)}")
