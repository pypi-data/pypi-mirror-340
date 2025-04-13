from  .nice_colorsys import spaces, rgb

def casted(type_, f):
    def inner(x):
        return type_(*f(x))
    return inner

def register_space(space: type, to_rgb, from_rgb, name=None, cast=True):
    if name is None:
        name = space.__name__
    if cast:
        to_rgb = casted(rgb, to_rgb)
        from_rgb = casted(space, from_rgb)
    spaces[name] = space
    space.to_rgb = to_rgb
    to_name = f"to_{name}"
    setattr(rgb, to_name, from_rgb)
    f = lambda x: getattr(x.to_rgb(), to_name)()
    for s in (set(spaces) - {"rgb", name}):
        setattr(spaces[s], f"to_{name}", f)
    for s in (set(spaces) - {"rgb", "hsluv"}):
        setattr(
            space,
            f"to_{s}",
            (lambda _s: lambda x: getattr(x.to_rgb(), f"to_{_s}")())(s)
        )

def derived_rgb_functions(a, b, to_a, from_a):
    return (
        lambda x: a(*to_a(x)).to_rgb(),
        lambda x: b(*from_a(getattr(x, f"to_{a.__name__}")()))
    )

__all__ = ["register_space", "derived_rgb_functions"]
