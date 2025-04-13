# PyOlan

This WIP package contains a OLAN (One Letter Aerobatic Notation, https://openaero.net/) parser written in Python. The OLAN string is interpreted as a set of elements (loop, line, stallturn, spin etc). This is currently used by FCScore (https://www.flightcoach.org/fcscore/) to generate sequence definitions for automatic scoring.


Installation
```
    pip install -e .
```

Read the next figure from an olan string:
```
    from pyolan.figure_parser import OlanFig

    ostr = "/d'1 5% 2a,f (-3,6) 4h4^> p(2)...' dq"
    olan_array = ostr.split(" ")
    ofig, olan_array = OlanFig.take(olan_array)
```


parse an entire olan sequence, join the templates into one and plot:
```
    from flightdata import State
    from pyolan.parser import parse_olan

    olans: list[ParsedOlanFig] = parse_olan(
        "/d'1 5% 2a,f (-3,6) 4h4^> p(2)...' dq 4% 2b.''1.''+``` (-13,0) 3% ~2g~ (2,0) 3% iv```6s.....'' 22y````1.. (-3,0) 8% `24'zt`8''",
    )

    template = State.stack({fig.definition.info.short_name: fig.template for fig in olans}, "manoeuvre")

    template.plotlabels("manoeuvre").show()
```

TODO:
- Modify so it respects the correct olan figure directions (prefers turnarounds when there is ambiguity)
- Consider closer links with open-aero. Would it be better to read .seq files?
- Add K factor calculation
- Think about positioning the generated templates so they fit in the box better (probably better handled in the FlightAnalysis submodule).
- 