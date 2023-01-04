import bluetooth
from . import epd_models
import logging
import importlib
import math
import numpy
import select
import struct
import time
import os
import waveshare_epd


class EPD:
  def __init__(self, epd_model, colour, h_flip, v_flip):
    if not epd_model in epd_models.EPD_MODELS:
      raise ValueError(f'Model {epd_model} is not supported!')
    self.display = epd_models.EPD_MODELS[epd_model]
    self.resolution = self.display.resolution
    self.width, self.height = self.resolution
    self.colors = [epd_models.ALL_COLORS[c] for c in self.display.palette]
    for (index, color) in enumerate(self.colors):
      setattr(self, color, index)

    self.buf = numpy.zeros((self.height, self.width), dtype=numpy.uint8)

    if colour not in ('red', 'black', 'yellow', 'multi'):
      raise ValueError('Colour {} is not supported!'.format(colour))

    self.colour = colour

    self.h_flip = h_flip
    self.v_flip = v_flip

  def __str__(self):
    return self.display.name

  @property
  def palette(self):
    return self.display.palette

  def _update(self, buf):
    pass

  def _get_buf(self, region):
    pass

  def _is_valid(self, c):
    return c >= 0 and c < len(self.palette)

  def set_pixel(self, x, y, colour):
    """Set a single pixel on the buffer.

    :param int x: x position on display.
    :param int y: y position on display.
    :param int v: Colour to set, valid values are `inky.BLACK`, `inky.WHITE`, `inky.RED` and `inky.YELLOW`.
    """
    if self._is_valid(colour):
        self.buf[y][x] = colour

  def show(self, busy_wait=True):
    """Show buffer on display.

    :param bool busy_wait: If True, wait for display update to finish before returning, default: `True`.
    """
    region = self.buf

    if self.v_flip:
        region = numpy.fliplr(region)

    if self.h_flip:
        region = numpy.flipud(region)

    buf = self._get_buf(region)

    self._update(buf, busy_wait=busy_wait)

  def set_border(self, colour):
    """Set the border colour.

    :param int colour: The border colour. Valid values are `inky.BLACK`, `inky.WHITE`, `inky.RED` and `inky.YELLOW`.
    """
    if self._is_valid(colour):
      self.border_colour = colour

  def set_image(self, image):
    """Copy an image to the buffer.

    The dimensions of `image` should match the dimensions of the display being used.

    :param image: Image to copy.
    :type image: :class:`PIL.Image.Image` or :class:`numpy.ndarray` or list
    """

    self.buf = numpy.array(image, dtype=numpy.uint8).reshape((self.width, self.height))


class InkyEPD(EPD):

  def __init__(self, epd_model, colour, h_flip=False, v_flip=False):
    super().__init__(epd_model, colour, h_flip, v_flip)
    logging.info(f'Load {epd_model}')
    epd_module = importlib.import_module(f'waveshare_epd.{self.display.epd_module}')
    self._epd = epd_module.EPD()

  def setup(self):
    """Set up Inky GPIO and reset display."""
    self._epd.init()
    self._busy_wait()

  def _busy_wait(self):
    """Wait for busy/wait pin."""
    self._epd.ReadBusy()

  def _get_buf(self, region):
    buf = [ numpy.packbits(numpy.where(region == self.BLACK, 0, 1)).tolist() ]
    if len(self.palette) > 2:
      buf.append(numpy.packbits(numpy.where(region > self.BLACK, 0, 1)).tolist())
    return buf

  def _update(self, buf, busy_wait=True):
    """Update display.

    :param buf_a: Black/White pixels
    :param buf_b: Yellow/Red pixels

    """
    self.setup()

    self._epd.display(*buf)

    if busy_wait:
      self._busy_wait()
      self._epd.sleep()  # Enter Deep Sleep

  def clear(self):
    logging.info("Clear")
    self.setup()
    self._epd.Clear()
    time.sleep(1)


BUF_SIZE = 256

class InkyEPDBluetooth(InkyEPD):
  def __init__(self, macAddress, epd_model, colour, h_flip=False, v_flip=False):
    super().__init__(epd_model, colour, h_flip, v_flip)
    logging.info(f'Load {epd_model}({macAddress})')
    self.macAddress = macAddress
    self.port = None
    for service in bluetooth.find_service(address=macAddress):
      if service['protocol'] == 'RFCOMM':
         self.port = service['port']
    if not self.port:
      raise ValueError(f'RFCOMM not found on device: {macAddress}')
    self._socket = None

  def setup(self):
    """Set up bluetooth connection."""
    if not self._socket:
      self._socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
      self._socket.connect((self.macAddress, self.port))
      self._socket.setblocking(False)

  def _waitForReply(self, timeout=0.01):
    """Wait for reply."""
    resp = b''
    start = time.time()
    while time.time() - start < timeout or not resp:
      ready = select.select([self._socket], [], [], 0.1)
      if ready[0]:
        data = self._socket.recv(256)
        resp += data
        if data[-1:] == b'!':
          break
        start = time.time()
    self._socket.setblocking(True)
    logging.debug(f'received: {resp}')
    return resp

  def _send(self, data):
    logging.debug(f'send: {data}')
    self._socket.sendall(data)

  def _get_buf(self, region):
    low_bit = numpy.where(region != 1, 1, 0)
    high_bit = numpy.where(region > 1, 1, 0)
    two_bits = numpy.dstack([low_bit, high_bit])
    return numpy.packbits(two_bits, bitorder='little')

  def _update(self, buf, busy_wait=True):
    """Update display.

    :param buf_a: Black/White pixels
    :param buf_b: Yellow/Red pixels

    """
    self.setup()

    data = struct.pack('cB', b'I', self.display.id)
    self._send(data)

    reply = self._waitForReply()
    if reply != b'Ok!':
      return False

    buf_len = len(buf)
    HEAD_SIZE = 6
    CHUNK_SIZE = BUF_SIZE - HEAD_SIZE
    i = 0
    while i * CHUNK_SIZE < buf_len:
      chunk = bytes(buf[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE] if (i+1) * CHUNK_SIZE <= buf_len else buf[i*CHUNK_SIZE:])
      head = struct.pack('<cHI', b'L', len(chunk)+HEAD_SIZE, i*BUF_SIZE+len(chunk)+HEAD_SIZE)[0:6]
      self._send(head)
      self._send(chunk)
      reply = self._waitForReply()
      if reply != b'Ok!':
        return False
      i += 1

    data = b'S'
    self._send(data)

    reply = self._waitForReply()
    if reply != b'Ok!':
      return False

    return True


  def clear(self):
    logging.info("Clear")
    self.setup()
    self._epd.Clear()
    time.sleep(1)

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--log-level',
      default=logging.INFO,
      type=lambda x: getattr(logging, x),
      help='Configure the logging level. default: INFO'
  )
  args = parser.parse_args()
  logging.basicConfig(level=args.log_level)

  epd = InkyEPDBluetooth('78:E3:6D:12:F5:0E', 'epd7in5b', 'red')
  for x in range(100, 200):
    for y in range(100, 200):
      epd.set_pixel(x, y, epd.BLACK)
  for x in range(350, 450):
    for y in range(150, 350):
      epd.set_pixel(x, y, epd.RED)
  epd.show()
