import csv
import numpy as np
import scipy.optimize as sopt
from pprint import pprint

from definitions import *



def utastar(problem):

    performanceTable = np.zeros((len(problem.alternativesList), len(problem.alternativesList[0].criteriaList)))

    for i in range(0,len(problem.alternativesList)):
        for j in range(0,len(problem.alternativesList[i].criteriaList)):
            performanceTable[i][j] = problem.alternativesList[i].criteriaList[j].value
            
    criteriaNumberOfBreakPoints = np.array([a.numberOfBreakPoints for a in problem.alternativesList[0].criteriaList])
    criteriaMinMax = np.array([a.minMax for a in problem.alternativesList[0].criteriaList])
    alternativesRanks = np.array([a.rank for a in problem.alternativesList])
    epsilon = problem.epsilon

    numCrit = performanceTable.shape[1]

    numAlt = performanceTable.shape[0]

    criteriaBreakPoints = []

    for i in range(0, numCrit):
        mini = np.amin(performanceTable[:,i])
        maxi = np.amax(performanceTable[:,i])

        if mini == maxi:
            pass


        alphai = criteriaNumberOfBreakPoints[i]

        tmp = np.zeros(alphai)
        for j in range(0,alphai):
            tmp[j] = mini + j/(float)(alphai-1) * (maxi - mini)


        tmp[0] = mini
        tmp[alphai-1] = maxi


        if (criteriaMinMax[i] == "min"):
            tmp[::-1].sort() #Sorting decreasingly


        criteriaBreakPoints.append(tmp)

    a = np.zeros((numAlt, np.sum(criteriaNumberOfBreakPoints) + 2 * numAlt))

    for n in range(0, numAlt):
        for m in range(0, numCrit):
            if np.any(performanceTable[n,m] == criteriaBreakPoints[m]):
                j = np.where(performanceTable[n,m] == criteriaBreakPoints[m])[0]

                if m == 0:
                    pos = j
                else:
                    pos = np.sum(criteriaNumberOfBreakPoints[0:m]) + j
                a[n,pos] = 1
            else:
                if criteriaMinMax[m] == "min":
                    j = np.where(performanceTable[n,m]>criteriaBreakPoints[m])[0][0] - 1
                else:
                    j = np.where(performanceTable[n,m]<criteriaBreakPoints[m])[0][0] - 1

                if m == 0:
                    pos = j
                else:
                    pos = np.sum(criteriaNumberOfBreakPoints[0:m]) + j

                a[n,pos] = 1 - (performanceTable[n,m] - criteriaBreakPoints[m][j])/(float)(criteriaBreakPoints[m][j+1] - criteriaBreakPoints[m][j])
                a[n,pos + 1] = (performanceTable[n,m] - criteriaBreakPoints[m][j])/(float)(criteriaBreakPoints[m][j+1] - criteriaBreakPoints[m][j])

            a[n,a.shape[1]-2*numAlt+n] = -1

            a[n,a.shape[1]-numAlt+n] = 1


    obj = np.zeros(np.sum(criteriaNumberOfBreakPoints))

    obj = np.append(obj, np.ones(2*numAlt))



    preferenceConstraints = np.zeros(shape=(0,np.sum(criteriaNumberOfBreakPoints)+2*numAlt))
    indifferenceConstraints = np.zeros(shape=(0,np.sum(criteriaNumberOfBreakPoints)+2*numAlt))

    indexOrder = []

    orderedAlternativesRanks = np.sort(alternativesRanks)

    tmpRanks1 = alternativesRanks
    tmpRanks2 = alternativesRanks


    while len(orderedAlternativesRanks) != 0:
        tmpIndex = np.where(alternativesRanks == orderedAlternativesRanks[0])[0]
        for i in range(0,len(tmpIndex)):
            indexOrder = np.append(indexOrder,tmpIndex[i])
        orderedAlternativesRanks = np.delete(orderedAlternativesRanks, np.where(orderedAlternativesRanks == orderedAlternativesRanks[0])[0], None)


    for i in range(0,len(alternativesRanks)-1):
        if alternativesRanks[int(indexOrder[i])] == alternativesRanks[int(indexOrder[i+1])]:
            indifferenceConstraints = np.vstack((indifferenceConstraints, a[int(indexOrder[i])] - a[int(indexOrder[i+1])]))
        else:
            preferenceConstraints = np.vstack((preferenceConstraints, a[int(indexOrder[i])] - a[int(indexOrder[i+1])]))




    mat = np.vstack((preferenceConstraints,indifferenceConstraints))

    rhs = [] 

    if np.shape(preferenceConstraints)[0] != 0:
        for i in range(0, np.shape(preferenceConstraints)[0]):
            rhs = np.append(rhs, epsilon)

    if np.shape(indifferenceConstraints)[0] != 0:
        for i in range(0, np.shape(indifferenceConstraints)[0]):
            rhs = np.append(rhs, 0)


    dirr = np.zeros(np.shape(preferenceConstraints)[0], dtype=np.dtype('a16'))


    if np.shape(preferenceConstraints)[0] != 0:
        for i in range(0, np.shape(preferenceConstraints)[0]):
            dirr[i] = (">=")

    if np.shape(indifferenceConstraints)[0] != 0:
        for i in range(0, np.shape(indifferenceConstraints)[0]):
            dirr = np.append(dirr, "==")


    monotonicityConstraints = np.zeros(shape=(0,np.sum(criteriaNumberOfBreakPoints)+2*numAlt))


    for i in range (0,len(criteriaNumberOfBreakPoints)):
        for j in range (0,criteriaNumberOfBreakPoints[i]-1):
            tmp = np.zeros(np.sum(criteriaNumberOfBreakPoints)+2*numAlt)
            if i == 0:
                pos = j
            else:
                pos = np.sum(criteriaNumberOfBreakPoints[0:i])+j
            tmp[pos] = -1
            tmp[pos+1] = 1

            monotonicityConstraints = np.vstack((monotonicityConstraints, tmp))


    mat = np.vstack((mat, monotonicityConstraints))


    for i in range(0, np.shape(monotonicityConstraints)[0]):
        dirr = np.append(dirr, ">=")



    for i in range(0, np.shape(monotonicityConstraints)[0]):
        rhs = np.append(rhs,0)


    tmp = np.zeros(shape=(np.sum(criteriaNumberOfBreakPoints)+2*numAlt))

    for i in range(0,len(criteriaNumberOfBreakPoints)):
        if i == 0:
            pos = criteriaNumberOfBreakPoints[i]
        else:
            pos = np.sum(criteriaNumberOfBreakPoints[0:i]) + criteriaNumberOfBreakPoints[i]
        tmp[pos-1] = 1

    mat = np.vstack((mat,tmp))

    dirr = np.append(dirr,"==")

    rhs = np.append(rhs,1)




    minValueFunctionsConstraints = np.zeros(shape=(0,np.sum(criteriaNumberOfBreakPoints)+2*numAlt))


    for i in range(0,len(criteriaNumberOfBreakPoints)):
        tmp = np.zeros(shape=(np.sum(criteriaNumberOfBreakPoints)+2*numAlt))
        if i == 0:
            pos = i
        else:
            pos = np.sum(criteriaNumberOfBreakPoints[0:i])
        tmp[pos] = 1
        minValueFunctionsConstraints = np.vstack((minValueFunctionsConstraints, tmp))

    mat = np.vstack((mat, minValueFunctionsConstraints))


    for i in range(0, np.shape(minValueFunctionsConstraints)[0]):
        dirr = np.append(dirr, "==")


    for i in range(0, np.shape(minValueFunctionsConstraints)[0]):
        rhs = np.append(rhs, 0)


    def convert_to_scikit_format(dirr, mat, rhs):
        """
        :param dirr: typ rownania/nierownosci dla i-tego ograniczenia
        :param mat: macierz ograniczen R(NxM)
                    N - indeks ograniczenia
                    M - indeks zmiennej
        :param rhs: prawe strony ograniczen
        :return:
        """
        if not len(dirr) == len(mat) == len(rhs):
            raise ValueError("Rozna ilosc wierszy")
        A_ub = []
        b_ub = []
        A_eq = []
        b_eq = []
        for ind in range(len(dirr)):
            if dirr[ind] == '<=':
                A_ub.append(mat[ind])
                b_ub.append(rhs[ind])
            if dirr[ind] == '>=':
                A_ub.append(-1 * mat[ind])
                b_ub.append(-1 * rhs[ind])
            if dirr[ind] == '==':
                A_eq.append(mat[ind])
                b_eq.append(rhs[ind])
        return A_ub, b_ub, A_eq, b_eq

    A_ub, b_ub, A_eq, b_eq = convert_to_scikit_format(dirr, mat, rhs)

    lpsolution = sopt.linprog(
        c=obj,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
    )

    if not lpsolution['success']:
        raise RuntimeError(lpsolution['message'])

    lpValues = lpsolution['x']

    valueFunctions = []
    for i in range(criteriaNumberOfBreakPoints.size):
        tmp = []
        pos = 0
        if i == 0:
            pos = 0
        else:
            pos = sum(criteriaNumberOfBreakPoints[0:i])
        for j in range(criteriaNumberOfBreakPoints[i]):
            tmp.append(lpValues[pos+j])
        tmp = np.vstack((criteriaBreakPoints[i], tmp))
        valueFunctions.append(tmp)

    critSum = sum(criteriaNumberOfBreakPoints)
    test = a[:,:critSum]
    test2 = lpValues[:critSum]

    overallValues = np.dot(test, test2)
    errorValuesPlus = lpValues[critSum:critSum + numAlt]
    errorValuesMinus = lpValues[critSum + numAlt: critSum + 2*numAlt]


    return overallValues
    '''
    {
        'Optimum': lpsolution['fun'],
        'Value Functions': valueFunctions,
        'Overall values': overallValues,
        'errors': {
            'sigma minus': errorValuesMinus,
            'sigma plus': errorValuesPlus
        }
    }
    '''



if __name__ == '__main__':
    
    problem = MCDAProblem()
    problem.read_performance_table('performanceTable.csv')
    problem.read_criteria_min_max('criteriaMinMax.csv')
    problem.read_number_of_breakpoints('numberOfBreakPoints.csv')
    problem.read_alternatives_ranks('alternativesRanks.csv')

    A = utastar(problem)
    pprint(A)
