from . import neuron_types

import numpy as np


def generate_encoders(block, output_range=(150, 200), radius=1, seed=None,
                      override_maximum=True):
    rng = np.random.default_rng(seed=seed)

    N = block.E.shape[0]
    max_rate = rng.uniform(output_range[0], output_range[1], N)
    intercepts = rng.uniform(-radius, radius, N)

    if override_maximum:
        if isinstance(block.neuron_type, neuron_types.Sigmoid):
            block.neuron_type.maximum = output_range[1]

        if isinstance(block.neuron_type, neuron_types.Tanh):
            block.neuron_type.maximum = output_range[1]

    J_max = block.neuron_type.rate_to_current(max_rate)
    gain = (J_max - block.neuron_type.intercept()) / (radius - intercepts)
    bias = J_max - gain * radius

    encoders = np.random.normal(size=block.E.shape)
    encoders /= np.linalg.norm(encoders, axis=1)[:, None]

    block.E[:] = encoders * gain[:, None]
    block.bias[:] = bias
