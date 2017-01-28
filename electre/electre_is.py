from interface.definitions import MCDAProblem, Alternative, Criterion


def electre_is(problem):
    assert isinstance(problem, type(MCDAProblem)), "This metod works only with MCDAproblems"

    for alt in problem.alternativesList:
        print(len(alt.criteriaList))


def main():
    problem = MCDAProblem

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
