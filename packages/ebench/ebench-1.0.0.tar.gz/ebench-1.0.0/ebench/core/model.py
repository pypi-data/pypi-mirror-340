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
"""Model 是 EBench 中用于视频增强的模块，返回增强后的模型路径

  Args:
    src (str): image or video path
    dst (str): output path

  Returns:
    None

"""
import math
import os
import glob
import cv2
import numpy as np
import tqdm

import thea

from ebench.core import utils
from ebench.core import media
from ebench.core.logger import log


class Model():

  def __init__(self, name):
    self.name = name

  def __call__(self, src, dst):
    """model should load src img/video and save result to dst
    """
    raise NotImplementedError(f"[MODEL] {self.name} not implemented")

  def forward(self, frame, colorspace, **kwargs):
    raise NotImplementedError(f"[MODEL] {self.name} not implemented")


class TheaModel(Model):

  def __init__(self, name):
    super().__init__(name=name)

  def inference(self, y, u, v):
    raise NotImplementedError(f"[MODEL] {self.name} not implemented")

  def forward(self, frame, height, width, pix_fmt='bgr24', colorspace='bt709'):
    """require all inputs should be BGR24 format.
    """
    if pix_fmt == 'bgr24':
      img_h, img_w = frame.shape[:2]
      x = utils.pad_to_size_divisible(frame, 32)
      h, w = x.shape[:2]

      # bgr24 to yuv420p
      b, g, r = cv2.split(x)
      if colorspace == 'bt709':
        y, u, v = utils.bgr_to_yuv709v(b, g, r, h, w)
      elif colorspace == 'bt601':
        y, u, v = utils.bgr_to_yuv601v(b, g, r, h, w)

      y, u, v = self.inference(y, u, v)

      if colorspace == 'bt709':
        b, g, r = utils.yuv709v_to_bgr(y, u, v, h, w)
      elif colorspace == 'bt601':
        b, g, r = utils.yuv601v_to_bgr(y, u, v, h, w)

      out = cv2.merge([b, g, r])[:img_h, :img_w]
      return out

    elif pix_fmt == 'yuv420p':
      y = frame[:height * width].reshape(height, width)
      u = frame[height * width: height * width + height * width // 4].reshape(height // 2, width // 2)
      v = frame[height * width + height * width // 4: height * width + height * width // 4 + height * width // 4].reshape(height // 2, width // 2)  # nopep8
      y, u, v = self.inference(y, u, v)
      yuv = np.concatenate([y.flatten(), u.flatten(), v.flatten()])
      return yuv

  def __call__(self, src, dst):
    """Thea default to use yuv420p format
    """
    if media.is_image(src):
      frame = cv2.imread(src)
      h, w = frame.shape[:2]
      aug = self.forward(frame, height=h, width=w, pix_fmt='bgr24', colorspace='bt709')
      cv2.imwrite(dst, aug)

    elif media.is_video(src):
      reader = media.FFmpegAsyncReader(src, pix_fmt='yuv420p')
      with media.FFmpegAsyncWriter(dst,
                                   fps=reader.fps,
                                   crf=16,
                                   height=reader.height,
                                   width=reader.width,
                                   color_range=reader.color_range,
                                   color_space=reader.color_space,
                                   pix_fmt='yuv420p') as writer:
        for frame in tqdm.tqdm(reader):
          out = self.forward(
              frame,
              height=reader.height,
              width=reader.width,
              pix_fmt='yuv420p',
              colorspace=reader.color_space)
          writer.write(out)
        writer.close()


class vls_v3(TheaModel):

  def __init__(self):
    super().__init__(name='vls_v3')
    # build instance
    root = os.getenv("THEA_ROOT")
    if not os.path.exists(root):
      raise ValueError(f"THEA_ROOT:{root} is not set.")
    config = glob.glob(f'{root}/config/*-all.meta')[0]
    log.info(config)
    self.instance = thea.create(config, thea.THEA_LOG_INFO, "./", 1, f"{root}/models", False, 1)

    # build graph
    self.graph = thea.create_graph(self.instance, thea.THEA_GPU_0)
    # create node
    self.inp = thea.create_op(self.graph, thea.THEA_OP_INPUT, thea.THEA_POWER_FULL, thea.THEA_INFER_FP32)  # nopep8
    self.vod = thea.create_op(self.graph, thea.THEA_OP_VIDEO_OBJECT_DETECT_V2_VINO, thea.THEA_POWER_FULL, thea.THEA_INFER_FP32)  # nopep8
    self.vls = thea.create_op(self.graph, thea.THEA_OP_VIDEO_LUMINANCE_SHARPEN_V3_CPU, thea.THEA_POWER_FULL, thea.THEA_INFER_FP32)  # nopep8
    # bind graph
    thea.bind_op(self.graph, self.vod, 0, self.inp)
    thea.bind_op(self.graph, self.vls, 0, self.inp)
    thea.bind_op(self.graph, self.vls, 1, self.vod)
    # freeze
    thea.freeze_graph(self.graph)

  def inference(self, y, u, v):
    thea.flush_graph(self.graph)
    ret_y = np.zeros_like(y)
    ret_u = np.zeros_like(u)
    ret_v = np.zeros_like(v)
    thea.set_op_input(self.graph, self.inp, [y, u, v], thea.THEA_BT_709_LIMITED)
    thea.inference_graph(self.graph)
    thea.get_op_output(self.graph, self.vls, [ret_y, ret_u, ret_v], thea.THEA_BT_709_LIMITED)
    return ret_y, ret_u, ret_v


LIST = {
    'vls_v3': vls_v3,
}
