from lmu_wta import LMUWTABlock
import numpy as np
import matplotlib.pyplot as plt

def sequence(q,tolerance):
    N_neurons = 50
    input_sequence_length = 5
    presentation_time = 10000
    max_input_value = 10

    lmus = []
    thetas = np.arange(0.1, 10, 1)
    print(thetas)
    for theta in thetas:
        lmu = LMUWTABlock(q=q, theta=theta, n_neurons=N_neurons,
                          size_in=1, size_out=1)
        lmu.E[:] = 1
        lmu.D[:] = 1/N_neurons
        lmus.append(lmu)

    rng = np.random.RandomState(seed=12)
    input = rng.randint(0, max_input_value, input_sequence_length)

    x = np.array([])
    for inp in input:
        x = np.append(x, inp*np.ones(presentation_time))

    ys = []
    for lmu in lmus:
        y = np.array([])
        for i in range(input.shape[0]*presentation_time):
            y = np.append(y, lmu.step([x[i]]))
        ys.append(y)

    # Delayed inputs to compare with outputs
    xs_del = []
    for lmu in lmus:
        xs_del.append(np.append(np.zeros(int(lmu.theta/lmu.dt)),
                                x)[0:-int(lmu.theta/lmu.dt)])

    errors = []
    for i in range(len(lmus)):
        error = np.sqrt(((xs_del[i] - ys[i])**2).mean())
        errors.append(error)

    errors = np.array(errors)
    normalized_errors = errors/max_input_value
    squared_errors = np.power(normalized_errors, 2)

    print(squared_errors)
    print(tolerance)
    assert(squared_errors < tolerance).all()
    # return squared_errors

def test_sequence():
    c = 0.015/9
    for q in range(10):
        sequence(2*q+2,c*np.linspace(0.1,9.1,10))
