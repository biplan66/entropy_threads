from entities.entities import *
import numpy as np
import matplotlib.pyplot as plt
import random

MULTIPLY_SELECTION_COUNT = 20
PLUS_SELECTION_COUNT = 10
MULTIPLY_LEADER_SELECTION = 100
PLUS_LEADER_SELECTION = 100

Mu = 0
Sigma = 0

def expander(entity: IThreadEntity, applyOneOperation = None):
    if applyOneOperation is None and (isinstance(entity, MultiplyEntity) or isinstance(entity, PlusEntity)):
        return [copy.deepcopy(entity._first), copy.deepcopy(entity._second)]
    elif applyOneOperation == 'plus' and isinstance(entity, PlusEntity):
        return [copy.deepcopy(entity._first), copy.deepcopy(entity._second)]
    elif applyOneOperation == 'multiply' and isinstance(entity, MultiplyEntity):
        return [copy.deepcopy(entity._first), copy.deepcopy(entity._second)]

    return []

def SelectionMultiplyThrowAway(field):
    return SelectionByMultiply(copy.deepcopy(field), MULTIPLY_SELECTION_COUNT, MULTIPLY_LEADER_SELECTION)

def SelectionPlusThrowAway(field):
    return SelectionByPlus(copy.deepcopy(field), PLUS_SELECTION_COUNT, PLUS_LEADER_SELECTION)

def SelectionByMultiply(field: list, selectionCount: int, leaderSelectionCount: int):
    totalResults = {}

    for x in field:
        totalResults[x.equation()] = (0, x)

    for iteration in range(selectionCount):
        hasBaseByJ1 = any([1 for x in field if x.name() == 'J1'])
        hasBaseByJ2 = any([1 for x in field if x.name() == 'J2'])
        if not hasBaseByJ1:
            value = EntityWithOriginalRandomDistribution('J1', [ThreadLimitation('J1', 1, 2)],
                                                             DistributionParam(Mu, Sigma))
            field.append(value)
        if not hasBaseByJ2:
            value = EntityWithOriginalRandomDistribution('J2', [ThreadLimitation('J2', 1, 2)],
                                                    DistributionParam(Mu, Sigma))

            field.append(value)

        random.shuffle(field)
        first, second, field = field[0], field[1], field[2:]
        if (first.name() == 'J1' and second.name() == 'J2'
                or first.name() == 'J2' and second.name() == 'J1'):
            print("Ta da")
        multiplyEntity = MultiplyEntity(first, second)

        trl = [first, second, multiplyEntity]
        trl += expander(first, 'musltiply')
        trl += expander(second, 'mulstiply')

        resDict = {}
        trl = [item for item in trl if item.isNormalCount()]
        [resDict.update({item: 0}) for item in trl]

        if len(trl) >= 2:
            for i in range(leaderSelectionCount):
                sortedItems = sorted([[item.getValue(), item] for item in trl], key=lambda item: item[0])
                resDict[sortedItems[-1][1]] += 1
                resDict[sortedItems[-2][1]] += 1
                [item.unlockValue() for item in trl]
            for key in resDict:
                if key.isNotNullable({'J1': 0, 'J2': 0}):
                    del resDict[key]
            res = sorted([[key, resDict[key]] for key in resDict], key=lambda item: item[1])
            del resDict
            if len(res) > 1:
                field.append(res[-2][0])
                if res[-2][0].equation() not in totalResults:
                    totalResults[res[-2][0].equation()]  = (0, res[-2][0])

                totalResults[res[-2][0].equation()] = (
                    totalResults[res[-2][0].equation()][0] + 1, totalResults[res[-2][0].equation()][1])

            field.append(res[-1][0])
            if res[-1][0].equation() not in totalResults:
                totalResults[res[-1][0].equation()] = (0, res[-1][0])
            totalResults[res[-1][0].equation()] = (
            totalResults[res[-1][0].equation()][0] + 1, totalResults[res[-1][0].equation()][1])
            del res
    totalSorted = sorted([[key, totalResults[key]] for key in totalResults], key=lambda item: item[1][0])

    # [print(x.name()) for x in field]
    return [totalSorted[-1][1][1], totalSorted[-2][1][1]]

