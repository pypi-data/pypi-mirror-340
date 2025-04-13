from .nice_colorsys import rgb, colorspace
from .custom_space import register_space

rgb255 = colorspace("rgb255", ["red", "green", "blue"], [(0, 255)]*3)
register_space(
    rgb255,
    lambda x: rgb(*(c/255 for c in x)),
    lambda x: rgb255(*(round(c*255) for c in x))
)
rgb255.as_hex = lambda x: "".join("{:02x}".format(c) for c in x)

__all__ = ["rgb255"]
