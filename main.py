from entities.entities import *
import numpy as np
import matplotlib.pyplot as plt
import random
import copy

def joiner(s : str, n = 25):
    return "\n".join([s[i:i + n] for i in range(0, len(s) - (len(s) % n), n)])

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

    # abcd = str(temp).replace('**', '^').split('*')
    # if len(abcd) <= 1:
    #     return res
    # firstTerm = sympify(abcd[0])
    # secondTerm = temp / firstTerm
    # if firstTerm.subs({'J1':0, 'J2': 0}) == 0 or secondTerm.subs({'J1':0, 'J2':0}) == 0:
    #     return res
    t = 0
    return res

def test():
    field = []
    sizeOfField = 3
    for i in range(sizeOfField):
        field.append(SimpleEntity('J1', [ThreadLimitation('J1', 1, sizeOfField)]))
        field.append(SimpleEntity('J2', [ThreadLimitation('J2', 1, sizeOfField)]))
    multiply1 = MultiplyEntity(field[0], field[1])
    multiply2 = MultiplyEntity(field[2], field[4])
    multiply3 = MultiplyEntity(field[3], field[5])
    plus1 = PlusEntity(multiply1, multiply2)
    plus2 = PlusEntity(plus1, multiply3)
    return (multiply1.isNormalCount() and multiply2.isNormalCount() and multiply3.isNormalCount() and plus1.isNormalCount() and plus2.isNormalCount())

if __name__ == '__main__':
    if not test():
        raise Exception("Test failed")
        exit(1)

    field = []
    sizeOfField = 15
    for i in range(sizeOfField):
        field.append(SimpleEntity('J1', [ThreadLimitation('J1', 1, sizeOfField)]))
        field.append(SimpleEntity('J2', [ThreadLimitation('J2', 1, sizeOfField)]))

    for iteration in range(100000):
        print(iteration)
        firstElem = int(np.random.uniform(0, len(field)))
        secondElem = int(np.random.uniform(0, len(field)))
        while firstElem == secondElem:
            secondElem = int(np.random.uniform(0, len(field)))

        first, second = field[firstElem], field[secondElem]
        print([len(first.name()), len(second.name())])
        plusEntity = PlusEntity(first, second)
        multiplyEntity = MultiplyEntity(first, second)
        trl = [first, second, plusEntity, multiplyEntity]
        trl += expander(first)
        trl += expander(second)
        # if first.canExpand() and np.random.uniform(0, 1) > 0.5:
        #     tmp1 = first._first
        #     tmp2 = first._second
        #     tmp1.limitation = copy.deepcopy(first.limitation)
        #     tmp2.limitation = copy.deepcopy(second.limitation)
        #     trl += [tmp1, tmp2]
        #     # del tmp1
        #     # del tmp2
        #
        # if second.canExpand() and np.random.uniform(0, 1) > 0.5:
        #     tmp1 = second._first
        #     tmp2 = second._second
        #     tmp1.limitation = copy.deepcopy(first.limitation)
        #     tmp2.limitation = copy.deepcopy(second.limitation)
        #     trl += [tmp1, tmp2]
        #     # del tmp1
        #     # del tmp2
        resDict = {}
        trl = [item for item in trl if item.isNormalCount()]
        [resDict.update({item: 0}) for item in trl]

        if len(trl) >= 2:
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
            if len(res) > 1:
                field[firstElem] = res[-2][0]
            field[secondElem] = res[-1][0]
            del res

        if iteration % 100 == 0:
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
            ax.hist([str(x.equation()).replace('**', '^') for x in field])
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