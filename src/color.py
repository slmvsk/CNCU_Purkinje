import colorsys


def to_bytes(color):
    return [int(x * 256) for x in color]


def round(n):
    return [to_bytes(colorsys.hsv_to_rgb((i / n) % 1.0, 0.7, 0.9)) for i in range(n)]
