from sympy import *


class IThreadEntity:
    def __init__(self, formula: str, equation: Symbol, canExpand: bool = False):
        self._name = formula
        self._equation = equation
        self._canExpand = canExpand
        self._lockedValue = False
        self._value = None

    def name(self):
        return self._name

    def equation(self):
        return self._equation

    def canExpand(self):
        return self._canExpand

    def calcValue(self):
        raise NotImplemented

    def getValue(self):
        if not self._lockedValue:
            self._value = self.calcValue()
            self._lockedValue = True
        return self._value

    def isNotNullable(self, items:dict):
        tmpRes = self._equation.subs(items)
        return tmpRes != 0

    def unlockValue(self):
        self._lockedValue = False