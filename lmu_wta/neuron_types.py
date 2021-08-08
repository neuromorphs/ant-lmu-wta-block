import numpy as np


class NeuronType:
    """Base class for all neurons."""

    def step(self, J):
        """Simulate the neuron for one time step with an input J"""
        raise NotImplementedError()

    def rate_to_current(self, rate):
        """Return the input J that will produce the given rate"""
        raise NotImplementedError()

    def intercept(self):
        """Return the input J where the neuron is the most non-linear"""
        raise NotImplementedError()


class RectifiedLinear(NeuronType):
    """The standard rectified linear (ReLU) neuron."""

    def step(self, J):
        return np.maximum(J, 0)

    def rate_to_current(self, rate):
        return rate

    def intercept(self):
        return 0


class Sigmoid(NeuronType):
    """A sigmoid neuron.

    The output is bounded between 0 and maximum.
    """
    def __init__(self, maximum=1000):
        self.maximum = maximum

    def step(self, J):
        return self.maximum / (1 + np.exp(-J))

    def rate_to_current(self, rate):
        scale = rate / self.maximum
        return np.log(-scale / (scale-1))

    def intercept(self):
        return 0


class Tanh(NeuronType):
    """A neuron with the hyperbolic tangent as an activation function.

    The output is bounded between -maximum and +maximum.
    """
    def __init__(self, maximum=1000):
        self.maximum = maximum

    def step(self, J):
        return self.maximum * np.tanh(J)

    def rate_to_current(self, rate):
        return np.arctanh(rate/self.maximum)

    def intercept(self):
        return 0


class LIFRate(NeuronType):
    """A rate-mode version ot the Leaky Integrate-and-Fire neuron."""

    def __init__(self, tau_ref=0.002, tau_rc=0.02):
        self.tau_ref = tau_ref
        self.tau_rc = tau_rc

    def step(self, J):
        valid = J > 1
        r = np.zeros_like(J)
        r[valid] = 1/(self.tau_ref - self.tau_rc*np.log(1-1/J[valid]))
        return r

    def rate_to_current(self, rate):
        return 1/(1-np.exp((self.tau_ref-1/rate)/self.tau_rc))

    def intercept(self):
        return 1


class Linear(NeuronType):
    """A perfectly linear neuron."""

    def step(self, J):
        return J

    def rate_to_current(self, rate):
        return rate

    def intercept(self):
        return 0
