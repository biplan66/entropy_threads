from .ithreadentity import IThreadEntity
from sympy import Symbol
import numpy as np


class SimpleEntity(IThreadEntity):
    def __init__(self, name, limitation):
        super(SimpleEntity, self).__init__(name, Symbol(name), limitation, False)

    def __str__(self):
        return self.name()

    def calcValue(self):
        return np.random.normal(0, 1)
