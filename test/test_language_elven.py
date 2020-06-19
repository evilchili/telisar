from telisar.languages.elven import Elven


def test_ara_am_akiir():
    elven = Elven()
    assert elven.is_valid_word('ara')
    assert elven.is_valid_word('am')
    assert elven.is_valid_word('akiir')
