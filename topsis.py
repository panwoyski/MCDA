from definitions import MCDAProblem
import numpy as np

def topsis(problem):
    performance_table = problem.get_performance_table()





def main():
    problem = MCDAProblem()
    problem.read_performance_table('performanceTable.csv')
    problem.read_criteria_min_max('criteriaMinMax.csv')
    problem.read_number_of_breakpoints('numberOfBreakPoints.csv')
    problem.read_alternatives_ranks('alternativesRanks.csv')

    ret = topsis(problem)


if __name__ == '__main__':
    main()
