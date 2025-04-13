"""These primitives map the olan letters onto sequences of loops, lines, stallturns, tailslides and turns

The key outputs of this module are the olan_figs dictionary and the ofig_re regex.

The olan_figs dictionary maps each olan letter onto an instance of OFig.
    The OFig instance contains the elements (OlanEl instances) that make up the figure. 
    The sign of the loopamount value in each OlanEl is selected to form the most basic representation of the figure,
    so with no rolls and upright entry (but possibly requiring inverted exit).

The ofig_re regex combines all the olan letters and matches an olan expression that representing a figure.

"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


@dataclass
class OlanEl:
    kind: Literal["Loop", "Line", "Spin", "Stallturn", "Tailslide", "Turn"]
    loopamount: float
    canRoll: bool
    direction: int = None
    rolltype: Literal["oi", "io", "o", "i"] = "i"
    turnamount: float = 0


def lo(amount: float, canRoll: bool = False) -> OlanEl:
    return OlanEl("Loop", amount, canRoll)


def li() -> OlanEl:
    return OlanEl("Line", 0, True)


def sp() -> OlanEl:
    return OlanEl("Spin", -0.25, True)


def ts(direction: int = 1) -> OlanEl:
    return OlanEl("Tailslide", 0.5 * direction, False, direction)


def st() -> OlanEl:
    return OlanEl("Stallturn", 0.5, False)


def tu(rolltype: str, amount: float = 1 / 4) -> OlanEl:
    return OlanEl("Turn", 0, True, None, rolltype, amount)

@dataclass
class OFig:
    name: str
    short_name: str
    chars: str
    oels: list[OlanEl]
    invertable: bool = False
    turnable: int | None = None

    def pattern(self) -> str:
        if not self.invertable:
            return self.chars
        else:
            return f"{self.chars}|i{self.chars.replace('|', '|i')}"

    def loop_count(self) -> list[float]:
        """get the direction of each line, 0 upwind, 0.25 vertical, 0.5 downwind, 0.75 vdown"""
        angles = []
        for el in self.oels:
            if isinstance(el, lo):
                angles.append(el.amount)
            else:
                if len(angles):
                    angles.append(angles[-1])
                else:
                    angles.append(0)
        return [a % 1 for a in angles]


def create_ofig_dict(ofigs: list[OFig]) -> dict[str, OFig]:
    figs = {}
    for f in ofigs:
        if "|" not in f.chars:
            figs[f.chars] = f
        else:
            for c in f.chars.split("|"):
                figs[c] = f
    return figs



olan_figs = create_ofig_dict(
    [
        OFig("45 Degree Line", "line", "d", [lo(1 / 8), li(), lo(-1 / 8)], True, -1),
        OFig("Vertical Line", "vline", "v", [lo(1 / 4), li(), lo(-1 / 4)], True, -1),
        OFig("Figure Z", "Z", "z", [lo(3 / 8), li(), lo(-3 / 8)], True, -1),
        OFig(
            "Sharks Tooth",
            "sTooth",
            "t",
            [lo(1 / 8), li(), lo(-3 / 8), li(), lo(1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Reverse Sharks Tooth",
            "rsTooth",
            "k",
            [lo(1 / 4), li(), lo(-3 / 8), li(), lo(1 / 8)],
            True,
            2,
        ),
        OFig(
            "Z Sharks Tooth",
            "zsTooth",
            "zt",
            [lo(3 / 8), li(), lo(3 / 8), li(), lo(1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Reverse Z Sharks Tooth",
            "rzsTooth",
            "kz",
            [lo(1 / 4), li(), lo(3 / 8), li(), lo(3 / 8)],
            True,
            -1,
        ),
        OFig("Split S", "spl", "a", [li(), lo(-1 / 2), li()]),
        OFig("Immelman", "imm", "m", [li(), lo(1 / 2), li()]),
        OFig("Loop", "loop", "o", [lo(1, True)], True),
        OFig(
            "Reversing Loop",
            "rloop",
            "ao",
            [li(), lo(3 / 4, True), lo(-1 / 4), li()],
            True,
        ),
        OFig(
            "Square Loop",
            "sql",
            "qo",
            [lo(1 / 4), li(), lo(1 / 4), li(), lo(1 / 4), li(), lo(1 / 4)],
            True,
        ),
        OFig(
            "Square on corner",
            "sqc",
            "dq",
            [
                lo(1 / 8),
                li(),
                lo(1 / 4),
                li(),
                lo(1 / 4),
                li(),
                lo(1 / 4),
                li(),
                lo(1 / 8),
            ],
            True,
        ),
        OFig(
            "8 Sided Loop",
            "loop8",
            "qq",
            [
                lo(1 / 8),
                li(),
                lo(1 / 8),
                li(),
                lo(1 / 8),
                li(),
                lo(1 / 8),
                li(),
                lo(1 / 8),
                li(),
                lo(1 / 8),
                li(),
                lo(1 / 8),
                li(),
                lo(1 / 8),
            ],
            True,
        ),
        OFig("Half Cuban", "hc", "c", [li(), lo(5 / 8), li(), lo(-1 / 8)], True),
        OFig(
            "Reverse Half Cuban", "rhc", "rc", [lo(1 / 8), li(), lo(-5 / 8), li()], True
        ),
        OFig(
            "Goldfish", "gf", "g", [lo(1 / 8), li(), lo(-3 / 4), li(), lo(1 / 8)], True
        ),
        OFig(
            "Horisontal S", "hS", "ac", [li(), lo(5 / 8), li(), lo(-5 / 8), li()], True
        ),
        OFig("Figure P", "P", "p", [li(), lo(3 / 4, True), li(), lo(1 / 4)], True, -1),
        OFig(
            "Reverser Figure P",
            "rP",
            "rp",
            [lo(1 / 4), li(), lo(3 / 4, True), li()],
            True,
            -2,
        ),
        OFig("Q Loop", "Ql", "q", [li(), lo(7 / 8, True), li(), lo(1 / 8)], True),
        OFig(
            "reverse Q Loop",
            "rQloop",
            "rq",
            [lo(1 / 4), lo(1 / 8), li(), lo(7 / 8, True), li()],
            True,
        ),
        OFig(
            "Teardrop",
            "tdrop",
            "y",
            [lo(1 / 8), li(), lo(5 / 8), li(), lo(1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Reverse Teardrop",
            "rtdrop",
            "ry",
            [lo(1 / 4), li(), lo(5 / 8), li(), lo(1 / 8)],
            True,
            2,
        ),
        OFig(
            "Humpty Bump",
            "hump",
            "b",
            [lo(1 / 4), li(), lo(1 / 2), li(), lo(1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Push Humpty",
            "phump",
            "pb",
            [lo(1 / 4), li(), lo(-1 / 2), li(), lo(1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Lay Down Humpty",
            "lhump",
            "db",
            [lo(1 / 8), li(), lo(1 / 2), li(), lo(-1 / 8)],
            True,
        ),
        OFig(
            "Reverse Lay Down Humpty",
            "rlhump",
            "rdb",
            [lo(1 / 8), li(), lo(-1 / 2), li(), lo(-1 / 8)],
            True,
        ),
        OFig(
            "Double Humpty",
            "dhump",
            "bb|bB|Bb",
            [lo(1 / 4), li(), lo(1 / 2), li(), lo(1 / 2), li(), lo(-1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Push Pull Double Humpty",
            "dhump",
            "pbb|pbB|pBb",
            [lo(1 / 4), li(), lo(-1 / 2), li(), lo(1 / 2), li(), lo(-1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Pull Push Double Humpty",
            "dhump",
            "bpb|bpB|Bpb",
            [lo(1 / 4), li(), lo(1 / 2), li(), lo(-1 / 2), li(), lo(-1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Push Push Double Humpty",
            "dhump",
            "pbpb|pbpB|pBpb",
            [lo(1 / 4), li(), lo(-1 / 2), li(), lo(-1 / 2), li(), lo(-1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Stallturn", "sT", "h", [lo(1 / 4), li(), st(), li(), lo(1 / 4)], False, -1
        ),
        OFig(
            "45 Entry Stallturn",
            "st",
            "dh",
            [lo(1 / 8), li(), lo(1 / 8), li(), st(), li(), lo(1 / 4)],
            False,
            -1,
        ),
        OFig(
            "45 Exit Stallturn",
            "st",
            "hd",
            [lo(1 / 4), li(), st(), li(), lo(1 / 8), li(), lo(1 / 8)],
        ),
        OFig(
            "45 Entry and Exit Stallturn",
            "st",
            "dhd",
            [lo(1 / 8), li(), lo(1 / 8), li(), st(), li(), lo(1 / 8), li(), lo(1 / 8)],
        ),
        OFig(
            "Wheels Down Tailslide",
            "tslide",
            "ta",
            [lo(1 / 4), li(), ts(), li(), lo(1 / 4)],
            False,
            -1,
        ),
        OFig(
            "Canopy Down Tailslide",
            "tslide",
            "ita",
            [lo(1 / 4), li(), ts(-1), li(), lo(1 / 4)],
            False,
            -1,
        ),
        OFig(
            "Figure N",
            "N",
            "n",
            [lo(1 / 4), li(), lo(3 / 8), li(), lo(-3 / 8), li(), lo(-1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Push Figure N",
            "pushN",
            "pn",
            [lo(1 / 4), li(), lo(-3 / 8), li(), lo(3 / 8), li(), lo(-1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Bow Tie",
            "bow",
            "w",
            [lo(1 / 8), li(), lo(-3 / 8), li(), lo(3 / 8), li(), lo(-1 / 8)],
            True,
            4,
        ),
        OFig(
            "Super 8",
            "S8",
            "gg",
            [lo(1 / 8), li(), lo(-3 / 4), li(), lo(3 / 4), li(), lo(-1 / 8)],
            True,
        ),
        OFig("Figure S", "S", "mm", [lo(1 / 2), lo(-1 / 2)], True),
        OFig("Vertical 8", "v8", "oo", [lo(1 / 2), lo(-1), lo(1 / 2)], True),
        OFig("Vertical 8", "v8", "ooo", [lo(1), lo(-1)], True),
        OFig(
            "Lay Down Humpty",
            "lHump",
            "zb",
            [lo(3 / 8), li(), lo(1 / 2), li(), lo(1 / 8)],
            True,
        ),
        OFig(
            "Lay Down Humpty",
            "lHump",
            "rzb",
            [lo(3 / 8), li(), lo(-1 / 2), li(), lo(1 / 8)],
            True,
        ),
        OFig(
            "Lay Down Humpty",
            "lHump",
            "bz",
            [lo(1 / 8), li(), lo(1 / 2), li(), lo(3 / 8)],
            True,
        ),
        OFig(
            "Lay Down Humpty",
            "lHump",
            "rbz",
            [lo(1 / 8), li(), lo(-1 / 2), li(), lo(3 / 8)],
            True,
        ),
        OFig(
            "Teardrop",
            "tdrop",
            "zy",
            [lo(3 / 8), li(), lo(-5 / 8), li(), lo(1 / 4)],
            True,
            -1,
        ),
        OFig(
            "Teardrop",
            "tdrop",
            "ryz",
            [lo(1 / 4), li(), lo(-5 / 8), li(), lo(3 / 8)],
            True,
            2,
        ),
        OFig("Turn", "turn", "j", [tu("i", 1 / 4)]),
        OFig("Rolling Turn", "rturn", "jo", [tu("o", 1 / 4)]),
        OFig("Rolling Turn", "rturn", "joi", [tu("oi", 1 / 4)]),
        OFig("Rolling Turn", "rturn", "jio", [tu("io", 1 / 4)]),
        OFig("Rev Loop b", "rloopb", "pp", [li(), lo(1/4), lo(-1/2, True), li(), lo(1/4)], True, -1), 
        OFig("R Rev Loop b", "rrloopb", "rpp", [lo(1/4), li(), lo(-1/2, True), lo(1/4), li()], True, 2 ),
    ]
)


ofig_re = re.compile(
    rf"([^a-zA-Z]|if|f|s|^)({'|'.join(f'{f.pattern()}' for f in olan_figs.values())})([^a-zA-Z]|if|f|s|$)"
)
