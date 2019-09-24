import pytest
from plotdarn.utils import antipode


def test_antipode():
    assert antipode(-72) == 108


def test_antipode_pos():
    assert antipode(72) == -108


def test_antipode_lat():
    assert antipode(20, axis='latitude') == -20


def test_antipode_lat_neg():
    assert antipode(-20, axis='latitude') == 20


def test_antipode_zero():
    assert antipode(0) == 180


def test_antipode_unknown_type():
    with pytest.raises(ValueError):
        antipode(20, axis='anything')
