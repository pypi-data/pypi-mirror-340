# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
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
import time
import logging
import sys
import traceback
from datetime import datetime, timedelta, date
from collections import OrderedDict


def sys_exception_handler(type, value, tb):
  for line in traceback.TracebackException(type, value, tb).format(chain=True):
    print(line)
    logging.error(line)
  print(value)
  logging.error(value)


sys.excepthook = sys_exception_handler


class Logger():

  @staticmethod
  def pid():
    return '{}'.format(datetime.strftime(datetime.now(), '%y%m%d%H%M%S'))

  def __init__(self):
    self._initialized = False
    self._start_timer = time.time()
    self._logger = None
    self._records = {}

  def counter(self, key):
    if key not in self._records:
      self._records[key] = 0
    self._records[key] += 1
    return self._records[key]

  @property
  def logger(self):
    if self._logger is None:
      if not os.path.exists('_outputs'):
        os.makedirs('_outputs', exist_ok=True)
      temp = '_outputs/ebench.{}.log'.format(datetime.strftime(datetime.now(), '%y%m%d%H%M%S'))
      self.init(temp, './')
      self.warn(f'Initialize a default logger <{temp}>.')
    return self._logger

  def is_init(self):
    return self._initialized

  def init(self, name, output_dir, stdout=True):
    if not os.path.exists(output_dir):
      os.makedirs(output_dir, exist_ok=True)
    logging.root.handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG, filename=os.path.join(output_dir, name))
    self._logger = logging.getLogger(name)
    if stdout:
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      ch.setFormatter(logging.Formatter('%(message)s'))
      self._logger.addHandler(ch)
    self._initialized = True

  def _print(self, show_type, content):
    str_date = '[' + datetime.strftime(datetime.now(), '%y.%m.%d %H:%M:%S') + '] '
    self.logger.info(str_date + show_type + ' ' + content)

  def sys(self, content):
    self._print('[SYS]', content)

  def net(self, content):
    self._print('[NET]', content)

  def train(self, content):
    self._print('[TRN]', content)

  def val(self, content):
    self._print('[VAL]', content)

  def test(self, content):
    self._print('[TST]', content)

  def warn(self, content):
    self._print('[WAN]', content)

  def info(self, content):
    self._print('[INF]', content)

  def cfg(self, content):
    self._print('[CFG]', content)

  def error(self, content):
    self._print('[ERR]', content)
    exit(-1)

  def server(self, content):
    self._print('[SERVER]', content)

  def client(self, content):
    self._print('[CLIENT]', content)

  def iters(self, keys, values, **kwargs):
    # iter/epoch
    if 'step' in kwargs and 'epoch' in kwargs and 'iters_per_epoch' in kwargs:
      _data = '[%d] Iter:%d/%d' % (kwargs['epoch'], kwargs['step'] %
                                   kwargs['iters_per_epoch'], kwargs['iters_per_epoch'])
    else:
      _data = []
      if 'epoch' in kwargs:
        _data.append('Epoch:%d' % kwargs['epoch'])
      if 'step' in kwargs:
        _data.append('Iter:%d' % kwargs['step'])
      _data = ', '.join(_data)

    # other info
    commits = {}
    for i, key in enumerate(keys):
      if isinstance(values[i], (int, str)):
        value = values[i]
        _data += ', {:}:{:}'.format(key, value)
      elif key == 'lr':
        value = round(float(values[i]), 6)
        _data += ', {:}:{:}'.format(key, value)
      elif isinstance(values[i], (list, tuple)):
        value = str([round(float(v), 4) for v in values[i]])
        _data += ', {:}:{}'.format(key, value)
      else:
        value = round(float(values[i]), 4)
        _data += ', {:}:{:.4f}'.format(key, value)

    return _data

  def tic(self):
    self._start_timer = time.time()

  def toc(self):
    return (time.time() - self._start_timer) * 1000

  def tick(self):
    return time.time()

  def duration(self, start_time, end_time):
    return (end_time - start_time) * 1000


log = Logger()
log.init('ebench', '_outputs', stdout=True)


class timer():

  def __init__(self, unit='ms'):
    self.unit = unit
    self.coeff = {'ms': 1000, 's': 1}[self.unit]
    self.ticks = OrderedDict({'start': time.time() * self.coeff})

  def tic(self, name):
    self.ticks[name] = time.time() * self.coeff

  def __str__(self):
    # count each time and total time
    s = []
    ticks = list(self.ticks.values())
    for i, key in enumerate(self.ticks):
      if i == 0:
        continue
      dur = (ticks[i] - ticks[i - 1])
      s.append(f'{key}: {dur:.2f}{self.unit}')
    s.append(f'total: {(ticks[-1] - ticks[0]):.2f}{self.unit}')
    return ', '.join(s)

  def total(self):
    # total time for last tick to start
    return (list(self.ticks.values())[-1] - self.ticks['start'])

  def __getitem__(self, key):
    return self.ticks[key]


class dates():

  def __init__(self):
    self._dates = self.generate_past_dates(n=30)
    self._today = date.today()

  def generate_past_dates(self, n, date_format="%Y-%m-%d"):
    today = date.today()
    return [(today - timedelta(days=i)).strftime(date_format) for i in range(n + 1)]

  def __len__(self):
    return len(self._dates)

  def __call__(self, end=0):
    if self._today != date.today():
      self._dates = self.generate_past_dates(n=30)
      self._today = date.today()
    try:
      return self._dates[:end + 1]
    except Exception as e:
      return None


dates = dates()
