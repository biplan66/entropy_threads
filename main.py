from entities.entities import *
import numpy as np
import matplotlib.pyplot as plt

def joiner(s : str, n = 25):
    return "\n".join([s[i:i + n] for i in range(0, len(s) - (len(s) % n), n)])

if __name__ == '__main__':

    field = []
    for i in range(25):
        field.append(SimpleEntity('J1'))
        field.append(SimpleEntity('J2'))

    for iteration in range(10000):
        print(iteration)
        firstElem = int(np.random.uniform(0, len(field)))
        secondElem = int(np.random.uniform(0, len(field)))
        while firstElem == secondElem:
            secondElem = int(np.random.uniform(0, len(field)))

        first, second = field[firstElem], field[secondElem]
        plusEntity = PlusEntity(first, second)
        multiplyEntity = MultiplyEntity(first, second)
        resDict = {first: 0, second: 0, plusEntity: 0, multiplyEntity: 0}
        trl = [first, second, plusEntity, multiplyEntity]
        if first.canExpand():
            tmp1 = first._first
            tmp2 = first._second
            trl += [tmp1, tmp2]
            resDict[tmp1] = 0
            resDict[tmp2] = 0
            del tmp1
            del tmp2

        if second.canExpand():
            tmp1 = second._first
            tmp2 = second._second
            trl += [tmp1, tmp2]
            resDict[tmp1] = 0
            resDict[tmp2] = 0
            del tmp1
            del tmp2

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

        if iteration % 30 == 0:
            res = {}
            for item in field:
                simplified = item.equation().expand()
                item.setEquation(simplified)
                if simplified not in res:
                    res[simplified] = 0
                res[simplified] += 1
            x = []
            y = []
            for key in res:
                x.append(str(key).replace('**','^'))
                y.append(res[key])

            position = np.arange(len(res))
            del res

            fig, ax = plt.subplots(figsize=(15,15))

            # ax.barh(x, y)
            ax.hist([str(x.equation()) for x in field])
            # ax.set_yticks(position)
            fig.suptitle("Iteration: " +str(iteration))
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
            #  Устанавливаем подписи тиков
            # labels = ax.set_yticklabels(x,
            #                             fontsize=8,  # Размер шрифта
            #                             color='b',  # Цвет текста
            #                             rotation=45,  # Поворот текста
            #                             verticalalignment='center')  # Вертикальное выравнивание
            fig.savefig("export/" + str(iteration)+".png")
            # fig.show()
            del x
            del y

    print("Main")