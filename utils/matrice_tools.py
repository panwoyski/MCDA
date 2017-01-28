import numpy as np


def apply_on_each_index(func, shape):
    x_dim, y_dim = shape
    result = np.zeros(shape)

    for x in range(x_dim):
        for y in range(y_dim):
            result[x, y] = func(x, y)

    return result
