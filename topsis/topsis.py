from interface.definitions import MCDAProblem
import numpy as np
import math as mt


def topsis(problem,
           positive_ideal_solution=None,
           negative_ideal_solution=None):
    performance_table = problem.get_performance_table()
    criteria_weights = problem.criteria_weights
    criteria_directions = problem.criteria_directions

    print(performance_table)

    alternative_number, criteria_number = performance_table.shape
    divide_by = np.arange(criteria_number, dtype=np.float32)

    for i in range(criteria_number):
        sum_val = np.sum(np.power(performance_table[:, i], 2))
        divide_by[i] = mt.sqrt(sum_val)

    normalised_m = np.zeros(shape=(0, criteria_number))
    for a in performance_table:
        normalised_m = np.vstack((normalised_m, np.divide(a, divide_by)))

    wnm = np.zeros(shape=(0,criteria_number))
    for a in normalised_m:
        wnm = np.vstack((wnm, np.multiply(a, criteria_weights)))

    pis = np.arange(criteria_number, dtype=np.float64)
    nis = np.arange(criteria_number, dtype=np.float64)

    if positive_ideal_solution is None or negative_ideal_solution is None:
        for i in range(criteria_number):
            if criteria_directions[i] == "max":
                pass
                pis[i] = max(wnm[:, i])
                nis[i] = min(wnm[:, i])
            else:
                pis[i] = min(wnm[:, i])
                nis[i] = max(wnm[:, i])
    else:
        pis = positive_ideal_solution
        nis = negative_ideal_solution

    print(pis)
    print(nis)


def main():
    problem = MCDAProblem()

    performance_tale = np.array([[5490, 51.4, 8.5, 285],
                                 [6500, 70.6, 7,   288],
                                 [6489, 54.3, 7.5, 290]])

    problem.read_performance_from_matrix(performance_tale)

    problem.criteria_weights = [0.35, 0.25, 0.25, 0.15]
    problem.criteria_directions = ["min", "max", "max", "max"]

    ret = topsis(problem)


if __name__ == '__main__':
    main()
