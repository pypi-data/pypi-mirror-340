from __future__ import annotations

from dataclasses import dataclass

import geometry as g
import numpy as np
import schemas.positioning as p
from flightanalysis import ManDef, Manoeuvre
from flightanalysis.builders.manbuilder import ManBuilder
from flightanalysis.builders.example.manbuilder import mb as exampe_mb
from flightdata import State
from schemas import aresti as a

from .figure_parser import OlanFig


@dataclass
class ParsedOlanFig:
    olan: OlanFig
    aresti: a.Figure
    definition: ManDef
    manoeuvre: Manoeuvre
    template: State

    @property
    def short_name(self):
        return self.olan.short_name


def parse_olan(
    data: str, mb: ManBuilder=None, wind: p.Heading = p.Heading.LTOR
) -> list[ParsedOlanFig]:
    mb = exampe_mb if mb is None else mb    
    data = data.split(" ")
    figs: list[ParsedOlanFig] = []
    itrans = None

    while data:
        olanfig, data = OlanFig.take(data)

        # make sure short_name is unique
        _suffix = ""
        while f"{olanfig.fig.short_name}{_suffix}" in [
            f.olan.fig.short_name for f in figs
        ]:
            _suffix = int(_suffix) + 1 if _suffix else "2"

        # Take the initial heading from the end of the previous figure if possible
        # if not infer it from the wind direction and the draw parameters (default to upwind)
        # TODO this should prefer a turnaround if possible
        entry_heading = (
            p.Heading.infer(itrans.att.bearing()[-1])
            if itrans
            else olanfig.entry_direction.wind_swap_heading(wind.reverse())
        )

        # need to get the direction (upwind / downwind / cross) from the heading and the wind
        entry_direction = p.Direction.parse_heading(entry_heading, wind)

        arestifig = a.Figure(
            info=olanfig.create_maninfo(
                f"{olanfig.fig.short_name}{_suffix}", entry_direction, None
            ),
            elements=olanfig.create_elements(),
            ndmps={},  # TODO consider some roll direction linking and also unusual inter criteria.
        )

        mdef = mb.create_mdef(arestifig)
        man = mdef.create()

        # if itrans cannot be picked up from the previous manouevre assume the olan figure is correct
        if not itrans:
            itrans = g.Transformation(g.Euler(olanfig.entry, 0, entry_heading), g.P0())

        tp = State.stack(man.create_template(itrans), "element")

        if np.any(olanfig.can_swap_exit()) and p.Heading.infer(
            tp.att.bearing()[-1]
        ) in [
            p.Heading.RTOL,
            p.Heading.LTOR,
        ]:
            # If there is a 1/4 roll on a vertical line make sure the next manoeuvre
            # starts in the correct direction
            itrans = g.Transformation(
                g.Euler(
                    olanfig.entry,
                    0,
                    p.Heading.LTOR if olanfig.exit_downwind else p.Heading.RTOL,
                )
            )

        else:
            # if not just take the exit direction from the end of this one
            itrans = g.Transformation(tp.att[-1], g.P0())

        # update maninfo with the correct centre now that we know the exit direction
        arestifig.info = olanfig.create_maninfo(
            f"{olanfig.fig.short_name}{_suffix}",
            entry_direction,
            p.Direction.parse_heading(tp.att.bearing()[-1], wind),
        )

        figs.append(ParsedOlanFig(olanfig, arestifig, mdef, man, tp))

    return figs
