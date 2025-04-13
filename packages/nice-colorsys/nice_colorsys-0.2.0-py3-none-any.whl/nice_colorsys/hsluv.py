import hsluv as hsluv_
from .custom_space import register_space, derived_rgb_functions
from .nice_colorsys import colorspace

hsluv = colorspace(
    "hsluv",
    ["hue", "saturation", "lightness"],
    ((0, 360), (0, 100), (0, 100))
)
luv = cieluv = colorspace(
    "cieluv",
    ["luminance", "u", "v"],
    ((0, 100), (-134, 220), (-140, 122))
)
luv.l = property(lambda x: x.luminance)
lch = cielch = colorspace(
    "cielch",
    ["luminance", "chroma", "hue"],
    ((0, 100), (0, None), (0, 360)),
    (False, False, True)
)
lch.c = property(lambda x: x.chroma)
lch.h = property(lambda x: x.hue)
xyz = ciexyz = colorspace("ciexyz", ["x", "lightness", "z"])
xyz.y = property(lambda x: x.lightness)
register_space(hsluv, hsluv_.hsluv_to_rgb, hsluv_.rgb_to_hsluv)
register_space(lch, hsluv_.lch_to_rgb, hsluv_.rgb_to_lch)
register_space(
    luv,
    *derived_rgb_functions(
        lch,
        luv,
        hsluv_.luv_to_lch,
        hsluv_.lch_to_luv
    )
)
register_space(ciexyz, hsluv_.xyz_to_rgb, hsluv_.rgb_to_xyz)

__all__ = ["hsluv", "luv", "lch", "xyz", "cieluv", "cielch", "ciexyz"]
