from lmu_wta import LMUWTABlock
import numpy as np


def test_sequence():
    N_neurons = 50
    input_sequence_length = 5
    presentation_time = 10000
    max_input_value = 10

    lmu = LMUWTABlock(q=10, theta=0.1, n_neurons=N_neurons,
                      size_in=1, size_out=1)
    lmu.E[:] = 1
    lmu.D[:] = 1/N_neurons

    rng = np.random.RandomState(seed=12)
    input = rng.randint(0, max_input_value, input_sequence_length)

    x = np.array([])
    for inp in input:
        x = np.append(x, inp*np.ones(presentation_time))

    y = np.array([])
    for i in range(input.shape[0]*presentation_time):
        y = np.append(y, lmu.step([x[i]]))

    x_del = np.append(np.zeros(int(lmu.theta*1000)), x)[0:-int(lmu.theta*1000)]
    # Delayed input to compare with output

    error = np.sqrt(((x_del - y.T)**2).mean())
    normalized_error = error/max_input_value

    tolerance = 0.01
    # Error limit should be some function of q and theta
    # but I don't know exactly what

    assert(normalized_error < tolerance)
