# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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
"""Media Pipeline
"""
import os
import glob
import tqdm
import functools
import subprocess

import cv2
import numpy as np
import ffmpeg


IMAGE_EXT = ['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'bmp', 'BMP', 'tif']
VIDEO_EXT = ['mp4', 'avi', 'qt', 'mov', '265', '264', 'yuv']
YUV_EXT = ['yuv', 'bin']
RAW_EXT = ['cr2', 'CR2', 'nef', 'NEF', 'arw', 'ARW']
POINTCLOUD_EXT = ['ply', 'PLY']

if os.path.isfile('/usr/bin/ffmpeg'):
  FFMPEG_PATH = '/usr/bin/ffmpeg'
elif os.path.isfile('/usr/local/bin/ffmpeg'):
  FFMPEG_PATH = '/usr/local/bin/ffmpeg'
else:
  FFMPEG_PATH = None

#!<-----------------------------------------------------------------------------
#!< BASIC
#!<-----------------------------------------------------------------------------


def is_image(filepath, **kwargs):
  for ext in IMAGE_EXT:
    if filepath.lower().endswith(ext):
      return True
  return False


def is_video(filepath, **kwargs):
  for ext in VIDEO_EXT:
    if filepath.lower().endswith(ext):
      return True
  return False


def collect(path: str, salience=False, **kwargs):
  """Collect all images/videos:
    1. from .txt file
    2. traverse all folder

  Args:
    path: a txt filepath or a folder path

  Returns:
    list (image_files, video_files)
  """
  image_files = []
  video_files = []

  if not os.path.exists(path):
    raise FileNotFoundError(path)

  if path.endswith('.txt') and os.path.isfile(path):
    with open(path, 'r') as fp:
      lines = fp.readlines()
      lines = [line.strip().split(',')[0] for line in lines]
    for lq in lines:
      if not os.path.exists(lq):
        log.warn(f'File {lq} not exists.')
        continue
      if is_image(lq):
        image_files.append(lq)
      elif is_video(lq):
        video_files.append(lq)

  elif os.path.isfile(path):
    if is_image(path):
      image_files.append(path)
    elif is_video(path):
      video_files.append(path)

  elif os.path.isdir(path):
    for root, _, fnames in os.walk(path):
      for name in fnames:
        filepath = os.path.join(root, name)
        if is_video(filepath):
          video_files.append(filepath)
        elif is_image(filepath):
          image_files.append(filepath)

  else:
    raise "Unknown input path attribution %s." % path

  if not salience:
    log.info('Total loading %d image.' % len(image_files))
    log.info('Total loading %d video.' % len(video_files))

  return image_files, video_files

#!<-----------------------------------------------------------------------------
#!< Yuv Reader/Writer
#!<-----------------------------------------------------------------------------


class YuvReader():
  def __init__(self, path: str, height: int, width: int, separate=False):
    assert os.path.exists(path)
    self.size = height * width + height * width // 2
    self.handle = open(path, 'rb')
    self.count = os.path.getsize(path) // self.size

    assert height > 0 and height % 2 == 0
    assert width > 0 and width % 2 == 0
    self.height = height
    self.width = width
    self.separate = separate

    # preload first
    h, w = height, width
    s = width * height
    uPlanePos = s
    vPlanePos = s + (width // 2) * (height // 2)

    self.frames = []
    for i in range(self.count):
      arr = np.array([i for i in self.handle.read(self.size)]).astype('uint8')
      y = arr[:uPlanePos]
      u = arr[uPlanePos: vPlanePos]
      v = arr[vPlanePos:]
      y = np.reshape(y, [h, w])
      u = u.reshape(h // 2, w // 2)
      v = v.reshape(h // 2, w // 2)
      if self.separate:
        self.frames.append([y, u, v])
      else:
        u = cv2.resize(u, dsize=(w, h))
        v = cv2.resize(v, dsize=(w, h))
        yuv = np.stack([y, u, v], axis=2)
        self.frames.append(yuv)

  def __len__(self):
    return len(self.frames)

  def __getitem__(self, idx):
    return self.frames[idx]

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.handle.close()


class YuvWriter():
  def __init__(self, path: str, height: int, width: int):
    assert height > 0 and height % 2 == 0
    assert width > 0 and width % 2 == 0
    self.height = height
    self.width = width
    self.handle = open(path, 'wb')

  def __len__(self):
    return len(self.frames)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.handle.close()

  def write(self, y: np.ndarray, u: np.ndarray, v: np.ndarray):
    assert y.shape[0] == self.height and y.shape[1] == self.width
    assert u.shape[0] == self.height // 2 and u.shape[1] == self.width // 2
    assert v.shape[0] == self.height // 2 and v.shape[1] == self.width // 2

    self.handle.write(y.astype('uint8').tobytes())
    self.handle.write(u.astype('uint8').tobytes())
    self.handle.write(v.astype('uint8').tobytes())

#!<-----------------------------------------------------------------------------
#!< OpenCV Reader/Writer: Possibly with color difference
#!<-----------------------------------------------------------------------------


class VideoReader():

  def __init__(self, path: str, to_rgb=False, to_tensor=False):
    self.cap = cv2.VideoCapture(path)
    self.frame = None
    self.to_rgb = to_rgb
    self.to_tensor = to_tensor

    if not self.cap.isOpened():
      log.warn('Failed to open {}'.format(path))
      self.valid = False
      self.fps = -1
      self.width = -1
      self.height = -1
      self.count = 0

    else:
      self.valid = True
      self.fps = self.cap.get(cv2.CAP_PROP_FPS)
      self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
      self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
      self.count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

  def __len__(self):
    return int(self.count)

  def __getitem__(self, idx):
    # return a clip
    if isinstance(idx, slice):
      return [self[i] for i in range(*idx.indices(len(self)))]

    if self.cap.get(cv2.CAP_PROP_POS_FRAMES) != idx:
      self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)

    ret, img = self.cap.read()
    if not ret:
      raise IndexError

    if self.to_rgb:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if self.to_tensor:
      img = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0

    return img

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.cap.release()


class VideoWriter():

  def __init__(self, path: str, width: int, height: int, fps: float):
    self.cap = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width), int(height)))

  def write_tensor(self, tensor, is_rgb=True):
    r"""Assume tensor is [0~1] [N, C, H, W] float32 format.
    """
    frames = tensor.mul(255).byte().cpu().permute(0, 2, 3, 1).numpy()
    for i in range(frames.shape[0]):
      if is_rgb:
        self.cap.write(cv2.cvtColor(frames[i], cv2.COLOR_RGB2BGR))
      else:
        self.cap.write(frames[i])

  def write(self, array: np.array):
    if array.ndim == 3:
      self.cap.write(array)
    elif array.ndim == 4:
      for i in range(array.shape[0]):
        self.cap.write(array[i])

  def close(self):
    self.cap.release()

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.close()

