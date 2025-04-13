"""Drawing commands aren't used, but they need to be recognised so as not to process them as a figure"""
import re


re_dpre = dict(
    entry=r"^(ed|ej|eja|eu)$",
    subsequence=r"^//$",
    move=r"^(\[|\()-?‑?\d+,-?‑?\d+(\]|\))$",
    scale=r"^\d+%$",
    offset=r"^(^|\d+)\>$",
    cross_switch=r"^\^$",
    y_direction=r"^/$",
    line_length=r"^[~+/]$",
    comment=r"^\".+\"$",
    freeuk=r"^@[A-L]$",
)

# Drawing commands that may be found on their own:
re_drawing = re.compile(rf"({'|'.join(re_dpre.values())})")

# Drawing commands within a figure:
re_draw = re.compile(r"[>/~+^'`.]")