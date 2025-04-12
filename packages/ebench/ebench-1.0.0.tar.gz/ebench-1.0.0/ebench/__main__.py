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
"""command script
"""
import shutil
import os
import argparse
import cv2
import tqdm
import json

from ebench.core import dataset
from ebench.core import metric
from ebench.core.logger import log

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='EBench - A Benchmark for Evaluating Visual Saliency Models')
  parser.add_argument('-t', '--task', type=str, default=None, required=True)
  parser.add_argument('-f', '--path', type=str, default=None, help='image/video/csv path.')
  parser.add_argument('-n', '--names', type=str, nargs='+', default=None, help='dataset names.')
  parser.add_argument('-d', '--dst', type=str, default=None, help='output dataset name.')
  parser.add_argument('-e', '--evaluators', type=str, nargs='+', default=None, help='evaluator names.')
  parser.add_argument('-m', '--model', type=str, default=None, help='model name.')

  parser.add_argument('--row', type=str, default=None, help='row name for pivot.')
  parser.add_argument('--row-interval', type=int, default=1, help='row interval for pivot.')
  parser.add_argument('--cols', type=str, nargs='+', default=None, help='column names for pivot.')

  parser.add_argument('--root', type=str, default='/data4/ebench/benchmarks', help='root path for datasets.')
  args = parser.parse_args()

  log.info(f"args: {args}")

  if args.task == 'prepare':
    # python -m ebench -t prepare -f /cephFS/yangying/VSR2024/assets/faceratio_bigolive_videos -d face0409
    db = dataset.Dataset(name=args.dst, root=args.root)
    db.create_from_folder(src=args.path)

  elif args.task == 'view':
    # python -m ebench -t view -n face0409
    db = dataset.Dataset(name=args.names[0], root=args.root)
    db.view()

  elif args.task == 'tag':
    # python -m ebench -t tag -n face0409 -e vqa_v4_4
    # python -m ebench -t tag -n face0409_vls_v2 -e vqa_v4_4
    db = dataset.Dataset(name=args.names[0], root=args.root)
    db.tag(evaluators=args.evaluators)

  elif args.task == 'enhance':
    # python -m ebench -t enhance -m vls_v3 -n face0409 -d face0409_vls_v2
    db = dataset.Dataset(name=args.names[0], root=args.root)
    db.create_from_enhance(name=args.dst, enhance=args.model)

  elif args.task == 'pivot':
    # python -m ebench -t pivot -n face0409 face0409_vls_v2 --row vqa_v4_4.y --cols vqa_v4_4.tech vqa_v4_4.tech_fg vqa_v4_4.tech_face
    # python -m ebench -t pivot -n face0409 face0409_vls_v2 --row vqa_v4_4.y
    # --cols vqa_v4_4.noise vqa_v4_4.noise_fg vqa_v4_4.noise_face
    # --row-interval 20
    cmp = metric.Comparator(names=args.names, root=args.root)
    cmp.pivot(row=args.row,
              cols=args.cols,
              row_interval=args.row_interval)
