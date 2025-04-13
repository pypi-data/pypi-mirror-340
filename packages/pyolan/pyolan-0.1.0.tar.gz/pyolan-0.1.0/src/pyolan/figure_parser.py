"""This module handles an entire olan figure.

An instance of OlanFig contains all the information relating to a figure from an olan string. 
This includes the original string and the important parts of it, the OFig primitive and all the
information on the rolls.

The OlanFig.take constructor will read the next figure from an olan array (an olan sequence split on 
spaces) return the OlanFig instance and the remaining olan array.

The create_elements method will create the pyflightcoach principal elements for the figure.
"""

from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Tuple


import numpy as np
import schemas.positioning as p
from loguru import logger
from schemas import aresti as a, maninfomaker

from .primitives import OFig, sp, li, lo, tu, ofig_re, olan_figs
from .rolls import OlanRoll, ro

from .drawing import re_drawing, re_draw


@dataclass
class OlanFig:
    draw: list[str]
    rawfig: str
    fig: OFig
    inverted: bool
    prefix: OlanRoll | None
    suffix: list[OlanRoll]
    final: OlanRoll | None
    entry: p.Orientation
    exit: p.Orientation
    entry_direction: p.Direction = p.Direction.UPWIND
    exit_downwind: bool = (
        False  ## only used if there is a 1/4 roll on vertical line, otherwise infer
    )

    def __len__(self):
        return len(self.fig.oels)

    @staticmethod
    def take(data: list[str]) -> Tuple[OlanFig, list[str]]:
        """read one olan figure from an array of strings, return figure and the remaining array"""
        draw = []
        for i, d in enumerate(data):
            if re_drawing.match(d):
                draw.append(d)
            else:
                rawfig = re_draw.sub("", d)
                fig_chars = None

                # check if it is a figure
                res = ofig_re.search(d)
                if res and res.group(2):
                    fig_chars = res.group(2)
                    ofig = olan_figs[res.group(2).lstrip("i")]
                    if res.group(2).startswith("i") and not ofig.invertable:
                        ofig = olan_figs[res.group(2)]
                if not fig_chars:
                    # check if it is a spin
                    res = re.search(r"([^a-z]|^)(s|is)([^a-z]|$)", rawfig)
                    if res and res.group(2):
                        fig_chars = res.group(2)
                        ofig = OFig(
                            "Spin", "sp", "", [sp(), li(), lo(1 / 4)], False, -1
                        )
                        if not rawfig.split(fig_chars)[0]:
                            rawfig = "1s"

                if fig_chars:
                    _prefix, _suffix = rawfig.split(fig_chars)

                if not fig_chars:
                    # check if its a roll
                    roll = OlanRoll.parse(rawfig)
                    if roll and len(roll.roll_arr):
                        fig_chars = "r"
                        ofig = OFig("Roll", "roll", "r", [li()])
                        _prefix = ""
                        _suffix = rawfig

                if fig_chars:
                    break
                else:
                    logger.warning(
                        "Unknown olan entry, assuming it is a drawing command", d
                    )
                    draw.append(d)
        else:
            raise Exception("No olan figure found in data")

        # Special handling for rolling circles
        if re.match(r"(j|ji|jo|jio|joi)", fig_chars):
            ofig = OFig(
                "turn",
                "turn",
                fig_chars,
                [tu(fig_chars.split("j")[1] or "i", int(_prefix.strip("-") or 1) / 4)],
            )
            prefix = None
            suffix = []

            rolls = int(_suffix.strip("-")) if _suffix.strip("-") else 0

            suff_rolls = []
            if rolls > 0:
                rolls = (rolls * 10 if rolls < 10 else rolls) / 10

                sign = 1 if ofig.chars in ["j", "ji", "jio"] else -1

                if ofig.chars in ["joi", "jio"]:
                    swapper = -1
                    for _ in range(int(rolls // 1)):
                        suff_rolls.append(ro(sign))
                        sign = sign * swapper
                else:
                    suff_rolls = [ro(sign * rolls)]
                if rolls % 1:
                    suff_rolls.append(ro(rolls % 1))
                final = OlanRoll(_suffix, suff_rolls)
            else:
                final = None

        else:
            prefix = OlanRoll.parse(_prefix.lstrip("-").split(")")[-1])
            suffix = [OlanRoll.parse(r) for r in re.findall(r"\((.*?)\)", _suffix)]
            final = OlanRoll.parse(_suffix.split(")")[-1].rstrip("-"))

        entry_direction = p.Direction.UPWIND
        for dr in draw:
            if dr in ["ej", "eja"]:
                entry_direction = p.Direction.CROSS
            elif dr == "ed":
                entry_direction = p.Direction.DOWNWIND
            elif dr == "eu":
                entry_direction = p.Direction.UPWIND

        return OlanFig(
            draw,
            rawfig,
            ofig,
            fig_chars.startswith("i") and ofig.invertable,
            prefix,
            suffix,
            final,
            p.Orientation.INVERTED if rawfig.startswith("-") else p.Orientation.UPRIGHT,
            p.Orientation.INVERTED if rawfig.endswith("-") else p.Orientation.UPRIGHT,
            entry_direction,
            re.match(r">", d) is not None,
        ), data[i + 1 :]

    def create_info(self):
        return maninfomaker(
            "olan figure",
            "ofig",
            10,
            p.BoxLocation(
                height=p.Height.MID,
                direction=p.Direction.UPWIND,
                orientation=self.entry,
            ),
            p.BoxLocation(height=p.Height.MID),
        )

    def element_rolls(self) -> list[OlanRoll | None]:
        # n==4: p fig (s0) (s1) f
        # n==3: p fig (s0) f
        # n==2: p fig f
        # n==1: fig f
        roll_positions = [i for i, el in enumerate(self.fig.oels) if el.canRoll]
        nrolls = len(roll_positions)
        rolls = [None for _ in self.fig.oels]

        def safe_get_item(arr: list, i: int):
            try:
                return arr[i]
            except IndexError:
                return None

        if nrolls == 1:
            rolls[roll_positions[0]] = self.final
        elif nrolls == 2:
            rolls[roll_positions[0]] = self.prefix
            rolls[roll_positions[1]] = self.final
        elif nrolls == 3:
            rolls[roll_positions[0]] = self.prefix
            rolls[roll_positions[1]] = safe_get_item(self.suffix, 0)
            rolls[roll_positions[2]] = self.final
        elif nrolls == 4:
            rolls[roll_positions[0]] = self.prefix
            rolls[roll_positions[1]] = safe_get_item(self.suffix, 0)
            rolls[roll_positions[2]] = safe_get_item(self.suffix, 1)
            rolls[roll_positions[3]] = self.final
        return rolls

    def can_swap_exit(self) -> bool:
        if all([el.loopamount == 0 for el in self.fig.oels]):
            return False
        roll_totals = np.array([r.total() if r else 0 for r in self.element_rolls()])

        loops = np.array([e.loopamount for e in self.fig.oels])

        direction = np.concatenate((np.array([0]), (loops.cumsum() % 1)[:-1]))
        is_vertical = (direction == 0.25) | (direction == 0.75)

        return is_vertical & (roll_totals % 1 == 0.25)

    def loop_amounts(self, element_rolls: list[OlanRoll]) -> list[float]:
        if all([el.loopamount == 0 for el in self.fig.oels]):
            return np.zeros(len(self.fig.oels))

        def swap(test):
            """returns -1 for false and 1 for true"""
            return np.where(test, 1, -1)

        roll_totals = np.array([r.total() if r else 0 for r in element_rolls])

        loops = np.array([e.loopamount for e in self.fig.oels])

        direction = np.concatenate((np.array([0]), (loops.cumsum() % 1)[:-1]))
        is_vertical = (direction == 0.25) | (direction == 0.75)

        if self.inverted:
            loops = loops * np.where(
                np.logical_not(is_vertical), swap(not self.inverted), 1
            )
            direction = np.concatenate((np.array([0]), (loops.cumsum() % 1)[:-1]))

        # If exit is inverted all loops before the first vertical line are swapped
        if sum(is_vertical) > 0:
            entry_swap = np.where(
                np.arange(len(self)) <= is_vertical.argmax(),
                swap(self.entry == p.Orientation.UPRIGHT),
                1,
            )
        else:
            entry_swap = np.ones(len(self)) * swap(self.entry == p.Orientation.UPRIGHT)

        # At half roll increments the loop directions are swapped
        # if the line is vertical the swap is cancelled
        roll_swap = []
        is_swapped = 1
        for hrp, isvert in zip(np.where(roll_totals % 1 == 0.5, 0.5, 0), is_vertical):
            if hrp == 0.5:
                is_swapped = -is_swapped
            if isvert:
                is_swapped = 1
            roll_swap.append(is_swapped)

        loops = loops * entry_swap * np.array(roll_swap)

        if self.fig.turnable is not None:
            # reverse all elements after the turnable element to make
            # the exit attitude correct.

            turn_index = (
                self.fig.turnable
                if self.fig.turnable > 0
                else len(loops) + self.fig.turnable
            )

            # infer exit attitude - if climbing then pull to inverted, push to upright
            # if diving pull to upright, push to inverted
            pos_exit_direction = -swap(direction[-2] < 0.5)

            exit_loop_direction = (
                swap(self.exit == p.Orientation.UPRIGHT) * pos_exit_direction
            )

            turn_swap = np.where(
                np.arange(len(loops)) >= turn_index,
                swap(np.sign(loops[-1]) == exit_loop_direction),
                1,
            )
            loops = loops * turn_swap

        return loops

    def create_elements(self) -> list[a.PE]:
        pes: list[a.PE] = []

        rolls = self.element_rolls()
        loops = self.loop_amounts(rolls)

        for i, el in enumerate(self.fig.oels):
            match el.kind:
                case "Loop":
                    pes.append(
                        a.loop(
                            p.r(loops[i]),
                            **(
                                dict(
                                    rolls=rolls[i].pfc_roll(),
                                    rolltypes=rolls[i].rolltypes(),
                                    rollangle=np.radians(90),
                                )
                                if rolls[i]
                                else {}
                            ),
                        )
                    )
                case "Line":
                    if rolls[i] and len(rolls[i].roll_arr):
                        if rolls[i].roll_arr[0].kind == "spin":
                            # If there is a spin on the line we need to delete the previous radius and make two elements.
                            assert pes[-1].kind == "loop"
                            pes.pop(-1)
                            pes.append(a.spin(rolls[i].roll_arr[0].turns * 2 * np.pi))

                            if len(rolls[i].roll_arr) > 1:
                                # TODO need to know if its F3A or IMAC here
                                pes.append(a.line(length=30))
                                pes.append(
                                    a.roll(
                                        rolls[i].angles()[1:],
                                        rolltypes=rolls[i].rolltypes()[1:],
                                        padded=False,
                                    )
                                )
                                pes.append(a.line(length=50))
                            else:
                                pes.append(a.line())
                            pass
                        else:
                            pes.append(
                                a.roll(
                                    rolls[i].pfc_roll(),
                                    rolltypes=rolls[i].rolltypes(),
                                    padded=i > 0 and i < len(self.fig.oels) - 1,
                                )
                            )
                    elif i > 0 and i < len(self.fig.oels) - 1:
                        pes.append(a.line())
                case "Stallturn":
                    pes.append(a.stallturn())
                case "Spin":
                    pes.append(a.spin(rolls[i].roll_arr[0].turns * 2 * np.pi))
                case "Turn":
                    if self.final:
                        pes.append(
                            a.loop(
                                el.turnamount * np.pi * 2,
                                rolls=self.final.angles(),
                                ke=np.pi / 2,
                            )
                        )
                    else:
                        pes.append(a.roll(np.radians(60), padded=False))
                        pes.append(a.loop(el.turnamount * 2 * np.pi, ke=np.radians(30)))
                        pes.append(a.roll(np.radians(-60), padded=False))
                case "Tailslide":
                    pes.append(a.tailslide(el.direction))
                case _:
                    raise NotImplementedError(f"cant do {el.__class__.__name__} yet")
        return pes

    def create_maninfo(
        self,
        short_name: str = None,
        entry_direction: p.Direction = None,
        exit_direction: p.Direction = None,
    ) -> a.ManInfo:
        return maninfomaker(
            self.fig.name,
            short_name or self.fig.short_name,
            10,
            p.Position.CENTRE if entry_direction == exit_direction else p.Position.END,
            p.BoxLocation(
                direction=entry_direction
                if entry_direction is not None
                else self.entry_direction,
                orientation=self.entry,
            ),
            p.BoxLocation(orientation=self.exit),
        )