#!<-----------------------------------------------------------------------------
#!< Folder Reader/Writer
#!<-----------------------------------------------------------------------------


class FolderReader():
  """Loading images from folder
  """

  def __init__(self, path: str, ext='.png', to_rgb=False, to_tensor=False):
    self.files = sorted(glob.glob(f'{path}/*{ext}'))
    self.count = len(self.files)
    self.to_rgb = to_rgb
    self.to_tensor = to_tensor

  def __getitem__(self, idx):
    # return a clip
    if isinstance(idx, slice):
      return [self[i] for i in range(*idx.indices(len(self)))]
    img = cv2.imread(self.files[idx])
    if self.to_rgb:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if self.to_tensor:
      img = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
    return img


class FolderWriter():
  """Writing images to folder
  """

  def __init__(self, path: str):
    self.count = 0
    self.dst = path
    if not os.path.exists(self.dst):
      os.system(f'mkdir -p {self.dst}')

  def write(self, array: np.array):
    if array.ndim == 3:
      self.count += 1
      cv2.imwrite('{}/{:08d}.png'.format(self.dst, self.count), array)
    elif array.ndim == 4:
      for i in range(array.shape[0]):
        self.count += 1
        cv2.imwrite('{}/{:08d}.png'.format(self.dst, self.count), array[i])


#!<-----------------------------------------------------------------------------
#!< FFmpeg Reader/Writer
#!<-----------------------------------------------------------------------------

