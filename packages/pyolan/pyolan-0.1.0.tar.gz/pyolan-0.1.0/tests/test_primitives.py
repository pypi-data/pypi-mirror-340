from pyolan.primitives import ofig_re



def test_ofig_re():
    assert ofig_re.search("23d2323").group(2) == "d"
    assert ofig_re.search("23id2323").group(2) == "id"
    assert ofig_re.search("d2323").group(2) == "d"
    assert ofig_re.search("212d").group(2) == "d"
    assert ofig_re.search("23rv2323") is None
    assert ofig_re.search("23a2323").group(2) == "a"
    assert ofig_re.search("23ia2323") is None

def test_ofig_re_2():
    assert ofig_re.search("-7is,fibB(9f)7").group(2) == "ibB"
