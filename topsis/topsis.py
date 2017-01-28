from interface.definitions import MCDAProblem


def topsis(problem):
    performance_table = problem.get_performance_table()
    criteria_weights = problem.get_criteria_weights()
    print(criteria_weights)


def main():
    problem = MCDAProblem()
    problem.read_performance_table('performanceTable.csv')
    # problem.read_criteria_min_max('criteriaMinMax.csv')
    # problem.read_number_of_breakpoints('numberOfBreakPoints.csv')
    problem.read_criteria_weights('criteriaWeights.csv')

    ret = topsis(problem)


if __name__ == '__main__':
    main()
