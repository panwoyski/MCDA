import numpy as np


def apply_on_each_element(func, matrix):
    try:
        x_dim, y_dim = matrix.shape
    except AttributeError:
        x_dim = len(matrix)
        y_dim = len(matrix[0]) if x_dim > 0 else 0

    result = np.zeros((x_dim, y_dim))

    for x in range(x_dim):
        for y in range(y_dim):
            result[x, y] = func(matrix[x, y])

    return result


def apply_on_each_index(func, shape):
    x_dim, y_dim = shape
    result = np.zeros(shape)

    for x in range(x_dim):
        for y in range(y_dim):
            result[x, y] = func(x, y)

    return result