class FFmpegReader():
  """Becuase using OpenCV will result in color mismatch between bt601 and bt709,
    we use ffmpeg to decode the mp4 and then loading png format image.
  """

  def convert_yuv_to_bgr(self, inputs, color_space, color_range, to_rgb=False):
    """Convert yuv420 to bgr
    """
    dst = T.COLORSPACE.RGB if to_rgb else T.COLORSPACE.BGR

    if color_space == 'bt709' and color_range == 'tv':
      src = T.COLORSPACE.YUV709V
    elif color_space == 'smpte170m' and color_range == 'tv':
      src = T.COLORSPACE.YUV709V
    elif color_space == 'smpte170m' and color_range == 'pc':
      src = T.COLORSPACE.YUV709F
    elif color_space == 'bt709' and color_range == 'pc':
      src = T.COLORSPACE.YUV709F
    elif color_space == 'bt601' and color_range == 'tv':
      src = T.COLORSPACE.YUV601V
    elif color_space == 'bt601' and color_range == 'pc':
      src = T.COLORSPACE.YUV601F
    elif color_space == 'bt470bg' and color_range == 'tv':
      src = T.COLORSPACE.YUV601V
    elif color_space == 'bt470bg' and color_range == 'pc':
      src = T.COLORSPACE.YUV601F
    else:
      raise NotImplementedError(f'Unknown color_space {color_space} or color_range {color_range}')

    return T.change_colorspace(inputs, src, dst)

  def __init__(self, path: str, to_rgb=False, to_tensor=False, **kwargs):
    """Default to BGR colorspace
    """
    probe = ffmpeg.probe(path, v='error')
    stream = probe['streams'][0]
    pix_fmt = 'rgb24' if to_rgb else 'bgr24'
    self.to_tensor = to_tensor
    self.to_rgb = to_rgb
    self.path = path

    # video parameters
    self.valid = True
    avg_rate = stream.get('avg_frame_rate', 0).split('/')
    self.fps = float(avg_rate[0]) / float(avg_rate[1])
    self.width = int(stream.get('width', -1))
    self.height = int(stream.get('height', -1))
    self.count = int(stream.get('nb_frames', -1))
    self.pix_fmt = stream.get('pix_fmt', 'yuv420p')
    self.color_range = stream.get('color_range', 'tv')
    self.color_space = stream.get('color_space', 'bt709')
    self.bitrate = int(stream.get('bit_rate', -1))

    # preload all frames: automatically convert to yuv444p
    # scale=in_color_matrix=bt709:in_range=pc
    out, _ = (
        ffmpeg
        .input(path, v='error', vsync=0)
        .output('pipe:', format='rawvideo', vsync=0, pix_fmt='yuv420p')
        .run(capture_stdout=True, cmd=FFMPEG_PATH)
    )

    self.frames = np.frombuffer(out, np.uint8).reshape([-1, int(self.height * self.width * 1.5)])
    self.count = len(self.frames)

  def __str__(self):
    s = f'path: {self.path}'
    s += f', fps: {self.fps}'
    s += f', count x h x w: {self.count} x {self.height} x {self.width}'
    s += f', pix_fmt: {self.pix_fmt}'
    s += f', color_range: {self.color_range}'
    s += f', color_space: {self.color_space}'
    s += f', bitrate: {self.bitrate}'
    return s

  def __len__(self):
    return int(self.count)

  def __getitem__(self, idx):
    # return a clip
    if isinstance(idx, slice):
      return [self[i] for i in range(*idx.indices(len(self)))]

    if idx >= self.count:
      raise IndexError

    # parse frames
    frame = self.frames[idx]
    frame = T.yuv420_to_yuv444(frame, self.height, self.width, interpolation=T.RESIZE_MODE.BILINEAR)
    img = self.convert_yuv_to_bgr(frame, self.color_space, self.color_range, self.to_rgb)

    if self.to_tensor:
      img = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0

    return img

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    pass


