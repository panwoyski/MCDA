from interface.definitions import MCDAProblem
import numpy as np
import math as mt


def topsis(problem,
           positive_ideal_solution=None,
           negative_ideal_solution=None):
    performance_table = problem.get_performance_table()
    criteria_weights = problem.criteria_weights
    criteria_directions = problem.criteria_directions

    alternative_number, criteria_number = performance_table.shape
    divide_by = np.arange(criteria_number, dtype=np.float32)

    for i in range(criteria_number):
        sum_val = np.sum(np.power(performance_table[:, i], 2))
        divide_by[i] = mt.sqrt(sum_val)

    normalised_m = np.zeros(shape=(0, criteria_number))
    for a in performance_table:
        normalised_m = np.vstack((normalised_m, np.divide(a, divide_by)))

    wnm = np.zeros(shape=(0, criteria_number))
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

    err_pis = np.power((wnm - pis), 2)
    err_nis = np.power((wnm - nis), 2)

    spisv = np.sqrt(err_pis.sum(1))
    snisv = np.sqrt(err_nis.sum(1))

    results = snisv / (spisv + snisv)

    best_alt_index = results.argmax()
    best_alt = problem.get_alterntive(best_alt_index)

    return best_alt


def main():
    problem = MCDAProblem()

    path_root = '../input_files/topsis_test_input/%s.csv'
    problem.read_performance_table(path_root % 'performance_table', delimiter=',')
    problem.read_criteria_weights(path_root % 'weights', delimiter=',')
    problem.read_criteria_directions(path_root % 'directions', delimiter=',')

    ret = topsis(problem)
    print('Best alternative is: %s' % ret.name)


if __name__ == '__main__':
    main()
