import csv
import numpy as np


class Alternative(object):
    def __init__(self, name='', rank=0):
        self.name = name
        self.criteriaList = []
        self.rank = rank
    
    def add_criterion(self, criterion):
        self.criteriaList.append(criterion)

    def clear_criteria(self):
        self.criteriaList.clear()


class Criterion(object):
    def __init__(self,
                 value=0,
                 weight=0,
                 minmax='max',
                 breakpoints=2):

        self.value = value
        self.minMax = minmax
        self.numberOfBreakPoints = breakpoints
        self.weight = weight


class MCDAProblem(object):
    def __init__(self):
        self.alternativesList = []
        '''
        MCDA problem we are solving
        lets say:
        0 - find ranking of alternatives
        1 - find best alternative
        2 - class aggregation
        3 - .... something else
        '''
        self.problemType = 0
        # if anyone needs it, enjoy
        self.epsilon = 0.05
        self.criteria_weights = []
        self.criteria_directions = []
        self.criteria_preference = []
        self.criteria_indifference = []
        self.veto_thresholds = []

    def read_performance_table(self, file_path, delimiter=';'):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=delimiter)
            for data in reader:
                alt = Alternative(name=data.pop(0))
                for val in data:
                    crit = Criterion(float(val))
                    alt.add_criterion(crit)
                self.alternativesList.append(alt)

    def read_performance_from_matrix(self, matrix):
        for i, line in enumerate(matrix):
            alt = Alternative(name='a%s' % i)
            for value in line:
                crit = Criterion(float(value))
                alt.add_criterion(crit)
            self.alternativesList.append(alt)

    def read_alternatives_ranks(self, file_path, delimiter=';'):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=delimiter)
            line = next(reader)

            if not len(line) == len(self.alternativesList):
                raise ValueError("Not maching alternative_ranks len with alt len")
            for val, alt in zip(line, self.alternativesList):
                alt.rank = int(val)

    def read_criteria_weights(self, file_path, delimiter=';'):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=delimiter)
            line = next(reader)

            line_len = len(line)
            if not line_len == len(self.alternativesList[0].criteriaList):
                raise ValueError("Not maching criteria_weights len with alt len")

            self.criteria_weights = np.zeros(line_len)
            for i, val in enumerate(line):
                self.criteria_weights[i] = float(val)

    def read_number_of_breakpoints(self, file_path, delimiter=';'):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=delimiter)
            line = next(reader)
            for alt in self.alternativesList:
                # check input for each alternative
                if not len(line) == len(alt.criteriaList):
                    raise ValueError("Not maching numberOfBreakPoints len with criteria len in alt: " + alt.name)
            for alt in self.alternativesList:
                for val, crit in zip(line, alt.criteriaList):
                    crit.numberOfBreakPoints = int(val)

    def read_criteria_min_max(self, file_path, delimiter=';'):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=delimiter)
            line = next(reader)
            for alt in self.alternativesList:
                # check input for each alternative
                if not len(line) == len(alt.criteriaList):
                    raise ValueError("Not maching criteriaMinMax len with criteria len in alt: " + alt.name)
            for alt in self.alternativesList:
                for val, crit in zip(line, alt.criteriaList):
                    crit.minMax = val

    def read_veto_thresholds(self, file_path, delimiter=','):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=delimiter)
            line = next(reader)

            line_len = len(line)
            for alt in self.alternativesList:
                # check input for each alternative
                if not line_len == len(alt.criteriaList):
                    raise ValueError("Criteria amount doesnt match with veto amount in alt: " + alt.name)

            self.veto_thresholds = np.zeros(line_len)
            for i, val in enumerate(line):
                self.veto_thresholds[i] = float(val)

    def read_preference(self, file_path, delimiter=','):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=delimiter)
            line = next(reader)

            line_len = len(line)
            for alt in self.alternativesList:
                # check input for each alternative
                if not line_len == len(alt.criteriaList):
                    raise ValueError("Criteria amount doesnt match with veto amount in alt: " + alt.name)

            self.criteria_preference = np.zeros(line_len)
            for i, val in enumerate(line):
                self.criteria_preference[i] = float(val)

    def read_indifference(self, file_path, delimiter=','):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=delimiter)
            line = next(reader)

            line_len = len(line)
            for alt in self.alternativesList:
                # check input for each alternative
                if not line_len == len(alt.criteriaList):
                    raise ValueError("Criteria amount doesnt match with veto amount in alt: " + alt.name)

            self.criteria_indifference = np.zeros(line_len)
            for i, val in enumerate(line):
                self.criteria_indifference[i] = float(val)

    def get_performance_table(self):
        performance_table = np.zeros((len(self.alternativesList),
                                      len(self.alternativesList[0]
                                              .criteriaList)))

        for i in range(len(self.alternativesList)):
            for j in range(len(self.alternativesList[i].criteriaList)):
                performance_table[i][j] = self.alternativesList[i].criteriaList[j].value

        return performance_table

    def get_alterntive(self, i):
        return self.alternativesList[i]
