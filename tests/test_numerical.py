from model import numerical
import pytest


@pytest.fixture
def parameters():
    return [0.00211, 0.246, 6.41, 1 / 13, 1 / 20.2, 0.04023596]


def test_numerical(parameters):
    assert round(numerical.calc_omega_s(parameters), 5) == 44.25733
