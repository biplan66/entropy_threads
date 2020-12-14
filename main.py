from entities.entities import *
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    field = []
    for i in range(25):
        field.append(SimpleEntity('J1'))
        field.append(SimpleEntity('J2'))

    for iteration in range(100):
        firstElem = int(np.random.uniform(0, len(field)))
        secondElem = int(np.random.uniform(0, len(field)))
        while firstElem == secondElem:
            secondElem = int(np.random.uniform(0, len(field)))

        first, second = field[firstElem], field[secondElem]
        plusEntity = PlusEntity(first, second)
        multiplyEntity = MultiplyEntity(first, second)
        resDict = {first: 0, second: 0, plusEntity: 0, multiplyEntity: 0}
        trl = [first, second, plusEntity, multiplyEntity]
        for i in range(10):
            sortedItems = sorted([[item.getValue(), item] for item in trl], key=lambda item: item[0])
            resDict[sortedItems[-1][1]]+=1
            resDict[sortedItems[-2][1]]+=1
            [item.unlockValue() for item in trl]
        for key in resDict:
            if key.isNotNullable({'J1':0, 'J2':0}):
                del resDict[key]
        res = sorted([[key, resDict[key]] for key in resDict], key=lambda item: item[1])
        del resDict
        field[firstElem] = res[-2][0]
        field[secondElem] = res[-1][0]
        del res

        if iteration % 10 == 0:
            res = {}
            for item in field:
                simplified = item.equation().simplify()
                if simplified not in res:
                    res[item.equation().simplify()] = 0
                res[item.equation().simplify()] += 1
            x = []
            y = []
            for key in res:
                x.append(str(key))
                y.append(res[key])

            position = np.arange(len(res))
            del res

            plt.title("Iteration: " +str(iteration))
            plt.barh(x, y)
            plt.savefig("export/" + str(iteration)+".png")
            plt.close()
            del x
            del y

    print("Main")