from entities.entities import *
import numpy as np
import matplotlib.pyplot as plt
import random
import copy
from datetime import datetime

SuperCounter = 0
IterCounter = None
Database = None
LeagueSizePerThread = 3
LeagueConcatingTimes = 20
LeagueLeaderChooseTimes = 10
CountOfLeagues = 50
SelectionFromLeagueSize = 3
SelectionCountInUpperLeague = 50
NameCollectionOfBaseThreads = ['J1', 'J2']
ParamsId = None
EnableFileWriting = False

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

def writeParamsToFile(name: str, param: DistributionParam, mode = 'a', iterNumber = None):
    if not EnableFileWriting:
        return
    if iterNumber != None:
        f = open(f"export/distrs_{iterNumber}.txt", mode)
    else:
        f = open(f"export/distrs.txt", mode)
    f.write(f"{name} mu: {param.mu} sigma: {param.sigma}\n")
    f.close()

def modellingBySixItems(iterNumber = None):
    field = []
    sizeOfField = LeagueSizePerThread
    selectionCount = LeagueConcatingTimes
    leaderSelectionCount = LeagueLeaderChooseTimes
    totalResults = {}
    nameCollectionOfBaseThread = NameCollectionOfBaseThreads
    distributions = {}

    mu = 0
    sigma = np.random.uniform(0, 5)
    for name in nameCollectionOfBaseThread:
        distributions[name] = DistributionParam(mu, sigma)
        writeParamsToFile(name, distributions[name], iterNumber=iterNumber)

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

    for iteration in range(selectionCount):
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

    # всего 6 элементов, сравниваются 4. А если победит кто-то простой.
    # Затем выбор по лигам. МОжет быть брать от 3 до 5 лидеров.
    totalSorted = sorted([[key, totalResults[key]] for key in totalResults], key=lambda item: item[1][0])
    return [totalSorted[-1][1][1], totalSorted[-2][1][1]]

def throwAwayFunction(_):
    global SuperCounter, IterCounter
    SuperCounter += 1
    print(SuperCounter)
    return modellingBySixItems(IterCounter)

def lotofTimeTries(iterNumber = None):
    global IterCounter
    IterCounter = iterNumber
    leaders = []
    leadersCnt = {}
    maxItemsInResult = SelectionFromLeagueSize
    leaderSelectionCount = SelectionCountInUpperLeague
    leaguesCount = CountOfLeagues
    from multiprocessing import Pool
    with Pool(4) as p:
        leaders = p.map(throwAwayFunction, range(leaguesCount))

    newLeaders = []
    for local in leaders:
        for x in local:
            leadersCnt[x.equation()] = (0, x)
            newLeaders.append(x)
    leaders = newLeaders

    for iteration in range(leaderSelectionCount):
        sortedLeaders = sorted([[x.getValue(), x] for x in leaders], key=lambda item:item[0])
        curLeader = leadersCnt[sortedLeaders[-1][1].equation()]
        leadersCnt[sortedLeaders[-1][1].equation()] = (curLeader[0]+1, curLeader[1])
        [x.unlockValue() for x in leaders]

    sortedByValue = dict(sorted(leadersCnt.items(), key=lambda item: -item[1][0]))

    if EnableFileWriting:
        if iterNumber != None:
            f = open(f"export/results_{iterNumber}.txt", "w")
        else:
            f = open("export/results.txt", "w")

        f.write('Top '+ str(maxItemsInResult) +' leaders:\n')
    iter = 0
    for key in sortedByValue:
        iter += 1
        if iter > maxItemsInResult:
            break
        value = sortedByValue[key]
        if Database != None:
            dbValue = value[1].toDict()
            dbValue['wins'] = value[0]
            dbValue['datetime'] = datetime.now()
            dbValue['params'] = ParamsId
            Database.results.insert_one(dbValue)
        if EnableFileWriting:
            f.write(str(key.expand()).replace("**", "^") + ':' + str(value[0]) + "\n")

    if EnableFileWriting:
        f.close()
    print("End of leaders")


def initExecutor():
    import pymongo
    global Database
    client = pymongo.MongoClient()
    Database = client['threads_modelling']


def modelingWithParams(leagueSizePerThread,
                       leagueConcatingTimes,
                       leagueLeaderChooseTimes,
                       countOfLeagues,
                       selectionFromLeagueSize,
                       selectionCountInUpperLeague,
                       nameCollectionOfBaseThreads,
                       modellingIterationsCount
                       ):
    global LeagueSizePerThread, LeagueConcatingTimes, LeagueLeaderChooseTimes
    global CountOfLeagues, SelectionFromLeagueSize, SelectionCountInUpperLeague
    global NameCollectionOfBaseThreads, ParamsId
    LeagueSizePerThread = leagueSizePerThread
    LeagueConcatingTimes = leagueConcatingTimes
    LeagueLeaderChooseTimes = leagueLeaderChooseTimes
    CountOfLeagues = countOfLeagues
    SelectionFromLeagueSize = selectionFromLeagueSize
    SelectionCountInUpperLeague = selectionCountInUpperLeague
    NameCollectionOfBaseThreads = nameCollectionOfBaseThreads
    ParamsId = Database.params.insert_one({
        'leagueSizePerThread': leagueSizePerThread,
        'leagueConcatingTimes': leagueConcatingTimes,
        'leagueLeaderChooseTimes': leagueLeaderChooseTimes,
        'countOfLeagues': countOfLeagues,
        'selectionFromLeagueSize': selectionFromLeagueSize,
        'selectionCounInUpperLeague': selectionCountInUpperLeague
    }).inserted_id

    for i in range(modellingIterationsCount):
        writeParamsToFile("Init", DistributionParam(0, 0), 'w')
        lotofTimeTries(i)

if __name__ == '__main__':
    # LeagueSizePerThread = 3
    # LeagueConcatingTimes = 20
    # LeagueLeaderChooseTimes = 10
    # CountOfLeagues = 50
    # SelectionFromLeagueSize = 3
    # SelectionCountInUpperLeague = 50
    nameCollectionOfBaseThreads = ['J1', 'J2']
    initExecutor()
    for leagueSizePerThread in range(4, 5):
        for leagueConcatingTimes in range(15, 50, 5):
            for leagueLeaderChooseTimes in range(10, 50, 5):
                for countOfLeagues in range(1, 100, 25):
                    for selectionFromLeagueSize in range(1, 5):
                        for selectionCountInUpperLeague in range(10, 11, 1):
                            modelingWithParams(leagueSizePerThread,
                                               leagueConcatingTimes,
                                               leagueLeaderChooseTimes,
                                               countOfLeagues,
                                               selectionFromLeagueSize,
                                               selectionCountInUpperLeague,
                                               nameCollectionOfBaseThreads,
                                               10)

