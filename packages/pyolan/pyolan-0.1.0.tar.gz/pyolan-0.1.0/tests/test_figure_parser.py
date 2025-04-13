import numpy as np
import schemas.aresti as a
from schemas.positioning import Orientation

from pyolan.figure_parser import OlanFig
from pyolan.rolls import ro, sn, spi


def test_olan_take() -> OlanFig:
    data = "2% `````4,3if``ry.'22 /~~+++..''1.'n('5if,3.).,8.---~".split(" ")
    ofig, newdata = OlanFig.take(data)

    assert isinstance(ofig, OlanFig)
    assert len(newdata) < len(data) and len(newdata) > 0

    assert ofig.fig.chars == "ry"

    assert ofig.prefix.roll_arr == [ro(1 / 4), sn(-3 / 4, True)]
    assert ofig.final.roll_arr == [ro(1 / 2), ro(1 / 2)]
    assert not ofig.suffix
    assert ofig.entry == Orientation.UPRIGHT
    assert ofig.exit == Orientation.UPRIGHT


def test_olan_take_with_drawing():
    ofig = OlanFig.take(["/~~+++..''1.'n('5if,3.).,8.---~"])[0]

    assert ofig.entry == Orientation.UPRIGHT
    assert ofig.exit == Orientation.INVERTED
    assert ofig.fig.chars == "n"
    assert ofig.prefix.roll_arr == [ro(1)]

    pass


def test_olan_take_with_drawing_2():
    ofig = OlanFig.take(["(-8,14)", "4%", "'',22m2"])[0]
    assert len(ofig.draw) == 2


def test_element_rolls():
    ofig = OlanFig.take(["/~~+++..''1.'n('5if,3.).,8.---~"])[0]
    rolls = [r.roll_arr if r else None for r in ofig.element_rolls()]
    assert not rolls[0]
    assert rolls[1] == [ro(1)]
    assert not rolls[2]
    assert rolls[3] == [sn(5 / 4, True), ro(-3 / 4)]
    assert not rolls[4]
    assert rolls[5] == [ro(1 / 8), ro(1 / 8)]

    ofig2 = OlanFig.take(["(13,8)", "-```5is';3..''iBb(``````````4',2`)....1~~"])[0]
    rolls = ofig2.element_rolls()
    assert rolls[1].roll_arr == [spi(5 / 4, True), ro(3 / 4)]


def test_3_element_rolls():
    fig = OlanFig.take(["2w(4)2"])[0]
    rolls = [r.total() if r else 0 for r in fig.element_rolls()]
    assert rolls == [0, 0.5, 0, 0.25, 0, 0.5, 0]


def test_fig_n_rolls():
    fig = OlanFig.take(["-.'pn(3f,3.')."])[0]
    rolls = [r.turns() if r else [] for r in fig.element_rolls()]
    assert rolls == [[], [], [], [3 / 4, -3 / 4], [], [], []]


def loop_amount_check(elstr, expected):
    oel = OlanFig.take([elstr])[0]
    np.testing.assert_array_equal(oel.loop_amounts(oel.element_rolls()), expected)


