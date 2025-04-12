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
import os
import shutil
import cv2
import tqdm
import json
import multiprocessing

import tqdm.contrib
import tqdm.contrib.concurrent

from ebench.core import media
from ebench.core import metric
from ebench.core import model
from ebench.core.logger import log


class Dataset():

  def __init__(self, name, root='/data4/ebench/benchmarks', **kwargs):
    super().__init__()
    self._name = name
    self._root = root
    self._resource = os.path.join(root, name)
    self._protocal = os.path.join(root, name + '.txt')
    self._files = []
    self._named_files = {}

  #!<------------------------------------------------------------------
  #!< CONSTANT
  #!<------------------------------------------------------------------

  @property
  def name(self):
    return self._name

  @property
  def root(self):
    return self._root

  @property
  def resource(self):
    if not os.path.exists(self._resource):
      os.makedirs(self._resource, exist_ok=True)
    return self._resource

  @property
  def protocal(self):
    if not os.path.exists(self._protocal):
      with open(self._protocal, 'w') as f:
        f.write('')
    return self._protocal

  @property
  def files(self):
    if len(self._files) == 0:
      self._load()
    return self._files

  @property
  def named_files(self):
    if len(self._files) == 0:
      self._load()
    return self._named_files

  def __len__(self):
    return len(self.files)

  def __getitem__(self, index_or_name):
    if isinstance(index_or_name, str):
      if index_or_name in self.named_files:
        return self.named_files[index_or_name]
      else:
        return None
    else:
      index = index_or_name
      if index < 0 or index >= len(self.files):
        raise IndexError("Index out of range")
      return self.files[index]

  #!<------------------------------------------------------------------
  #!< LOAD PRE-DEFINED DATASET
  #!<------------------------------------------------------------------

  def _load(self):
    imgs, vids = media.collect(self.protocal, salience=True)
    for path in imgs + vids:
      if os.path.isfile(path) and os.path.isfile(path + '.json'):
        pair = (path, path + '.json')
      elif os.path.isfile(path):
        pair = (path, None)
      else:
        continue
      self._files.append(pair)
      self._named_files[os.path.basename(path)] = pair

  #!<------------------------------------------------------------------
  #!< CREATE DATASET
  #!<------------------------------------------------------------------

  def create_file(self, src):
    if media.is_image(src):
      dst = os.path.join(self.resource, os.path.basename(src))
      shutil.copy2(src, dst)
      return [dst, ]
    elif media.is_video(src):
      dst_vid = os.path.join(self.resource, os.path.basename(src))
      shutil.copy2(src, dst_vid)
      try:
        dst_img = os.path.splitext(dst_vid)[0] + '.png'
        cv2.imwrite(dst_img, media.FFmpegAsyncFirstFrameReader(dst_vid).frames[0])
      except Exception as e:
        log.warn(f"Error processing video {src}: {e}")
      return [dst_img, dst_vid]

  def create_from_folder(self, src):
    """从外部数据集中创建一个新的 dataset
    """
    imgs, vids = media.collect(src, salience=True)
    results = tqdm.contrib.concurrent.process_map(self.create_file, imgs + vids, max_workers=16)
    with open(self.protocal, 'w') as f:
      for files in results:
        for file in files:
          f.write(f'{file}\n')

  def create_from_enhance(self, name, enhance):
    """从现有的数据集中使用增强算法生成一个新的 dataset
    """
    db = Dataset(name=name, root=self.root)
    enhancer = model.LIST[enhance]()

    with open(db.protocal, 'w') as fw:
      for fname, (src_path, _) in tqdm.tqdm(self.named_files.items()):
        dst_path = os.path.join(db.resource, fname)
        try:
          enhancer(src_path, dst_path)
          fw.write(f'{dst_path}\n')
        except Exception as e:
          log.error(f'[ENHANCE] Error enhancing {fname}: {e}')

  #!<------------------------------------------------------------------
  #!< VIEW DATASET
  #!<------------------------------------------------------------------

  def view(self):
    img_count, vid_count, meta_count = 0, 0, 0
    for filepath, metapath in self.files:
      if media.is_image(filepath):
        img_count += 1
      elif media.is_video(filepath):
        vid_count += 1
      if metapath is not None:
        meta_count += 1
    log.info(f'[VIEW] dataset:{self.resource}, imgs:{img_count}, vids:{vid_count}, metas:{meta_count}')

  #!<------------------------------------------------------------------
  #!< ADD META INFO
  #!<------------------------------------------------------------------

  def tag(self, evaluators):
    evaluators: metric.Metric = [metric.Meta()] + [metric.LIST[name]() for name in evaluators]
    for i, file in enumerate(tqdm.tqdm(self.files)):
      filepath, metapath = file
      if metapath is not None:
        metas = json.load(open(metapath, 'r'))
      else:
        metapath = filepath + '.json'
        metas = {}
      for evaluator in evaluators:
        try:
          results = evaluator(filepath)
          metas[evaluator.name()] = results
        except Exception as e:
          log.error(f'[TAG] Error evaluating {evaluator.name} on {filepath}: {e}')
      with open(metapath, 'w') as f:
        json.dump(metas, f)
      self.files[i] = (filepath, metapath)