class FFmpegWriter():

  def convert_bgr_to_yuv(self, inputs, color_space, color_range, from_rgb=False):
    """Convert yuv420 to bgr
    """
    src = T.COLORSPACE.RGB if from_rgb else T.COLORSPACE.BGR

    if color_space == 'bt709' and color_range == 'tv':
      dst = T.COLORSPACE.YUV709V
    elif color_space == 'bt709' and color_range == 'pc':
      dst = T.COLORSPACE.YUV709F
    elif color_space == 'bt601' and color_range == 'tv':
      dst = T.COLORSPACE.YUV601V
    elif color_space == 'bt601' and color_range == 'pc':
      dst = T.COLORSPACE.YUV601F
    elif color_space == 'bt470bg' and color_range == 'tv':
      dst = T.COLORSPACE.YUV601V
    elif color_space == 'bt470bg' and color_range == 'pc':
      dst = T.COLORSPACE.YUV601F
    else:
      raise NotImplementedError(f'Unknown color_space {color_space} or color_range {color_range}')

    return T.change_colorspace(inputs, src, dst)

  def __init__(self,
               path: str,
               width: int = None,
               height: int = None,
               fps: float = 30.0,
               crf=16,
               color_range='tv',
               color_space='bt709',
               pix_fmt='yuv420p'):
    """Default from BGR colorspace"""
    assert color_range in ['tv', 'pc'], f'color_range should be tv or pc, but got {color_range}'
    assert color_space in ['bt709', 'bt601', 'bt470bg'], f'color_space should be bt709 or bt601, but got {color_space}'
    assert pix_fmt in ['yuv420p', 'yuvj420p'], f'pix_fmt should be yuv420p, yuvj420p, but got {pix_fmt}'

    self.color_space = color_space
    self.color_range = color_range
    self.pix_fmt = pix_fmt
    self.width = width
    self.height = height
    self.path = path
    self.crf = crf
    self.fps = fps

    if self.width and self.height:
      self.pipeline = self.resize(height, width)
    else:
      self.pipeline = None

  def resize(self, height, width):
    s = '{}x{}'.format(width, height)
    self.height, self.width = height, width
    return (
        ffmpeg
        .input(
            'pipe:',
            format='rawvideo',
            pix_fmt='yuv420p',
            s=s,
            v='error',
            vsync=0)
        .output(
            self.path,
            crf=self.crf,
            # preset='veryslow',
            pix_fmt=self.pix_fmt,
            vcodec='libx264',
            threads='0',
            s=s,
            colorspace=self.color_space,
            color_range=self.color_range,
            framerate=self.fps,
            v='error',
            vsync=0)
        .overwrite_output()
        .run_async(pipe_stdin=True, cmd=FFMPEG_PATH, quiet=True)
    )

  def write(self, frame, from_rgb=False):
    """write BGR frame (0-255) to video file
    """
    # require input tensor should be [0 ~ 1]
    if isinstance(frame, torch.Tensor):
      if frame.ndim == 4:
        assert frame.size(0) == 1
        frame = frame[0]
      frame = frame.mul(255).round().clip(0, 255).byte().cpu().permute(1, 2, 0).numpy()

    # numpy datatype
    else:
      frame = frame.round().clip(0, 255).astype('uint8')

    # build pipeline
    if self.pipeline is None:
      h, w = T.get_inputs_hw(frame)
      self.pipeline = self.resize(height=h, width=w)

    # bgr to yuv444
    frame = self.convert_bgr_to_yuv(frame, self.color_space, self.color_range, from_rgb)

    # yuv444 to yuv420
    frame = T.yuv444_to_yuv420(frame, self.height, self.width, interpolation=T.RESIZE_MODE.BILINEAR)

    # write to ffmpeg
    self.pipeline.stdin.write(frame.tobytes())

  def __enter__(self):
    return self

  def close(self):
    if self.pipeline is not None:
      self.pipeline.stdin.close()
      self.pipeline.wait()

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.close()


#!<-----------------------------------------------------------------------------
#!< Video Sampler
#!<-----------------------------------------------------------------------------

