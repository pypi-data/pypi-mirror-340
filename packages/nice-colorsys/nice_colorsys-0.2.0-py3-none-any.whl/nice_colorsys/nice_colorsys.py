import colorsys
from itertools import permutations
from collections import namedtuple

def range_restrict(x, min_, max_, mod):
    if not mod:
        return max(min_, min(max_, x))
    else:
        return (x - min_) % (max_ - min_) + min_

def safe(self):
    return type(self)(
        *(
            range_restrict(x, *r, m) if r is not None else x
            for (x, r, m) in zip(self, type(self).ranges, type(self).modular)
        )
    )

def colorspace(name, fields, ranges=None, modular=None):
    if modular is None:
        modular = (False,)*len(fields)
    res = namedtuple(name, fields)
    if ranges is not None:
        res.ranges = ranges
        res.modular = modular
        res.safe = safe
    return res
        
h_mod = (True, False, False)
unit = ((0, 1),)
hls = colorspace("hls", ["hue", "lightness", "saturation"], unit*3, h_mod)
hsv = colorspace("hsv", ["hue", "saturation", "value"], unit*3, h_mod)
rgb = colorspace("rgb", ["red", "green", "blue"], unit*3)
yiq = colorspace(
    "yiq",
    ["luma", "in_phase", "quadrature"],
    ((0, 1), (-0.5957, 0.5957), (-0.5226, 0.5226))
)
chrominance = namedtuple("chrominance", ["in_phase", "quadrature"])
yiq.luma = property(lambda x: x.in_phase)
yiq.chrominance = property(lambda x: chrominance(x.in_phase, x.quadrature))
spaces = {"hls": hls, "hsv": hsv, "rgb": rgb, "yiq": yiq}
__all__ = list(spaces)
for s in spaces:
    spaces[s].to_rgb = (lambda _s: lambda x: rgb(*(getattr(colorsys, f"{_s}_to_rgb")(*x))))(s)
rgb.to_rgb = lambda _s: _s
non_rgb = set(spaces) - {"rgb"}
for s in non_rgb:
    setattr(rgb, f"to_{s}", (lambda _s: lambda x: spaces[_s](*(getattr(colorsys, f"rgb_to_{_s}")(*x))))(s))
for s1, s2 in permutations(set(spaces) - {"rgb"}, 2):
    setattr(
        spaces[s1],
        f"to_{s2}",
        (lambda _s2: lambda x: spaces[_s2](*(getattr(x.to_rgb(), f"to_{_s2}")())))(s2)
    )
