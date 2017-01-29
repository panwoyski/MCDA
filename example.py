from interface.definitions import MCDAProblem


def mojaMetoda(problem):
    #tutaj kod metody
    pass


def main():
    problem = MCDAProblem()
    problem.read_performance_table('input_files/performanceTable.csv')
    problem.read_criteria_min_max('input_files/criteriaMinMax.csv')
    problem.read_number_of_breakpoints('input_files/numberOfBreakPoints.csv')
    problem.read_alternatives_ranks('input_files/alternativesRanks.csv')


    solution = mojaMetoda(problem)


if __name__ == '__main__':
    main()