class VideoSampler():

  def __init__(self,
               reader,
               clip_num=None,
               clip_length=None,
               clip_stride=None,
               interval=1,
               to_tensor=False,
               padding_last=False):
    super(VideoSampler, self).__init__()
    assert isinstance(reader, (VideoReader, FFmpegReader)), f'Unknown reader {type(reader)}'
    assert interval >= 1, f'interval should be greater than 1, but got {interval}'
    self.to_tensor = to_tensor

    # pre-loading all frames
    self.frames = []
    for frame in reader:
      self.frames.append(frame)
    total = len(self.frames)
    self.frames = np.stack(self.frames, axis=0)

    # split clips
    self.clip_inds = T.split_video_into_clips(
        total,
        clip_num=clip_num,
        clip_length=clip_length,
        clip_stride=clip_stride,
        interval=interval)

  def __len__(self):
    return len(self.clip_inds)

  def __getitem__(self, idx):
    if idx >= len(self.clip_inds):
      raise IndexError

    clip = np.stack(self.frames[self.clip_inds[idx]], axis=0)  # [T, H, W C]
    if self.to_tensor:
      clip = torch.from_numpy(clip).permute(0, 3, 1, 2).float() / 255.0

    return clip

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    pass


#!<-----------------------------------------------------------------------------
#!< FFmpeg Async Reader/Writer
#!<-----------------------------------------------------------------------------

class FFmpegAsyncReader():

  def __init__(self, path: str, pix_fmt='bgr24', **kwargs):
    super(FFmpegAsyncReader, self).__init__()
    probe = ffmpeg.probe(path, v='error')
    stream = probe['streams'][0]

    assert pix_fmt in ['yuv420p', 'rgb24', 'bgr24']
    self.path = path

    # video parameters
    self.valid = True
    avg_rate = stream.get('avg_frame_rate', 0).split('/')
    self.fps = float(avg_rate[0]) / float(avg_rate[1])
    self.width = int(stream.get('width', -1))
    self.height = int(stream.get('height', -1))
    self.count = int(stream.get('nb_frames', -1))
    self.pix_fmt = stream.get('pix_fmt', 'yuv420p')
    self.color_range = stream.get('color_range', 'tv')
    self.color_space = stream.get('color_space', 'bt709')
    self.bitrate = int(stream.get('bit_rate', -1))

    # load all frames at once
    if pix_fmt in ['rgb24', 'bgr24']:
      out, _ = (
          ffmpeg
          .input(path, v='quiet', vsync=0)
          .output('pipe:',
                  format='rawvideo',
                  vf=f'scale=in_color_matrix={self.color_space}:in_range={self.color_range}:out_color_matrix={self.color_space}:out_range={self.color_range}',
                  vsync=0,
                  pix_fmt=pix_fmt)
          .run(capture_stdout=True, cmd=FFMPEG_PATH))
      self.frames = np.frombuffer(out, np.uint8).reshape([-1, self.height, self.width, 3])

    elif pix_fmt in ['yuv420p', 'yuvj420p']:
      out, _ = (
          ffmpeg
          .input(path, v='quiet', vsync=0)
          .output('pipe:', format='rawvideo', vsync=0, pix_fmt=pix_fmt)
          .run(capture_stdout=True, cmd=FFMPEG_PATH))
      self.frames = np.frombuffer(out, np.uint8).reshape([-1, int(self.height * self.width * 1.5)])

    assert self.count == len(self.frames), f'frame count mismatch: {self.count} vs {len(self.frames)}'
    self.count = len(self.frames)

  def __str__(self):
    s = f'path: {self.path}'
    s += f', fps: {self.fps}'
    s += f', count x h x w: {self.count} x {self.height} x {self.width}'
    s += f', pix_fmt: {self.pix_fmt}'
    s += f', color_range: {self.color_range}'
    s += f', color_space: {self.color_space}'
    s += f', bitrate: {self.bitrate}'
    return s

  def __len__(self):
    return int(self.count)

  def __getitem__(self, idx):
    if isinstance(idx, slice):
      return [self[i] for i in range(*idx.indices(len(self)))]
    if idx >= self.count:
      raise IndexError
    frame = self.frames[idx]
    return frame

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    pass