def test_loop_amounts():
    loop_amount_check("2pb2", [0.25, 0, -0.5, 0, 0.25])
    loop_amount_check("-2pb2", [-0.25, 0, -0.5, 0, 0.25])
    loop_amount_check("2pb2-", [0.25, 0, -0.5, 0, -0.25])
    loop_amount_check("-2pb2-", [-0.25, 0, -0.5, 0, -0.25])
    loop_amount_check("w", [1 / 8, 0, -3 / 8, 0, 3 / 8, 0, -1 / 8])
    loop_amount_check("w-", [1 / 8, 0, -3 / 8, 0, -3 / 8, 0, 1 / 8])
    loop_amount_check("ry", [1 / 4, 0, 5 / 8, 0, 1 / 8])
    loop_amount_check("ry-", [1 / 4, 0, -5 / 8, 0, -1 / 8])
    loop_amount_check("-ry", [-1 / 4, 0, 5 / 8, 0, 1 / 8])
    loop_amount_check("-ry-", [-1 / 4, 0, -5 / 8, 0, -1 / 8])
    loop_amount_check("n", [1 / 4, 0, 3 / 8, 0, -3 / 8, 0, -1 / 4])
    loop_amount_check("n-", [1 / 4, 0, 3 / 8, 0, -3 / 8, 0, 1 / 4])
    loop_amount_check("-n", [-1 / 4, 0, 3 / 8, 0, -3 / 8, 0, -1 / 4])
    loop_amount_check("-w", [-1 / 8, 0, 3 / 8, 0, 3 / 8, 0, -1 / 8])
    loop_amount_check("-2w(4)2", [-1 / 8, 0, -3 / 8, 0, -3 / 8, 0, -1 / 8])
    loop_amount_check("-2pb3,1if", [-1 / 4, 0, -1 / 2, 0, 1 / 4])
    loop_amount_check(
        "/~~+++..''1.'n('5if,3.).,8.---~", [1 / 4, 0, 3 / 8, 0, 3 / 8, 0, 1 / 4]
    )
    loop_amount_check(
        "-```5is';3..''iBb(``````````4',2`)....1~~",
        [1 / 4, 0, 1 / 2, 0, 1 / 2, 0, 1 / 4],
    )
    loop_amount_check("ib", [-0.25, 0, 0.5, 0, -0.25])


def test_q_loops():
    loop_amount_check("2q2", [0, -7 / 8, 0, 1 / 8])
    loop_amount_check("-q-", [0, -7 / 8, 0, -1 / 8])
    loop_amount_check("q", [0, 7 / 8, 0, 1 / 8])


def test_single_loop_amount():
    loop_amount_check("of", [1])


def test_olan_take_dhump():
    ofig = OlanFig.take(["-```5is';3..''iBb(``````````4',2`)....1~~"])[0]

    assert ofig.entry == Orientation.INVERTED
    assert ofig.exit == Orientation.UPRIGHT


def test_create_elements(olan_teardrop):
    pes = OlanFig.take([olan_teardrop])
    aresti = pes[0].create_elements()

    assert isinstance(aresti[0], a.PE)


def test_create_avalanche():
    ofig = OlanFig.take(["of2"])[0]
    pe = ofig.create_elements()
    assert len(pe) == 1


def test_olan_take_only_roll():
    ofig = OlanFig.take(["22"])[0]
    els = ofig.create_elements()
    assert len(els) == 1
    assert isinstance(els[0], a.PE)


def test_olan_take_turn():
    ofig = OlanFig.take(["j"])[0]
    els = ofig.create_elements()
    assert len(els) == 3


def test_olan_take_turn_2():
    ofig = OlanFig.take("3% 10> 4joi2>".split(" "))[0]
    assert ofig.fig.oels[0].turnamount == 1
    assert ofig.final.roll_arr == [ro(-1), ro(1)]


def test_olan_take_spin():
    ofig = OlanFig.take(["s"])[0]
    assert len(ofig.fig.oels) == 3
    assert ofig.prefix.roll_arr[0].turns == 1
    loop_amounts = ofig.loop_amounts(ofig.element_rolls())
    np.testing.assert_array_equal(loop_amounts, [-0.25, 0, 0.25])


def test_create_unl_loop():
    ofig = OlanFig.take(["o8;5f-"])[0]
    els = ofig.create_elements()
    pass


def test_create_spin_on_line():
    fig = OlanFig.take(["```9s....'ikz----~~"])[0]
    aresti = fig.create_elements()
    assert aresti[0].kind == "spin"


def test_imac_adv_reversing_loop():
    fig = OlanFig.take(["48,2rpp(,f)2"])[0]
    assert fig.fig.chars == "rpp"
