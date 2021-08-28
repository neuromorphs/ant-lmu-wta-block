import numpy as np
import scipy.linalg

from . import neuron_types


def generate_LMU(theta, q, dt):
    A = np.zeros((q, q))
    B = np.zeros((q, 1))
    for i in range(q):
        B[i] = (-1.)**i * (2*i+1)
        for j in range(q):
            A[i, j] = (2*i+1)*(-1 if i < j else (-1.)**(i-j+1))
    A = A / theta
    B = B / theta

    # handle discrete time step
    Ad = scipy.linalg.expm(A*dt)
    Bd = np.dot(np.dot(np.linalg.inv(A), (Ad-np.eye(q))), B)

    return Ad, Bd


class LMUWTABlock(object):
    def __init__(self, q, theta, n_neurons, size_in, size_out,
                 neuron_type=neuron_types.RectifiedLinear(), n_WTA=0, dt=0.001):
        self.theta = theta
        self.q = q
        self.dt = dt
        self.Ad, self.Bd = generate_LMU(theta, q, dt)

        self.m = np.zeros((q, size_in))
        self.a = np.zeros(n_neurons)

        self.n_neurons = n_neurons
        self.neuron_type = neuron_type

        # TODO: add methods to generate E, D, and bias
        self.E = np.zeros((n_neurons, q * size_in))
        self.D = np.zeros((size_out, n_neurons))
        self.bias = np.zeros(n_neurons)

        self.n_WTA = n_WTA
        if self.n_WTA > self.n_neurons:
            raise ValueError("n_WTA must be smaller than n_neurons")

    def WTA(self):
        args = np.argpartition(self.a,-self.n_WTA)[-self.n_WTA:]
        self.a[:] = 0
        self.a[args] = 1

    def step(self, x):
        x = np.asarray(x)
        self.m[:] = self.Ad.dot(self.m) + self.Bd.dot(x[None, :])
        J = self.E.dot(self.m.flat) + self.bias
        self.a[:] = self.neuron_type.step(J)
        if self.n_WTA > 0:
            self.WTA()
        y = self.D.dot(self.a)
        return y
