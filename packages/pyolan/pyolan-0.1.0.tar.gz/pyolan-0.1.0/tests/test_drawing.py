import re

from pyolan.drawing import re_dpre, re_draw, re_drawing


def test_re_drawing():
    assert re.match(re_dpre["move"], "(-8,14)")
    assert re.match(re_drawing, "(‑2,0)")


def test_remove_draw_instructions(olan_teardrop):
    res = re_draw.sub("", olan_teardrop)
    assert res == "4,3ifry22"


def test_drawing():
    assert re_drawing.match("ed")
    assert re_drawing.match("eja")
    assert not re_drawing.match("ejj")
    assert re_drawing.match("//")
    assert re_drawing.match("[1,2]")
    assert re_drawing.match("(1,2)")
    assert re_drawing.match("100%")
    assert re_drawing.match(">")
    assert re_drawing.match("^")
    assert not re_drawing.match("/saa")
    assert re_drawing.match('"sdcs 98y #"')
    assert re_drawing.match("@A")
    assert not re_drawing.match("@AA")
    assert re_drawing.match("11>")
