"""PWA icons (192/512 + maskable-512) for 비율 리사이즈.

Dark tile with a warm coral/rose (#fb7185) glow top edge, a 4:5 frame outline
and a landscape photo block centred inside it with even margins — the app's
one idea: the photo never gets cropped, the frame is filled around it.
"""
from PIL import Image, ImageDraw, ImageFilter

BG = (11, 14, 18)              # #0b0e12 app background
BG_GLOW = (66, 22, 34)         # rose top glow
ACCENT = (251, 113, 133)       # #fb7185
ACCENT_DEEP = (244, 63, 94)    # #f43f5e
PAPER = (255, 240, 241)        # #fff0f1
WORK = 1600


def background(size):
    grad = Image.new("RGB", (size, size))
    gd = ImageDraw.Draw(grad)
    for y in range(size):
        t = y / size
        f = (1 - t) ** 1.7
        gd.line([(0, y), (size, y)], fill=tuple(
            int(BG_GLOW[i] * f + BG[i] * (1 - f)) for i in range(3)
        ))
    return grad


def glyph(size, scale):
    """Portrait 4:5 frame outline + landscape photo block inside."""
    L = WORK
    layer = Image.new("L", (L, L), 0)
    d = ImageDraw.Draw(layer)

    def sx(v):
        return 0.5 + (v - 0.5) * scale

    # outer frame, 4:5 portrait
    fx0, fx1 = sx(0.275) * L, sx(0.725) * L
    fy0, fy1 = sx(0.185) * L, sx(0.815) * L
    stroke = 0.052 * scale * L
    d.rounded_rectangle([fx0, fy0, fx1, fy1], radius=0.058 * scale * L,
                        outline=255, width=int(round(stroke)))

    # photo block inside, landscape, centred with even margins
    px0, px1 = sx(0.345) * L, sx(0.655) * L
    py0, py1 = sx(0.395) * L, sx(0.605) * L
    d.rounded_rectangle([px0, py0, px1, py1], radius=0.020 * scale * L, fill=255)

    return layer.resize((size, size), Image.LANCZOS)


def make(size, scale=1.0):
    img = background(size).convert("RGBA")
    g = glyph(size, scale)

    glow = g.filter(ImageFilter.GaussianBlur(radius=size * 0.045)).point(lambda v: int(v * 0.6))
    img.paste(Image.new("RGBA", (size, size), ACCENT + (255,)), (0, 0), glow)

    grad = Image.new("RGB", (size, size))
    gd = ImageDraw.Draw(grad)
    for y in range(size):
        t = y / size
        gd.line([(0, y), (size, y)], fill=tuple(
            int(PAPER[i] * (1 - t) + ACCENT[i] * t) for i in range(3)
        ))
    img.paste(grad, (0, 0), g)
    return img


if __name__ == "__main__":
    make(512, 1.02).save("work/aspect-resize-repo/icon-512.png", optimize=True)
    make(192, 1.02).save("work/aspect-resize-repo/icon-192.png", optimize=True)
    make(512, 0.72).save("work/aspect-resize-repo/icon-maskable-512.png", optimize=True)
    print("icons written")
