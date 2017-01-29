from interface.definitions import MCDAProblem, Alternative, Criterion
import numpy as np
from utils.matrice_tools import apply_on_each_index, apply_on_each_element


class MCDAProxy(object):
    def __init__(self, problem):
        self.problem = problem

    def apply_on_each_crit(self, func):
        x_dim = len(self.problem.alternativesList)
        y_dim = len(self.problem.alternativesList[0].criteriaList) if x_dim > 0 else 0

        result = np.zeros((x_dim, y_dim))

        for x in range(x_dim):
            for y in range(y_dim):
                result[x, y] = func(self.problem.alternativesList[x].criteriaList[y])

        return result

    def alt_count(self):
        return len(self.problem.alternativesList)

    def crit_count(self):
        return len(self.problem.alternativesList[0].criteriaList) if self.alt_count() > 0 else 0

    def criterion(self, i, j):
        if i >= self.alt_count() or j >= self.crit_count():
            raise ValueError('index out of bounds')

        return self.problem.alternativesList[i].criteriaList[j]

    def weight(self, i):
        return self.problem.criteria_weights[i]

    def value(self, i, j):
        return self.criterion(i, j).value

    def direction(self, i, j):
        return self.criterion(i, j).minmax

    def p(self, i):
        return self.problem.criteria_preference[i]

    def q(self, i):
        return self.problem.criteria_indifference[i]

    def veto(self, i):
        return self.problem.veto_thresholds[i]

    def alternative(self, i):
        return self.problem.alternativesList[i]


def electre_is(problem):
    assert isinstance(problem, MCDAProblem), "This metod works only with MCDAproblems"

    pr = MCDAProxy(problem)

    def js(a, b):
        def predicate(j):
            return pr.value(a, j) >= pr.value(b, j) - pr.q(j)

        indexes = filter(predicate, range(pr.crit_count()))
        return list(indexes)

    def jq(a, b):
        def predicate(j):
            return pr.value(b, j) - pr.p(j) <= pr.value(a, j) < pr.value(b, j) - pr.q(j)

        indexes = filter(predicate, range(pr.crit_count()))
        return list(indexes)

    def jp(a, b):
        def predicate(j):
            return pr.value(b, j) > pr.value(a, j) + pr.p(j)

        indexes = filter(predicate, range(pr.crit_count()))
        return list(indexes)

    def fi(a, b, j):
        nom = pr.p(j) + pr.value(a, j) - pr.value(b, j)
        denom = pr.p(j) - pr.q(j)
        return float(nom)/denom

    def concordance(a, b):
        if len(jp(a, b)) == pr.crit_count():
            return 0
        if len(js(a, b)) == pr.crit_count():
            return 1

        part1 = sum(pr.weight(j) for j in js(a, b))

        part2 = sum(fi(a, b, j) * pr.weight(j) for j in jq(a, b))

        norm = sum(pr.weight(j) for j in range(pr.crit_count()))

        return float(part1 + part2) / norm

    s = 0.60
    dim = pr.alt_count()
    concordance_mtx = apply_on_each_index(concordance, (dim, dim))

    def condition1(val):
        return 0.5 < val < s

    def filter_by_condition(value):
        if condition1(value):
            return value

        return 0

    filtered_matrix = apply_on_each_element(filter_by_condition, concordance_mtx)
    # print(filtered_matrix)

    # import itertools as it

    # failed_dict = {(a, b): [] for a, b in it.permutations(range(pr.alt_count()), 2)}

    def condition2(a, b, j):
        def w(x, y, i):
            norm = sum(pr.weight(jj) for jj in range(pr.crit_count()))
            nom = 1 - concordance_mtx[x, y] - pr.weight(i) / norm
            denom = 1 - s - pr.weight(i) / norm
            return float(nom) / denom

        # if not (pr.value(a, j) + pr.veto(j) >= pr.value(b, j) + pr.q(j) + w(a, b, j)):
        #     failed_dict[(a, b)].append(j)

        return pr.value(a, j) + pr.veto(j) >= pr.value(b, j) + pr.q(j) + w(a, b, j)

    def filter2(a, b):
        return all(condition2(a, b, j) for j in range(pr.crit_count()))

    filtered2_matrix = apply_on_each_index(filter2, (dim, dim))

    result_matrix = filtered_matrix * filtered2_matrix

    non_zero = result_matrix.nonzero()
    graph_dict = {k: [] for k in non_zero[0]}
    for i, k in enumerate(non_zero[0]):
        graph_dict[k].append(non_zero[1][i])

    filtered = list(filter(lambda x: x not in non_zero[1], non_zero[0]))
    best_alternatives = [pr.alternative(i) for i in filtered]

    return best_alternatives, graph_dict


def main():
    problem = MCDAProblem()

    path_root = '../input_files/electre_test_input/%s'

    problem.read_performance_table(path_root % 'testAlternatives.csv', delimiter=',')
    problem.read_criteria_weights(path_root % 'weights.csv', delimiter=',')
    problem.read_veto_thresholds(path_root % 'vetos.csv', delimiter=',')
    problem.read_preference(path_root % 'preference.csv', delimiter=',')
    problem.read_indifference(path_root % 'indifference.csv', delimiter=',')

    best_alternatives, graph = electre_is(problem)

    if len(best_alternatives):
        print('Najlepsze alternatywy')
        print(', '.join(alt.name for alt in best_alternatives))
    else:
        print('Dla zadanych parametrow brak rozwiazan')
        print('struktura grafu:')
        print(graph)


if __name__ == '__main__':
    main()
