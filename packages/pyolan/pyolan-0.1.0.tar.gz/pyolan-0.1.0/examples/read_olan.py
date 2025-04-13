
from flightdata import State
from pyolan.parser import parse_olan


olan = parse_olan(
    "/d'1 5% 2a,f (-3,6) 4h4^> p(2)...' dq 4% 2b.''1.''+``` (-13,0) 3% ~2g~ (2,0) 3% iv```6s.....'' 22y````1.. (-3,0) 8% `24'zt`8''",
)


template = State.stack({fig.definition.info.short_name: fig.template for fig in olan}, "manoeuvre")

template.plotlabels("manoeuvre").show()