from interface.definitions import MCDAProblem
import numpy as np


def topsis(problem):
    performance_table = problem.get_performance_table()
    criteria_weights = problem.criteria_weights
    print(performance_table)
    print(criteria_weights)


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