class FFmpegAsyncFirstFrameReader():

  def __init__(self, path: str, pix_fmt='bgr24', **kwargs):
    super(FFmpegAsyncFirstFrameReader, self).__init__()
    probe = ffmpeg.probe(path, v='error')
    stream = probe['streams'][0]

    assert pix_fmt in ['yuv420p', 'rgb24', 'bgr24']
    self.path = path

    # video parameters
    self.valid = True
    avg_rate = stream.get('avg_frame_rate', 0).split('/')
    self.fps = float(avg_rate[0]) / float(avg_rate[1])
    self.width = int(stream.get('width', -1))
    self.height = int(stream.get('height', -1))
    self.count = int(stream.get('nb_frames', -1))
    self.pix_fmt = stream.get('pix_fmt', 'yuv420p')
    self.color_range = stream.get('color_range', 'tv')
    self.color_space = stream.get('color_space', 'bt709')
    self.bitrate = int(stream.get('bit_rate', -1))

    # load all frames at once
    if pix_fmt in ['rgb24', 'bgr24']:
      out, _ = (
          ffmpeg
          .input(path, v='quiet', vsync=0)
          .output('pipe:',
                  format='rawvideo',
                  vf=f'scale=in_color_matrix={self.color_space}:in_range={self.color_range}:out_color_matrix={self.color_space}:out_range={self.color_range}',
                  vsync=0,
                  ss='00:00:00',
                  vframes=1,
                  pix_fmt=pix_fmt)
          .run(capture_stdout=True, cmd=FFMPEG_PATH))
      self.frames = np.frombuffer(out, np.uint8).reshape([-1, self.height, self.width, 3])

    elif pix_fmt in ['yuv420p', 'yuvj420p']:
      out, _ = (
          ffmpeg
          .input(path, v='quiet', vsync=0)
          .output('pipe:', format='rawvideo', vsync=0, ss='00:00:00', vframes=1, pix_fmt=pix_fmt)
          .run(capture_stdout=True, cmd=FFMPEG_PATH))
      self.frames = np.frombuffer(out, np.uint8).reshape([-1, int(self.height * self.width * 1.5)])
    self.count = len(self.frames)

  def __str__(self):
    s = f'path: {self.path}'
    s += f', fps: {self.fps}'
    s += f', count x h x w: {self.count} x {self.height} x {self.width}'
    s += f', pix_fmt: {self.pix_fmt}'
    s += f', color_range: {self.color_range}'
    s += f', color_space: {self.color_space}'
    s += f', bitrate: {self.bitrate}'
    return s

  def __len__(self):
    return int(self.count)

  def __getitem__(self, idx):
    if isinstance(idx, slice):
      return [self[i] for i in range(*idx.indices(len(self)))]
    if idx >= self.count:
      raise IndexError
    frame = self.frames[idx]
    return frame

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    pass


class FFmpegAsyncWriter():

  def __init__(self,
               path: str,
               width: int = None,
               height: int = None,
               fps: float = 30.0,
               crf=16,
               color_range='tv',
               color_space='bt709',
               pix_fmt='bgr24'):
    super(FFmpegAsyncWriter, self).__init__()
    self.color_space = color_space
    self.color_range = color_range
    self.pix_fmt = pix_fmt
    self.width = width
    self.height = height
    self.path = path
    self.crf = crf
    self.fps = fps

    if self.width and self.height:
      self.pipeline = self.resize(height, width)
    else:
      self.pipeline = None

  def resize(self, height, width):
    self.height, self.width = height, width
    s = '{}x{}'.format(self.width, self.height)
    return (
        ffmpeg
        .input(
            'pipe:',
            format='rawvideo',
            pix_fmt=self.pix_fmt,
            s=s,
            v='error',
            framerate=self.fps,
            vsync=0)
        .output(
            self.path,
            crf=self.crf,
            preset='ultrafast',
            vf=f'scale=in_color_matrix={self.color_space}:in_range={self.color_range}:out_color_matrix={self.color_space}:out_range={self.color_range}',
            vcodec='libx264',
            acodec='copy',
            threads='0',
            s=s,
            v='error')
        .overwrite_output()
        .run_async(pipe_stdin=True, cmd=FFMPEG_PATH, quiet=True)
    )

  def write(self, frame):
    """write BGR frame (0-255) to video file
    """
    # build pipeline
    if self.pipeline is None:
      h, w = frame.shape[:2]
      self.pipeline = self.resize(height=h, width=w)
    self.pipeline.stdin.write(frame.tobytes())

  def close(self):
    if self.pipeline is not None:
      self.pipeline.stdin.close()
      self.pipeline.wait()

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.close()


if __name__ == '__main__':

  reader = FFmpegAsyncReader('/data4/ebench/benchmarks/face0409/615309681_17_2023-05-18_05:09:21_1.mp4')
