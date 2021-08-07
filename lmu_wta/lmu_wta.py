import numpy as np
import scipy.linalg


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
    def __init__(self, q, theta, n_neurons, size_in, size_out, dt=0.001):
        self.theta = theta
        self.q = q
        self.dt = dt
        self.Ad, self.Bd = generate_LMU(theta, q, dt)

        self.m = np.zeros((q, size_in))
        self.a = np.zeros(n_neurons)

        # TODO: add methods to generate E, D, and bias
        self.E = np.zeros((n_neurons, q * size_in))
        self.D = np.zeros((size_out, n_neurons))
        self.bias = np.zeros(n_neurons)

        # TODO: add WTA option

    def nonlinearity(self, J):
        # TODO: add other neuron models?
        # rectified linear
        return np.maximum(J, 0)

    def step(self, x):
        x = np.asarray(x)
        self.m[:] = self.Ad.dot(self.m) + self.Bd.dot(x[None, :])
        J = self.E.dot(self.m.flat) + self.bias
        self.a[:] = self.nonlinearity(J)
        y = self.D.dot(self.a)
        return y