def SelectionByPlus(field: list, selectionCount: int, leaderSelectionCount: int):
    totalResults = {}

    initialThreads = copy.deepcopy(field)
    initialThreads.append(EntityWithOriginalRandomDistribution('J1', [ThreadLimitation('J1', 1, 3)],
                                                             DistributionParam(Mu, Sigma)))
    initialThreads.append(EntityWithOriginalRandomDistribution('J2', [ThreadLimitation('J2', 1, 3)],
                                                             DistributionParam(Mu, Sigma)))

    for x in field:
        totalResults[x.equation()] = (0, x)

    for iteration in range(selectionCount*10):
        for item in initialThreads:
            if not any([x for x in field if x.name() == item.name()]):
                field.append(copy.deepcopy(item))
        random.shuffle(field)
        first, second, field = field[0], field[1], field[2:]
        plusEntity = PlusEntity(first, second)

        trl = [first, second, plusEntity]
        trl += expander(first, 'plus')
        trl += expander(second, 'plus')

        resDict = {}
        trl = [item for item in trl if item.isNormalCount()]
        [resDict.update({item: 0}) for item in trl]

        if len(trl) >= 2:
            for i in range(leaderSelectionCount):
                sortedItems = sorted([[item.getValue(), item] for item in trl], key=lambda item: item[0])
                resDict[sortedItems[-1][1]] += 1
                resDict[sortedItems[-2][1]] += 1
                [item.unlockValue() for item in trl]
            for key in resDict:
                if key.isNotNullable({'J1': 0, 'J2': 0}):
                    del resDict[key]
            res = sorted([[key, resDict[key]] for key in resDict], key=lambda item: item[1])
            del resDict
            if len(res) > 1:
                field.append(res[-2][0])
                if res[-2][0].equation() not in totalResults:
                    totalResults[res[-2][0].equation()] = (0, res[-2][0])

                totalResults[res[-2][0].equation()] = (
                    totalResults[res[-2][0].equation()][0] + 1, totalResults[res[-2][0].equation()][1])

            field.append(res[-1][0])
            if res[-1][0].equation() not in totalResults:
                totalResults[res[-1][0].equation()] = (0, res[-1][0])
            totalResults[res[-1][0].equation()] = (
                totalResults[res[-1][0].equation()][0] + 1, totalResults[res[-1][0].equation()][1])
            del res

    totalSorted = sorted([[key, totalResults[key]] for key in totalResults], key=lambda item: item[1][0])
    return [totalSorted[-1][1][1], totalSorted[-2][1][1]]

def SelectBestEquations(field: list, leaderSelectionCount: int):
    resDict = {}
    trl = [item for item in field if item.isNormalCount()]
    [resDict.update({item: 0}) for item in trl]

    for i in range(leaderSelectionCount):
        sortedItems = sorted([[item.getValue(), item] for item in trl], key=lambda item: item[0])
        resDict[sortedItems[-1][1]] += 1
        resDict[sortedItems[-2][1]] += 1
        [item.unlockValue() for item in trl]

    for key in resDict:
        if key.isNotNullable({'J1': 0, 'J2': 0}):
            del resDict[key]
    res = sorted([[key, resDict[key]] for key in resDict], key=lambda item: item[1])
    del resDict
    return res

def convertFromArrayOfArray(fieldOfFields:list):
    res = []
    for item in fieldOfFields:
        if isinstance(item, list):
            res += item
        else:
            res += [item]
    return res

def parallelRunner(field, func, sizeFieldOfFields = 20):
    fieldOfFields = []
    for _ in range(sizeFieldOfFields):
        fieldOfFields.append(field)

    from multiprocessing import Pool
    with Pool(4) as p:
        return convertFromArrayOfArray(p.map(func, fieldOfFields))

def modelling(sizeOfField, threadLimitation:int, nameCollectionOfBaseThread = ['J1', 'J2']):
    field = []
    distributions = {}

    global mu, sigma
    mu = 0
    sigma = np.random.uniform(0, 5)
    for name in nameCollectionOfBaseThread:
        distributions[name] = DistributionParam(mu, sigma)

        # writeParamsToFile(name, distributions[name], iterNumber=iterNumber)

    for i in range(sizeOfField):
        for name in nameCollectionOfBaseThread:
            value = None
            if name == 'J1':
                value = EntityWithOriginalRandomDistribution(name, [ThreadLimitation(name, 1, 2, 2)],
                                                             distributions[name])
            elif name == 'J2':
                value = EntityWithOriginalRandomDistribution(name, [ThreadLimitation(name, 1, 2, 2)],
                                                    distributions[name])
            else:
                continue
            field.append(value)

    iterationCount = 20
    # field = parallelRunner(field, SelectionMultiplyThrowAway, iterationCount)
    # for fieldItem in field:
    #     for name in nameCollectionOfBaseThread:
    #         fieldItem.setMaxLimitation(name, 3)
    #         fieldItem.setMaxTerms(None)
    #
    # field = parallelRunner(field, SelectionPlusThrowAway, int(50))#iterationCount/2 + 1))

    t = SelectBestEquations(field, 100)
    t = sorted(t, key=lambda item: item[1])
    for item in t[-3:]:
        print(item[0], item[1])


if __name__ == '__main__':
    modelling(4, 3)
