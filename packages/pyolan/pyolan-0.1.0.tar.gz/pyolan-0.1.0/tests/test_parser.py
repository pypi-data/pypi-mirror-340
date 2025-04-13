import numpy as np
from pytest import approx
from schemas.positioning import Direction
from flightanalysis.builders.example.manbuilder import mb

from pyolan.parser import ParsedOlanFig, parse_olan


def test_entry_direction():
    ofigs = parse_olan("13% -``5if```,4ao(,1),22+`", mb)
    assert ofigs[0].aresti.info.start.direction == Direction.UPWIND


def test_create_unl_loop_definition():

    ofig: ParsedOlanFig = parse_olan("`+o34;5f+`", mb)[0]

    pass
    #assert "point_length" in ofig.definition.mps.data.keys()


def test_imac_sportsman_2025():
    oseq = parse_olan(
        "/d'1 5% 2a,f (-3,6) 4h4^> p(2)...' dq 4% 2b.''1.''+``` (-13,0) 3% ~2g~ (2,0) 3% iv```6s.....'' 22y````1.. (-3,0) 8% `24'zt`8''",
        mb,
    )
    assert len(oseq) == 10


def test_imac_inter_2025():
    oseq = parse_olan(
        "d'f 5% 44a,if- (-3,6) -4h2,4-^> -,ify...''22 (-1,0) -2% 1dq1 1j1> 3% ``1,24pb...34..+++ 3% ~`1,48``g~ (5,0) 3% ```9s....'ikz----~~ /-22iy2",
        mb,
    )
    assert len(oseq) == 10


def test_turn():
    fig: ParsedOlanFig = parse_olan("4j", mb)[0]

    assert fig.aresti.elements[0].kind == "roll"
    assert fig.aresti.elements[1].kind == "loop"
    assert fig.aresti.elements[1].kwargs["ke"] == approx(np.radians(30))

    assert fig.definition.eds[2].props["ke"] == approx(np.radians(30))


def test_tailslide():
    fig: ParsedOlanFig = parse_olan("~~.,3ita'3....~>", mb)
