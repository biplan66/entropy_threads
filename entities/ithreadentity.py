from sympy import *
import numpy as np
import copy

class ThreadLimitation:
    def __init__(self, paramName: str, curValue: int, maxValue: int, maxTerms: int = None):
        self.paramName = paramName
        self.curValue = curValue
        self.maxValue = maxValue
        self.maxTerms = maxTerms

    def toDict(self):
        return {
            'paramName': self.paramName,
            'curValue': self.curValue,
            'maxValue': self.maxValue
        }

    def __str__(self):
        return self.paramName + ':' + str(self.curValue) + '/' + str(self.maxValue)

    def isNormalCount(self):
        return self.curValue <= self.maxValue

    def getMaxTerms(self):
        return self.maxTerms

    def setMaxTerms(self, newTerm: int):
        self.maxTerms = newTerm

    def getCurValue(self):
        return self.curValue

    def modifyCurValue(self, addToCurValue: int):
        self.curValue += addToCurValue


class IThreadEntity:
    def __init__(self, formula: str, equation: Symbol, limitation: list, canExpand: bool = False):
        if limitation is None:
            limitation = {}
        self._name = formula
        self._equation = equation
        self._canExpand = canExpand
        self._lockedValue = False
        self._value = None
        self.limitation = limitation

    def toDict(self):
        return {
            'equation': str(self._equation.expand()).replace("**", "^"),
            'limitation': [x.toDict() for x in self.limitation]
        }

    def name(self):
        return self._name

    def modifyLimitations(self, newLimit: ThreadLimitation):
        modified = False
        for myLimit in self.limitation:
            if myLimit.paramName != newLimit.paramName:
                continue
            myLimit.modifyCurValue(newLimit.curValue)
            modified = True
            break
        if not modified:
            self.limitation.append(copy.copy(newLimit))

    def setMaxLimitation(self, name:str, newMax:int):
        for myLimit in self.limitation:
            if myLimit.paramName != name:
                continue
            myLimit.maxValue = newMax

    def setMaxTerms(self, newMaxTerms: int):
        for myLimit in self.limitation:
            myLimit.setMaxTerms(newMaxTerms)


    def equation(self):
        return self._equation

    def setEquation(self, equation:Symbol):
        self._equation = equation

    def canExpand(self):
        return self._canExpand

    def calcValue(self):
        raise NotImplemented

    def getValue(self):
        from random import gauss
        if not self._lockedValue:
            self._value = self.equation().subs({"J1": gauss(0, 1), "J2":np.random.normal(0, 1)})
            # self._value = self.equation().subs({"J1":np.random.normal(0, 1), "J2":np.random.normal(0, 1)})
        return self._value
        # old stuff
        if not self._lockedValue:
            self._value = self.calcValue()
            self._lockedValue = True
        return self._value

    def isNotNullable(self, items:dict):
        tmpRes = self._equation.subs(items)
        return tmpRes != 0

    def unlockValue(self):
        self._lockedValue = False

    def isNormalCount(self):
        auto = all([item.isNormalCount() for item in self.limitation])
        maxTerms = [item.getMaxTerms() for item in self.limitation if item.getMaxTerms() != None]
        if len(maxTerms) > 0:
            maxTerms = min(maxTerms)
        else:
            maxTerms = None
        totalTerms = sum([item.getCurValue() for item in self.limitation])
        if not auto:
            a=10
        return auto and (maxTerms != None and totalTerms <= maxTerms or maxTerms == None)
        # paramNames = [key[:-len('_cur')] for key in self.limitation if key.endswith('_cur')]
        # for name in paramNames:
        #     if self.limitation[name + '_cur'] > self.limitation[name + '_max']:
        #         return False

        # return True
