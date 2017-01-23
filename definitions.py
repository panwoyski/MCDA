import csv
import numpy as np


class Alternative(object):
    def __init__(self):
        
        self.name = ""
        self.criteriaList = []
        self.rank = 0
    
    def add_criterion(self, criterion):
        self.criteriaList.append(criterion)

    def clear_criteria(self):
        self.criteriaList.clear()
        pass


class Criterion(object):
    def __init__(self, value=0):
        self.value = value
        self.minMax = "max"
        self.numberOfBreakPoints = 2
        self.weight = 0


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

    def read_performance_table(self, file_path):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=';')
            for data in reader:
                alt = Alternative()
                alt.name = data.pop(0)
                for val in data:
                    crit = Criterion(val)
                    alt.add_criterion(crit)
                self.alternativesList.append(alt)

    def read_alternatives_ranks(self, file_path):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=';')
            line = next(reader)

            if not len(line) == len(self.alternativesList):
                raise ValueError("Not maching numberOfBreakPoints len with alt len")
            for val, alt in zip(line, self.alternativesList):
                alt.rank = int(val)

    def read_criteria_weights(self, file_path):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=';')
            line = next(reader)

            if not len(line) == len(self.alternativesList):
                raise ValueError("Not maching criteriaWeights len with alt len")
            for val, alt in zip(line, self.alternativesList):
                alt.weight = int(val)

    def read_number_of_breakpoints(self, filePath):

        with open(filePath) as data_file:
            reader = csv.reader(data_file, delimiter=';')
            line = next(reader)
            for alt in self.alternativesList:
                # check input for each alternative
                if not len(line) == len(alt.criteriaList):
                    raise ValueError("Not maching numberOfBreakPoints len with criteria len in alt: " + alt.name)
            for alt in self.alternativesList:
                for val, crit in zip(line, alt.criteriaList):
                    crit.numberOfBreakPoints = int(val)

    def read_criteria_min_max(self, file_path):

        with open(file_path) as data_file:
            reader = csv.reader(data_file, delimiter=';')
            line = next(reader)
            for alt in self.alternativesList:
                # check input for each alternative
                if not len(line) == len(alt.criteriaList):
                    raise ValueError("Not maching criteriaMinMax len with criteria len in alt: " + alt.name)
            for alt in self.alternativesList:
                for val, crit in zip(line, alt.criteriaList):
                    crit.minMax = val

    def get_performance_table(self):
        performance_table = np.zeros((len(self.alternativesList), len(self.alternativesList[0].criteriaList)))

        for i in range(len(self.alternativesList)):
            for j in range(len(self.alternativesList[i].criteriaList)):
                performance_table[i][j] = self.alternativesList[i].criteriaList[j].value

    # def get_criteria_weights(self):

