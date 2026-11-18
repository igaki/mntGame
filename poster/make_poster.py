"""Create an A5, 300 dpi mntGame poster with exact, selectable source text."""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics.barcode import qr


HERE = Path(__file__).resolve().parent
OUT = HERE / "mntGame_A5_poster.png"
URL = "https://igaki.github.io/mntGame/"
W, H = 1748, 2480  # A5 portrait at approximately 300 dpi

FONT_DIR = Path(r"C:\Windows\Fonts")
JP = FONT_DIR / "NotoSansJP-VF.ttf"
MONO = FONT_DIR / "consolab.ttf"


def font(size, mono=False):
    result = ImageFont.truetype(str(MONO if mono else JP), size)
    if not mono:
        result.set_variation_by_axes([750])
    return result


def centered(draw, y, value, size, fill, *, mono=False, stroke=0, stroke_fill=None):
    f = font(size, mono)
    box = draw.textbbox((0, 0), value, font=f, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y), value, font=f, fill=fill, stroke_width=stroke,
              stroke_fill=stroke_fill, anchor="lt")


img = Image.new("RGB", (W, H), "#111a42")
px = img.load()
for y in range(H):
    t = y / (H - 1)
    base = (16 + int(11 * t), 25 + int(15 * t), 62 + int(19 * t))
    for x in range(W):
        glow = max(0, 1 - math.hypot((x - 1320) / 1350, (y - 260) / 950))
        px[x, y] = (base[0] + int(9 * glow), base[1] + int(16 * glow), base[2] + int(29 * glow))

d = ImageDraw.Draw(img)

# Arcade-like framing and little stars.
d.rounded_rectangle((74, 76, W - 74, H - 76), radius=44, outline="#6b8ad0", width=7)
for x, y, r, color in [
    (150, 340, 22, "#ffdc54"), (1560, 335, 28, "#69e9ff"),
    (265, 460, 11, "#85f3ff"), (1475, 475, 12, "#ffdc54"),
    (160, 1520, 13, "#ffdc54"), (1570, 1510, 12, "#69e9ff"),
]:
    d.line((x - r, y, x + r, y), fill=color, width=7)
    d.line((x, y - r, x, y + r), fill=color, width=7)

d.rounded_rectangle((175, 118, W - 175, 470), radius=50, fill="#27326a", outline="#ffdf5c", width=9)
centered(d, 145, "mntGame", 200, "#ffdf5c", stroke=2, stroke_fill="#ffdf5c")
centered(d, 370, "2つの3Dゲームを あそぼう！", 60, "#ffffff")

# Game 1: red action card with a simple oni illustration.
d.rounded_rectangle((160, 555, W - 160, 1010), radius=50, fill="#80234e", outline="#ffb35b", width=10)
d.ellipse((910, 585, 1465, 975), fill="#bf3551")
d.polygon([(1040, 702), (1060, 610), (1134, 680)], fill="#ffd58a")
d.polygon([(1292, 680), (1370, 610), (1390, 708)], fill="#ffd58a")
d.ellipse((1070, 660, 1360, 940), fill="#ed6a54", outline="#ffe8ad", width=12)
d.rounded_rectangle((1122, 764, 1186, 792), radius=8, fill="#1b1a3e")
d.rounded_rectangle((1244, 764, 1308, 792), radius=8, fill="#1b1a3e")
d.arc((1166, 798, 1260, 886), 0, 180, fill="#1b1a3e", width=12)
d.line((1435, 620, 1355, 740), fill="#e9f9ff", width=17)
d.polygon([(1435, 620), (1395, 652), (1422, 670)], fill="#e9f9ff")
d.text((230, 620), "01  BATTLE ACTION", font=font(48, True), fill="#ffdf5c")
d.text((230, 704), "GIANT", font=font(108, True), fill="#ffffff")
d.text((230, 834), "BATTLE 3D", font=font(102, True), fill="#ffffff")
d.text((230, 933), "鬼とたたかえ！ 必殺技で大逆転！", font=font(42), fill="#ffe9e8")

# Game 2: blue jumping card with steps and a jumping player.
d.rounded_rectangle((160, 1050, W - 160, 1505), radius=50, fill="#0e5a8b", outline="#7af1ff", width=10)
d.ellipse((985, 1095, 1480, 1485), fill="#1377a2")
for i, (xx, yy) in enumerate([(984, 1412), (1088, 1348), (1200, 1270), (1320, 1188)]):
    d.polygon([(xx, yy), (xx + 114, yy - 30), (xx + 170, yy - 12), (xx + 55, yy + 18)],
              fill="#d3f8ff" if i % 2 == 0 else "#77e6fb")
    d.line((xx + 55, yy + 18, xx + 55, yy + 74), fill="#8ce6f8", width=12)
d.ellipse((1180, 1116, 1237, 1173), fill="#ffe0a6", outline="#ffffff", width=5)
d.line((1207, 1173, 1180, 1247), fill="#163968", width=27)
d.line((1194, 1202, 1148, 1180), fill="#163968", width=20)
d.line((1194, 1202, 1240, 1183), fill="#163968", width=20)
d.line((1180, 1247, 1144, 1285), fill="#163968", width=20)
d.line((1180, 1247, 1234, 1262), fill="#163968", width=20)
d.text((230, 1116), "02  JUMP ACTION", font=font(48, True), fill="#8ef7ff")
d.text((230, 1214), "空跳設備", font=font(120), fill="#ffffff")
d.text((230, 1375), "ジャンプで進め！ しかけを突破！", font=font(42), fill="#e0fbff")

# White access panel keeps URL legible even when the poster is printed small.
d.rounded_rectangle((130, 1580, W - 130, 2368), radius=50, fill="#ffffff", outline="#ffdc54", width=12)
centered(d, 1632, "あそびにいこう！", 68, "#18234f")
centered(d, 1732, "このURLを入力 または QRコードをスキャン", 36, "#404e77")
d.rounded_rectangle((186, 1812, W - 186, 1940), radius=20, fill="#edf4ff")

# Fit the entire literal URL on one line; monospaced glyphs distinguish i/l/1.
url_size = 68
while d.textbbox((0, 0), URL, font=font(url_size, True))[2] > W - 440:
    url_size -= 1
centered(d, 1835, URL, url_size, "#111b40", mono=True)

q = qr.QrCodeWidget(URL)
q.qr.make()
matrix = q.qr.modules
n = q.qr.moduleCount
module = 10
quiet = 4
qr_size = (n + quiet * 2) * module
qx = (W - qr_size) // 2
qy = 1970
d.rectangle((qx, qy, qx + qr_size, qy + qr_size), fill="#ffffff")
for row in range(n):
    for col in range(n):
        if matrix[row][col]:
            x0 = qx + (col + quiet) * module
            y0 = qy + (row + quiet) * module
            d.rectangle((x0, y0, x0 + module - 1, y0 + module - 1), fill="#111b40")

centered(d, 2333, "mntGame", 28, "#18234f", mono=True)

img.save(OUT, dpi=(300, 300), optimize=True)
print(OUT)
print(f"{W}x{H}px, 300dpi, URL={URL}, QR={n}x{n}")
