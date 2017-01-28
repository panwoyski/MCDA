from interface.definitions import MCDAProblem


def mojaMetoda(problem):
    #tutaj kod metody
    pass

if __name__ == '__main__':
    
    problem = MCDAProblem()
    problem.read_performance_table('performanceTable.csv')
    problem.read_criteria_min_max('criteriaMinMax.csv')
    problem.read_number_of_breakpoints('numberOfBreakPoints.csv')
    problem.read_alternatives_ranks('alternativesRanks.csv')


    solution = mojaMetoda(problem)
