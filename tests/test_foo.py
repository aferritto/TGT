import pytest
from tgt import foo


def test_hello_world():
    assert foo.hello_world(0) == '00'
    assert foo.hello_world(7) == '77'
