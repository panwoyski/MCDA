from interface.definitions import MCDAProblem, Alternative, Criterion
import numpy as np
from utils.matrice_tools import apply_on_each_index, apply_on_each_element


def electre_is(problem):
    assert isinstance(problem, MCDAProblem), "This metod works only with MCDAproblems"

    alt_vals = problem.apply_on_each_crit(lambda crit: crit.value)
    alt_weights = problem.apply_on_each_crit(lambda crit: crit.weight)
    print(alt_vals)
    print(alt_weights)


def main():
    problem = MCDAProblem()

    alt1 = Alternative("test1", 0, [
        Criterion(10, 1, 0.2, 0.3),
        Criterion(9, 1, 0.3, 0.5),
        Criterion(8, 1, 0.3, 0.5),
        Criterion(11, 1, 0.2, 0.2),
    ])

    alt2 = Alternative("test1", 0, [
        Criterion(9, 1, 0.3, 0.5),
        Criterion(10, 1, 0.2, 0.3),
        Criterion(11, 1, 0.2, 0.2),
        Criterion(8, 1, 0.3, 0.5),
    ])

    alt3 = Alternative("test1", 0, [
        Criterion(9, 1, 0.3, 0.5),
        Criterion(11, 1, 0.2, 0.2),
        Criterion(10, 1, 0.2, 0.3),
        Criterion(8, 1, 0.3, 0.5),
    ])

    problem.alternativesList = [alt1, alt2, alt3]

    electre_is(problem)


if __name__ == '__main__':
    main()
