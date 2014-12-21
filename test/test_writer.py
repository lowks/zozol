import os.path
from zozol import encode_ber, encode_ber_tag, base as asn1, markers as m
from zozol.schemas.pkcs7_dstszi import ContentInfo

def here(fname):
    dirname, _ = os.path.split(__file__)
    return os.path.join(dirname, fname)


def test_encode_ocsttr():
    data = encode_ber_tag(0x04, 0, bytearray('123'), bytearray())
    assert data == '0403313233'.decode('hex')


def test_encode_ocsttr_long():
    expect_hex = '0481803333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333'
    data = encode_ber_tag(0x04, 0, bytearray('3' * 128), bytearray())
    assert data == expect_hex.decode('hex')


def test_encode_ocsttr_long2():
    expect_hex = '048201013333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333'
    data = encode_ber_tag(0x04, 0, bytearray('3' * 257), bytearray())
    assert data == expect_hex.decode('hex')


def test_encode_seq():
    seq = (
        (0x30, 0, (
            (0x04, 0, '123'),
            (0, 2, '999'),
        ))
    )
    data = encode_ber((seq,))
    assert len(data) == 2 + 2 + 2 + 3 + 3
    assert data[0] == 0x30
    assert data[1] == 2 + 2 + 3 + 3
    assert data[2] == 0x04
    assert data[3] == 3
    assert str(data[4:7]) == '123'
    assert data[7] == 0x80
    assert data[8] == 3
    assert str(data[9:12]) == '999'


def test_encode_schema():
    class X(asn1.Seq):
        fields = [
            ('b', asn1.OctStr),
            ('c', asn1.Int),
        ]

    x = X()
    x.b = asn1.OctStr(value='123')
    x.c = asn1.Int(value=2227)

    data = x.to_stream(encode_fn=encode_ber)
    assert str(data) == str.decode('30090403313233020208b3', 'hex')
