import lmu_wta

import numpy as np
import pytest


@pytest.mark.parametrize("neuron_type", [lmu_wta.Linear(),
                                         lmu_wta.RectifiedLinear(),
                                         lmu_wta.Sigmoid(),
                                         lmu_wta.Tanh(),
                                         lmu_wta.LIFRate()])
def test_generate_encoders(neuron_type):
    N = 50
    block = lmu_wta.LMUWTABlock(q=1, theta=1, size_in=1,
                                n_neurons=N, size_out=N,
                                neuron_type=neuron_type)

    lmu_wta.generate_encoders(block, output_range=(150, 200))

    x = np.linspace(-1, 1, 80).reshape((80, 1))

    J = block.E.dot(x.T) + block.bias[:, None]

    A = block.neuron_type.step(J)

    assert(np.max(A) <= 200)
    assert(np.all(np.maximum(A[:, 0], A[:, -1]) >= 150))
