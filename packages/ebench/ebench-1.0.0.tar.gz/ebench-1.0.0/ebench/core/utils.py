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
import math
import numpy as np
import falcon


def bgr_to_yuv709v(B, G, R, h, w):
  Y = np.zeros((h, w), dtype=np.uint8)
  U = np.zeros((h // 2, w // 2), dtype=np.uint8)
  V = np.zeros((h // 2, w // 2), dtype=np.uint8)
  falcon.colorspace_rgb_to_yuv420_bt709v_u8(R, G, B, w, h, w, w, w, Y, U, V, w, w // 2, w // 2)
  return Y, U, V


def yuv709v_to_bgr(Y, U, V, h, w):
  R = np.zeros((h, w), dtype=np.uint8)
  G = np.zeros((h, w), dtype=np.uint8)
  B = np.zeros((h, w), dtype=np.uint8)
  falcon.colorspace_yuv420_bt709v_to_rgb_u8(Y, U, V, w, h, w, w // 2, w // 2, R, G, B, w, w, w)
  return B, G, R


def pad_to_size_divisible(inputs: np.ndarray, size_divisible, **kwargs) -> np.ndarray:
  shape = list(inputs.shape)
  shape[0] = int(math.ceil(shape[0] / size_divisible) * size_divisible)
  shape[1] = int(math.ceil(shape[1] / size_divisible) * size_divisible)
  outputs = np.zeros(shape).astype(inputs.dtype)
  outputs[:inputs.shape[0], :inputs.shape[1]] = inputs
  return outputs


def valid_mean(values, min_v=None, max_v=None):
  if min_v is not None:
    values = [v for v in values if v >= min_v]
  if max_v is not None:
    values = [v for v in values if v <= max_v]
  return np.mean(values) if len(values) > 0 else -1
