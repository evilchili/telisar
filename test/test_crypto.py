import pytest
from telisar import crypto

@pytest.fixture
def c():
    return crypto.ElethisCipher()

@pytest.mark.parametrize('key, expected', [
    ('00', 'a'),
    ('01', 'b'),
    ('09', 'j'),
    ('99', '1'),
])
def test_forward(c, key, expected):
    assert c.forward(key) == expected

def test_reverse(c):
    for y, row in enumerate(c._table):
        for x, col in enumerate(row):
            num = int(f'{y}{x}')
            assert c.reverse(col) in (num, num - len(c.alphabet), num - 2 * len(c.alphabet))

@pytest.mark.parametrize('primer, plaintext, expected', [
    ('keen',
     'noobhammer',
     [23, 18, 18, 14, 20, 14, 26, 13, 11, 17]),
    ('brescht',
     'keep sons whereabouts hidden',
     [11, 21, 8, 33, 20, 21, 32, 28,
      26, 11, 19, 35, 18, 13, 19, 36,
      27, 23, 35, 11, 8, 4, 17, 24, 32]),
])
def test_encrypt(c, primer, plaintext, expected):
    encrypted = c.encrypt(primer, plaintext)
    assert encrypted == expected


@pytest.mark.parametrize('primer, plaintext, expected', [
    ('primer',
     'string to encrypt',
     'S T R I N    G T O E N    C R Y P T'),
])
def test_encrypt_decrypt(c, primer, plaintext, expected):
    encrypted = ' '.join([str(x) for x in c.encrypt(primer, plaintext)])
    assert ''.join(c.pretty_decrypt(primer, encrypted)) == expected

@pytest.mark.parametrize('primer, msg, plaintext', [
    ('Keen', '23 18 18 14 20 14 26 13 11 17', 'NOOBHAMMER'),
])
def test_decrypt(c, primer, msg, plaintext):
    assert ''.join(c.decrypt(primer, msg)) == plaintext.upper()


@pytest.mark.parametrize('primer, msg, expected', [
    ('brescht',
     'keep sons whereabouts hidden',
     '011 021 008 033 020    021 032 028 026 011    019 035 018 013 019\n'
     '036 027 023 035 011    008 004 017 024 032'),
])
def test_pretty_encrypt(c, primer, msg, expected):
    assert c.pretty_encrypt(primer, msg) == expected
