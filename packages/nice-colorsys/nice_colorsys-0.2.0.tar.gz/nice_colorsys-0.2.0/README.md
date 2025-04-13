# nice_colorsys

This is a very small library that may offer a nicer way of working with and
converting between color systems than the default Python colorsys library.

In this library, a color in each supported color system is represented as a
`namedtuple` with `to_` methods for converting to different color systems.

## Supported color systems

### Main/built-in

* RGB (0.0&ndash;1.0)
* HLS
* HSV
* YIQ
* RGB (0&ndash;255) (with [`nice_colorsys.rgb255`](src/nice_colorsys/rgb255.py))

### With [hsluv](https://github.com/hsluv/hsluv-python) via [`nice_colorsys.hsluv`](src/nice_colorsys/hsluv.py)

* HSLuv
* CIELUV
* CIELCH
* CIEXYZ

## Example

```python
from nice_colorsys import *

print(hsv(0.5, 1, 1).to_hls())

# Output:
#
# hls(hue=0.5, lightness=0.5, saturation=1.0)
```
