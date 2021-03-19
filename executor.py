from entities.entities import *
import numpy as np
import matplotlib.pyplot as plt
import random
import copy

SuperCounter = 0

def expander(entity: IThreadEntity):
    res = []
    if entity.canExpand():
        res += [copy.deepcopy(entity._first)]
        res += [copy.deepcopy(entity._second)]

    temp = factor(entity.equation())
    if entity.equation() == simplify('J1*J1+J1*J2+J2*J2'):
        return res
    if str(temp) == str(entity.equation()):
        return res
    return res

def writeParamsToFile(name: str, param: DistributionParam, mode = 'a'):
    f = open("export/distrs.txt", mode)
    f.write(f"{name} mu: {param.mu} sigma: {param.sigma}\n")
    f.close()

def modellingBySixItems():
    field = []
    sizeOfField = 3
    totalResults = {}
    nameCollectionOfBaseThread = ['J1', 'J2']
    distributions = {}

    mu = np.random.uniform(0, 3)
    sigma = np.random.uniform(0, 5)
    for name in nameCollectionOfBaseThread:
        distributions[name] = DistributionParam(mu, sigma)
        writeParamsToFile(name, distributions[name])

    for i in range(sizeOfField):
        for name in nameCollectionOfBaseThread:
            value = None
            if name == 'J1':
                value = EntityWithOriginalRandomDistribution(name, [ThreadLimitation(name, 1, sizeOfField)], distributions[name])
            elif name == 'J2':
                value = EntityWithNumpyDistribution(name, [ThreadLimitation(name, 1, sizeOfField)],
                                                                  distributions[name])
            else:
                continue
            field.append(value)

    for x in field:
        totalResults[x.equation()] = (0, x)

    for iteration in range(20):
        random.shuffle(field)
        first, second, field = field[0], field[1], field[2:]
        plusEntity = PlusEntity(first, second)
        multiplyEntity = MultiplyEntity(first, second)

        trl = [first, second, plusEntity, multiplyEntity]
        trl += expander(first)
        trl += expander(second)

        resDict = {}
        trl = [item for item in trl if item.isNormalCount()]
        [resDict.update({item: 0}) for item in trl]

        if len(trl) >= 2:
            for i in range(10):
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

    # всего 6 элементов, сравниваются 4. А если победит кто-то простой.
    # Затем выбор по лигам. МОжет быть брать от 3 до 5 лидеров.
    totalSorted = sorted([[key, totalResults[key]] for key in totalResults], key=lambda item: item[1][0])
    return [totalSorted[-1][1][1], totalSorted[-2][1][1]]

def throwAwayFunction(_):
    global SuperCounter
    SuperCounter += 1
    print(SuperCounter)
    return modellingBySixItems()

def lotofTimeTries():
    leaders = []
    leadersCnt = {}
    maxItemsInResult = 3
    from multiprocessing import Pool
    with Pool(4) as p:
        leaders = p.map(throwAwayFunction, range(50))

    newLeaders = []
    for local in leaders:
        for x in local:
            leadersCnt[x.equation()] = 0
            newLeaders.append(x)
    leaders = newLeaders

    for iteration in range(50):
        sortedLeaders = sorted([[x.getValue(), x] for x in leaders], key=lambda item:item[0])
        leadersCnt[sortedLeaders[-1][1].equation()] += 1
        [x.unlockValue() for x in leaders]

    sortedByValue = dict(sorted(leadersCnt.items(), key=lambda item: -item[1]))


    f = open("export/results.txt", "w")
    # f.write('Init leaders:\n')
    # for leader in leaders:
    #     f.write(str(leader.equation().expand()).replace("**", "^") + '\n')

    f.write('Top '+ str(maxItemsInResult) +' leaders:\n')
    iter = 0
    for key in sortedByValue:
        iter += 1
        if iter > maxItemsInResult:
            break
        value = sortedByValue[key]
        f.write(str(key.expand()).replace("**", "^") + ':' + str(value) + "\n")

    f.close()
    print("End of leaders")
    exit(0)



if __name__ == '__main__':
    writeParamsToFile("Init", DistributionParam(0, 0), 'w')
    lotofTimeTries()

