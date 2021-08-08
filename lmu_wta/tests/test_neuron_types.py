import lmu_wta

import pytest
import numpy as np


@pytest.mark.parametrize("neuron_type", [lmu_wta.Linear(),
                                         lmu_wta.RectifiedLinear(),
                                         lmu_wta.Sigmoid(),
                                         lmu_wta.Tanh(),
                                         lmu_wta.LIFRate()])
def test_neuron_types(neuron_type):
    J = np.linspace(-1, 10, 100)
    r = neuron_type.step(J)

    # check if the neuron is monotonic
    assert np.all(np.diff(r) >= 0)

    # check if the rate_to_current function works for
    #  any non-zero output rate
    assert np.allclose(J[r > 0], neuron_type.rate_to_current(r[r > 0]))

    # check that there is an intercept value
    assert neuron_type.intercept() is not None


def test_unimplemented_neuron_type():
    n = lmu_wta.neuron_types.NeuronType()
    with pytest.raises(NotImplementedError):
        n.step(0)
    with pytest.raises(NotImplementedError):
        n.rate_to_current(0)
    with pytest.raises(NotImplementedError):
        n.intercept()
