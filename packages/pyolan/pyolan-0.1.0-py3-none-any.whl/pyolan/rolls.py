"""This module handles olan roll strings.
The ORoll class handles a single element, either a roll, snap or spin. This could be a single point of a point roll.
The OlanRoll class handles the entire combination, so all the points of a point roll.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

import numpy as np
import schemas.positioning as p


# Map olan roll strings onto
olan_rolls = {k: np.array(v) for k, v in {
    "1": [1],
    "2": [0.5],
    "22": [0.5] * 2,
    "32": [0.5] * 3,
    "42": [0.5] * 4,
    "3": [0.75],
    "4": [0.25],
    "24": [0.25] * 2,
    "34": [0.25] * 3,
    "44": [0.25] * 4,
    "54": [0.25] * 5,
    "64": [0.25] * 6,
    "74": [0.25] * 7,
    "84": [0.25] * 8,
    "5": [1.25],
    "6": [1.5],
    "7": [7 / 4],
    "8": [0.125] * 2,
    "48": [0.125] * 4,
    "88": [0.125] * 8,
    "9": [2],
}.items()}


oroll_re = re.compile(r"([1-9]|[1-9][2|4|8]|^)([fis]|$)([fs]|$)")


@dataclass
class ORoll:
    kind: Literal["roll", "snap", "spin"]
    turns: float
    negative: bool = False

    def __repr__(self):
        return f"{self.turns}{'i' if self.negative else ''}{dict(roll='', snap='f', spin='s')[self.kind]}"

    @property
    def pfc_char(self):
        return dict(roll="r", snap="s", spin="-")[self.kind]


def ro(turns: float) -> ORoll:
    return ORoll("roll", turns)


def sn(turns: float, negative: bool) -> ORoll:
    return ORoll("snap", turns, negative)


def spi(turns: float, negative: bool) -> ORoll:
    return ORoll("spin", turns, negative)


def create_roll(rollchars: str, turns: float) -> ORoll:
    match rollchars:
        case "f":
            return sn(turns, False)
        case "if":
            return sn(turns, True)
        case "s":
            return spi(turns, False)
        case "is":
            return spi(turns, True)
        case _:
            return ro(turns)


@dataclass
class OlanRoll:
    rawroll: str
    roll_arr: list[ORoll]

    def turns(self) -> list[float]:
        return [r.turns for r in self.roll_arr]

    def total(self) -> float:
        return sum(self.turns())

    def angles(self) -> list[float]:
        res = p.r(self.turns())
        return res if len(res) > 1 else res[0]

    def pfc_roll(self) -> list[float] | str | float:
        roll_arr = np.array(self.turns())
        if (
            len(roll_arr) > 1
            and np.all(roll_arr == roll_arr[0])
            and np.all(np.array([r.kind for r in self.roll_arr]) == "roll")
        ):
            return f"{len(roll_arr)}x{int(1 / roll_arr[0])}"
        else:
            return self.angles()

    def rolltypes(self) -> list[str]:
        rtypes = "".join([r.pfc_char for r in self.roll_arr])
        if len(rtypes) * "r" == rtypes:
            return "roll"
        elif len(rtypes) * "s" == rtypes:
            return "snap"
        elif len(rtypes) * "-" == rtypes:
            return "spin"
        else:
            return rtypes

    def parse(data: str) -> OlanRoll | None:
        rolls = []
        rollarr = [";"] + re.split(r"(;|,)", re.sub(r"^(;|,)", "", data))
        last_direction = 1
        for direction, roll in zip(rollarr[::2], rollarr[1::2]):
            res = oroll_re.search(roll)
            if not res:
                break
            else:
                res = res.group()
            olan_roll_str = re.search(r"\d+", res)
            if olan_roll_str:
                new_rolls = olan_rolls[olan_roll_str.group()]
            else:
                new_rolls = [1]

            roll_chars = None
            res = re.search(r"(f|if|s|is)", res)
            if res:
                roll_chars = res.group()

            last_direction = last_direction if direction == ";" else -last_direction
            rolls = rolls + [
                create_roll(roll_chars, r * last_direction) for r in new_rolls
            ]
        if len(data):
            return OlanRoll(data, rolls)
