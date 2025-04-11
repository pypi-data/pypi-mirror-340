import hsluv as hsluv_
from collections import namedtuple
from .custom_space import register_space, derived_rgb_functions

hsluv = namedtuple("hsluv", ["hue", "saturation", "lightness"])
luv = cieluv = namedtuple("cieluv", ["luminance", "u", "v"])
luv.l = property(lambda x: x.luminance)
lch = cielch = namedtuple("cielch", ["luminance", "chroma", "hue"])
lch.c = property(lambda x: x.chroma)
lch.h = property(lambda x: x.hue)
xyz = ciexyz = namedtuple("ciexyz", ["x", "lightness", "z"])
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
