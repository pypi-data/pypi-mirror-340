import pytest

from colourings.conversions import (
    hex2hsl,
    hex2rgb,
    hex2web,
    hsl2hex,
    hsl2hsla,
    hsl2hslaf,
    hsl2hslf,
    hsl2rgb,
    hsl2web,
    hsla2hsl,
    hslf2hsl,
    rgb2hex,
    rgb2hsl,
    rgb2web,
    rgba2hsl,
    rgbaf2hsl,
    rgbf2hsl,
    web2hex,
    web2hsl,
    web2rgb,
)


def test_rgb2web():
    assert rgb2web((0, 0, 0)) == "black"
    assert rgb2web((0.0, 0.0, 0.0)) == "black"


def test_web2rgb():
    assert web2rgb("black") == (0.0, 0.0, 0.0)


def test_web2hsl():
    hsl = web2hsl("grey")
    assert hsl[0] == 0.0
    assert hsl[1] == 0.0
    assert round(hsl[2], 4) == 50.1961
    hsl1 = web2hsl("grey")
    assert hsl1[0] == 0.0
    assert hsl1[1] == 0.0
    assert round(hsl1[2], 4) == 50.1961


def test_hsl2web():
    assert hsl2web((0.0, 0.0, 50.20)) == "gray"


def test_hex2hsl():
    hsl = hex2hsl("#00ff00")
    assert round(hsl[0] / 360.0, 4) == 0.3333
    assert hsl[1] == 100.0
    assert hsl[2] == 50


def test_hsl2hex():
    assert hsl2hex((100.0, 100.0, 100.0)) == "#fff"


def test_hex2web_7_to_4_digits():
    assert hex2web("#112233") == "#123"


def test_web2hex():
    assert web2hex("#123", True) == "#112233"


def test_bad_rgbaf2hsl():
    with pytest.raises(ValueError):
        rgbaf2hsl("a")  # type: ignore
    with pytest.raises(ValueError):
        rgbaf2hsl((2, 0, 0, 0))
    with pytest.raises(ValueError):
        rgbaf2hsl((0, 2, 0, 0))
    with pytest.raises(ValueError):
        rgbaf2hsl((0, 0, 2, 0))
    with pytest.raises(ValueError):
        rgbaf2hsl((0, 0, 0, 2))


def test_bad_rgba2hsl():
    with pytest.raises(ValueError):
        rgba2hsl("a")  # type: ignore
    with pytest.raises(ValueError):
        rgba2hsl((256, 0, 0, 0))
    with pytest.raises(ValueError):
        rgba2hsl((0, 256, 0, 0))
    with pytest.raises(ValueError):
        rgba2hsl((0, 0, 256, 0))
    with pytest.raises(ValueError):
        rgba2hsl((0, 0, 0, 256))


def test_bad_rgbf2hsl():
    with pytest.raises(ValueError):
        rgbf2hsl("a")  # type: ignore
    with pytest.raises(ValueError):
        rgbf2hsl((1.1, 0, 0, 0))
    with pytest.raises(ValueError):
        rgbf2hsl((0, 1.1, 0, 0))
    with pytest.raises(ValueError):
        rgbf2hsl((0, 0, 1.1, 0))
    with pytest.raises(ValueError):
        rgbf2hsl((0, 0, 0, 1.1))


def test_bad_hsla2hsl():
    with pytest.raises(ValueError):
        hsla2hsl("a")  # type: ignore
    with pytest.raises(ValueError):
        hsla2hsl((370, 0, 0, 0))
    with pytest.raises(ValueError):
        hsla2hsl((0, 200, 0, 0))
    with pytest.raises(ValueError):
        hsla2hsl((0, 0, 200, 0))
    with pytest.raises(ValueError):
        hsla2hsl((0, 0, 0, 200))


def test_bad_hex2web():
    with pytest.raises(ValueError):
        hex2web("black")


def test_bad_web2hex():
    with pytest.raises(AttributeError):
        web2hex("#1234")
    with pytest.raises(ValueError):
        web2hex("123")


def test_bad_web2rgb():
    with pytest.raises(ValueError):
        web2rgb("#1234")
    with pytest.raises(ValueError):
        web2rgb("123")


def test_bad_web2hsl():
    with pytest.raises(ValueError):
        web2hsl("#1234")
    with pytest.raises(ValueError):
        web2hsl("123")


def test_bad_hsl2web():
    with pytest.raises(ValueError):
        hsl2web("a")  # type: ignore
    with pytest.raises(ValueError):
        hsl2web((0, 0, 0, 0))
    with pytest.raises(ValueError):
        hsl2web((361, 0, 0))
    with pytest.raises(ValueError):
        hsl2web((0, 110, 0))
    with pytest.raises(ValueError):
        hsl2web((0, 0, 110))


def test_bad_hsl2hex():
    with pytest.raises(ValueError):
        hsl2hex("a")  # type: ignore
    with pytest.raises(ValueError):
        hsl2hex((0, 0, 0, 0))
    with pytest.raises(ValueError):
        hsl2hex((361, 0, 0))
    with pytest.raises(ValueError):
        hsl2web((0, 110, 0))
    with pytest.raises(ValueError):
        hsl2web((0, 0, 110))


def test_bad_hex2hsl():
    with pytest.raises(ValueError):
        hex2hsl("black")
    with pytest.raises(ValueError):
        hex2hsl("#black")


def test_bad_rgb2web():
    with pytest.raises(ValueError):
        rgb2web("a")  # type: ignore
    with pytest.raises(ValueError):
        rgb2web((1, 0, 0, 0))
    with pytest.raises(ValueError):
        rgb2web((-1, 0, 0))


def test_bad_hsl2rgb():
    with pytest.raises(ValueError):
        hsl2rgb((0, 102, 0))
    with pytest.raises(ValueError):
        hsl2rgb((0, 0, 102))
    with pytest.raises(ValueError):
        hsl2rgb((0, 0, -1))
    with pytest.raises(ValueError):
        hsl2rgb((0, -1, 0))


def test_bad_rgb2hex():
    with pytest.raises(ValueError):
        rgb2hex((-1, 0, 0, 0))
    with pytest.raises(ValueError):
        rgb2hex((260, 0, 0))


def test_bad_rgb2hsl():
    with pytest.raises(ValueError):
        rgb2hsl((0, 0, -1))
    with pytest.raises(ValueError):
        rgb2hsl((0, -1, 0))
    with pytest.raises(ValueError):
        rgb2hsl((-1, 0, 0))


def test_bad_hex2rgb():
    with pytest.raises(ValueError):
        hex2rgb("#00ff000")


def test_bad_hsl2hsla():
    with pytest.raises(ValueError):
        hsl2hsla((-1, 0, 0), 1)


def test_bad_hsl2hslaf():
    with pytest.raises(ValueError):
        hsl2hslaf((-1, 0, 0), 1)


def test_bad_hslf2hsl():
    with pytest.raises(ValueError):
        hslf2hsl((-1, 0, 0))


def test_bad_hsl2hslf():
    with pytest.raises(ValueError):
        hsl2hslf((-1, 0, 0))
