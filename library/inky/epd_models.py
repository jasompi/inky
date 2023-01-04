

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255,255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 128, 0)

ALL_COLORS = {
  COLOR_BLACK: 'BLACK',
  COLOR_WHITE: 'WHITE',
  COLOR_RED: 'RED',
  COLOR_GREEN: 'GREEN',
  COLOR_BLUE: 'BLUE',
  COLOR_GRAY: 'GRAY',
  COLOR_YELLOW: 'YELLOW',
  COLOR_ORANGE: 'ORANGE',
}

EPD_PALETTES = [
  [ COLOR_WHITE, COLOR_BLACK, ],
  [ COLOR_WHITE, COLOR_BLACK, COLOR_RED, ],
  [ COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, ],
  [ COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, COLOR_RED, ],
  [ COLOR_WHITE, COLOR_BLACK, ],
  [ COLOR_WHITE, COLOR_BLACK, COLOR_YELLOW],
  [],
  [ COLOR_WHITE, COLOR_BLACK, COLOR_GREEN, COLOR_BLUE, COLOR_RED, COLOR_YELLOW, COLOR_ORANGE],
]

class EPaperDisplay:
  def __init__(self, epd_module, resolution, palette_index, name, id):
    self.resolution = resolution
    self.epd_module = epd_module
    self.palette = EPD_PALETTES[palette_index]
    self.name = name
    self.id = id

  def __str__(self):
    return f'{self.name} ({self.resolution[0]}x{self.resolution[1]})'

EPD_MODELS = {
  "epd1in54" : EPaperDisplay("epd1in54", (200,200), 0, "1.54 inch e-Paper", 0),
#   "epd1in54b" : EPaperDisplay("epd1in54b", (200,200), 3, "1.54 inch e-Paper (B)", 1),
  "epd1in54b" : EPaperDisplay("epd1in54b", (200,200), 1, "1.54 inch e-Paper (B)", 1),
  "epd1in54c" : EPaperDisplay("epd1in54c", (152,152), 5, "1.54 inch e-Paper (C)", 2),
  "epd2in13" : EPaperDisplay("epd2in13", (122,250), 0, "2.13 inch e-Paper", 3),
  "epd2in13b" : EPaperDisplay("epd2in13bc", (104,212), 1, "2.13 inch e-Paper (B)", 4),
  "epd2in13c" : EPaperDisplay("epd2in13bc", (104,212), 5, "2.13 inch e-Paper (C)", 5),
  "epd2in13d" : EPaperDisplay("epd2in13d", (104,212), 0, "2.13 inch e-Paper (D)", 6),
  "epd2in7" : EPaperDisplay("epd2in7", (176,264), 0, "2.7 inch e-Paper", 7),
  "epd2in7b" : EPaperDisplay("epd2in7b", (176,264), 1, "2.7 inch e-Paper (B)", 8),
  "epd2in9" : EPaperDisplay("epd2in9", (128,296), 0, "2.9 inch e-Paper", 9),
  "epd2in9b" : EPaperDisplay("epd2in9bc", (128,296), 1, "2.9 inch e-Paper (B)", 10),
  "epd2in9c" : EPaperDisplay("epd2in9bc", (128,296), 5, "2.9 inch e-Paper (C)", 11),
  "epd2in9d" : EPaperDisplay("epd2in9d", (128,296), 0, "2.9 inch e-Paper (D)", 12),
  "epd4in2" : EPaperDisplay("epd4in2", (400,300), 0, "4.2 inch e-Paper", 13),
  "epd4in2b" : EPaperDisplay("epd4in2bc", (400,300), 1, "4.2 inch e-Paper (B)", 14),
  "epd4in2c" : EPaperDisplay("epd4in2bc", (400,300), 5, "4.2 inch e-Paper (C)", 15),
  "epd5in83" : EPaperDisplay("epd5in83", (600,448), 0, "5.83 inch e-Paper", 16),
  "epd5in83b" : EPaperDisplay("epd5in83bc", (600,448), 1, "5.83 inch e-Paper (B)", 17),
  "epd5in83c" : EPaperDisplay("epd5in83bc", (600,448), 5, "5.83 inch e-Paper (C)", 18),
  "epd7in5" : EPaperDisplay("epd7in5", (640,384), 0, "7.5 inch e-Paper", 19),
  "epd7in5b" : EPaperDisplay("epd7in5bc", (640,384), 1, "7.5 inch e-Paper (B)", 20),
  "epd7in5c" : EPaperDisplay("epd7in5bc", (640,384), 5, "7.5 inch e-Paper (C)", 21),
  "epd7in5_V2" : EPaperDisplay("epd7in5_V2", (800,480), 0, "7.5 inch e-Paper V2", 22),
  "epd7in5b_V2" : EPaperDisplay("epd7in5b_V2", (800,480), 1, "7.5 inch e-Paper (B) V2", 23),
  "epd7in5b_HD" : EPaperDisplay("epd7in5b_HD", (880,528), 1, "7.5 inch HD e-Paper (B)", 24),
  "epd5in65f" : EPaperDisplay("epd5in65f", (600,448), 7, "5.65 inch e-Paper (F)", 25),
  "epd7in5_HD" : EPaperDisplay("epd7in5_HD", (880,528), 0, "7.5 inch HD e-Paper", 26),
  "epd3in7" : EPaperDisplay("epd3in7", (280,480), 0, "3.7 inch e-Paper", 27),
  "epd2in66" : EPaperDisplay("epd2in66", (152,296), 0, "2.66 inch e-Paper", 28),
  "epd5in83b_V2" : EPaperDisplay("epd5in83b_V2", (648,480), 1, "5.83 inch e-Paper (B) V2", 29),
  "epd2in9b_V3" : EPaperDisplay("epd2in9b_V3", (128,296), 1, "2.9 inch e-Paper (B) V3", 30),
  "epd1in54b_V2" : EPaperDisplay("epd1in54b_V2", (200,200), 1, "1.54 inch e-Paper (B) V2", 31),
  "epd2in13b_V3" : EPaperDisplay("epd2in13b_V3", (104,214), 1, "2.13 inch e-Paper (B) V3", 32),
  "epd2in9_V2" : EPaperDisplay("epd2in9_V2", (128,296), 0, "2.9 inch e-Paper V2", 33),
  "epd4in2b_V2" : EPaperDisplay("epd4in2b_V2", (400,300), 1, "4.2 inch e-Paper (B) V2", 34),
  "epd2in66b" : EPaperDisplay("epd2in66b", (152,296), 1, "2.66 inch e-Paper (B)", 35),
  "epd5in83_V2" : EPaperDisplay("epd5in83_V2", (648,480), 0, "5.83 inch e-Paper V2", 36),
  "epd4in01f" : EPaperDisplay("epd4in01f", (640,400), 7, "4.01 inch e-Paper (F)", 37),
  "epd2in7b_V2" : EPaperDisplay("epd2in7b_V2", (176,264), 1, "2.7 inch e-Paper (B) V2", 38),
  "epd2in13_V3" : EPaperDisplay("epd2in13_V3", (122,250), 0, "2.13 inch e-Paper V3", 39),
  "epd2in13b_V4" : EPaperDisplay("epd2in13b_V4", (122,250), 1, "2.13 inch e-Paper (B) V4", 40),
  "epd3in52" : EPaperDisplay("epd3in52", (240,360), 0, "3.52 inch e-Paper", 41),
  "epd2in7_V2" : EPaperDisplay("epd2in7_V2", (176,264), 0, "2.7 inch e-Paper V2", 42), }
