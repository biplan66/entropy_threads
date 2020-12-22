from sympy import *
import numpy as np
import copy

class ThreadLimitation:
    def __init__(self, paramName: str, curValue: int, maxValue: int):
        self.paramName = paramName
        self.curValue = curValue
        self.maxValue = maxValue

    def __str__(self):
        return self.paramName + ':' + str(self.curValue) + '/' + str(self.maxValue)

    def isNormalCount(self):
        return self.curValue <= self.maxValue

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


    def equation(self):
        return self._equation

    def setEquation(self, equation:Symbol):
        self._equation = equation

    def canExpand(self):
        return self._canExpand

    def calcValue(self):
        raise NotImplemented

    def getValue(self):
        if not self._lockedValue:
            self._value = self.equation().subs({"J1":np.random.normal(0, 1), "J2":np.random.normal(0, 1)})
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
        if not auto:
            a=10
        return auto
        # paramNames = [key[:-len('_cur')] for key in self.limitation if key.endswith('_cur')]
        # for name in paramNames:
        #     if self.limitation[name + '_cur'] > self.limitation[name + '_max']:
        #         return False

        # return True
