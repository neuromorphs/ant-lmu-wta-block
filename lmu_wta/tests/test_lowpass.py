from lmu_wta import LMUWTABlock
import numpy as np
import nengo


def test_basic_lowpass():
    lmu = LMUWTABlock(q=1, theta=0.1, n_neurons=1, size_in=1, size_out=1)
    lmu.E[:] = 1
    lmu.D[:] = 1

    y = []
    for i in range(1000):
        y.append(lmu.step([1]))

    filt = nengo.synapses.Lowpass(0.1)
    ideal = filt.filt(np.ones((1000, 1)))

    y = np.array(y)

    assert np.allclose(y, ideal)
