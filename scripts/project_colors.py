"""Name-seeded, visually distinct project identity colors in perceptual OKLab.

Uses FNV-1a over the normalized name, golden-angle OKLCH hue candidates,
sRGB gamut fitting and minimum OKLab separation. Stable former identities
are reserved; new ones are deterministically selected in slug/name order.
This is a human-distinction heuristic, not a claim of universal uniqueness.
"""
import math

GOLDEN_ANGLE = 137.50776405003785
LIGHTNESS = 0.68
CHROMA = 0.14
MIN_DELTA_E = 0.12
MIN_HUE_GAP = 38.0

# Existing, owner-approved visual identities remain unchanged.
LEGACY_COLORS = {"architectarium": "#B9905D", "stratlas": "#6B9DC4"}


def hash_name(name):
    value = 0x811C9DC5
    for code in name.strip().casefold().encode("utf-8"):
        value = ((value ^ code) * 0x01000193) & 0xFFFFFFFF
    return value


def rgb_to_oklab(color):
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = (x / 12.92 if x <= 0.04045 else ((x + .055) / 1.055) ** 2.4 for x in rgb)
    l = (.4122214708*r + .5363325363*g + .0514459929*b) ** (1/3)
    m = (.2119034982*r + .6806995451*g + .1073969566*b) ** (1/3)
    s = (.0883024619*r + .2817188376*g + .6299787005*b) ** (1/3)
    return (
        .2104542553*l + .7936177850*m - .0040720468*s,
        1.9779984951*l - 2.4285922050*m + .4505937099*s,
        .0259040371*l + .7827717662*m - .8086757660*s,
    )


def oklch_to_hex(hue):
    for step in range(19):
        chroma = CHROMA - step * .004
        a, b = chroma * math.cos(math.radians(hue)), chroma * math.sin(math.radians(hue))
        l = (LIGHTNESS + .3963377774*a + .2158037573*b) ** 3
        m = (LIGHTNESS - .1055613458*a - .0638541728*b) ** 3
        s = (LIGHTNESS - .0894841775*a - 1.291485548*b) ** 3
        linear = (
            4.0767416621*l - 3.3077115913*m + .2309699292*s,
            -1.2684380046*l + 2.6097574011*m - .3413193965*s,
            -.0041960863*l - .7034186147*m + 1.7076147010*s,
        )
        if any(x < 0 or x > 1 for x in linear):
            continue
        channels = [
            round(255 * (12.92*x if x <= .0031308 else 1.055*x ** (1/2.4) - .055))
            for x in linear
        ]
        return "#" + "".join(f"{max(0, min(255, x)):02X}" for x in channels)
    raise ValueError("No in-gamut OKLCH color candidate")


def oklab_distance(first, second):
    return math.sqrt(sum((a-b)**2 for a, b in zip(rgb_to_oklab(first), rgb_to_oklab(second))))


def hue_gap(first, second):
    _, a1, b1 = rgb_to_oklab(first)
    _, a2, b2 = rgb_to_oklab(second)
    h1, h2 = math.degrees(math.atan2(b1,a1)), math.degrees(math.atan2(b2,a2))
    return abs((h1-h2+180) % 360 - 180)


def assign_colors(names, fixed=None):
    colors = dict(LEGACY_COLORS if fixed is None else fixed)
    for name in sorted(names, key=str.casefold):
        slug = name.casefold()
        if slug in colors:
            continue
        base = (hash_name(name) * GOLDEN_ANGLE) % 360
        for candidate in range(28):
            color = oklch_to_hex((base + candidate * GOLDEN_ANGLE) % 360)
            if all(
                oklab_distance(color, old) >= MIN_DELTA_E
                and hue_gap(color, old) >= MIN_HUE_GAP
                for old in colors.values()
            ):
                colors[slug] = color
                break
        else:
            raise ValueError(f"No suitably distinct OKLab candidate for {name}")
    return colors
