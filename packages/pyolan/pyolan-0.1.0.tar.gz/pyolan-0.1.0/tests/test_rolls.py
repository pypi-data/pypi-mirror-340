import schemas.positioning as pos

from pyolan.rolls import OlanRoll, oroll_re, ro, sn


def test_oroll_re():
    assert oroll_re.search("2f").group(0) == "2f"
    assert oroll_re.search("2").group(0) == "2"
    assert oroll_re.search("24is").group(0) == "24is"


def check_roll_parse(roll, expected):
    assert OlanRoll.parse(roll).roll_arr == expected


def test_parse_roll():
    check_roll_parse("1", [ro(1)])
    check_roll_parse("1f", [sn(1, False)])
    check_roll_parse("1f,1f", [sn(1, False), sn(-1, False)])
    check_roll_parse("1f;1f", [sn(1, False), sn(1, False)])
    check_roll_parse("22;1", [ro(0.5), ro(0.5), ro(1)])
    check_roll_parse("22;1", [ro(0.5), ro(0.5), ro(1)])
    check_roll_parse(",8", [ro(1 / 8), ro(1 / 8)])


def check_olanroll(rollstr, angles, rtypes):
    oroll: OlanRoll = OlanRoll.parse(rollstr)
    assert oroll.angles() == angles
    assert oroll.rolltypes() == rtypes


def test_olanroll():
    check_olanroll("1", pos.r(1), "roll")
    check_olanroll("1f", pos.r(1), "snap")
    check_olanroll("1f,1f", pos.r([1, -1]), "snap")
    check_olanroll("1f;1f", pos.r([1, 1]), "snap")
    check_olanroll("22", pos.r([0.5, 0.5]), "roll")
    check_olanroll("22,1f", pos.r([0.5, 0.5, -1]), "rrs")
    check_olanroll("1s,1f", pos.r([1, -1]), "-s")


def test_olanroll_single():
    check_olanroll("f", pos.r(1), "snap")


def test_oroll_pfc_roll():
    assert OlanRoll.parse("88").pfc_roll() == "8x8"

    assert OlanRoll.parse("2,2f").pfc_roll() == pos.r([0.5, -0.5])
