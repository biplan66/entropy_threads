from .ithreadentity import IThreadEntity
import copy

class MultiplyEntity(IThreadEntity):
    def __init__(self, first: IThreadEntity, second: IThreadEntity):
        self._first = first#copy.copy(first)
        self._second = second #copy.copy(second)
        if first.canExpand() or second.canExpand():
            name = '(' + first.name() + ')*(' + second.name() + ')'
        else:
            name = first.name() + '*' + second.name()
        equation = first.equation() * second.equation()

        super(MultiplyEntity, self).__init__(name, equation, copy.deepcopy(first.limitation), True)
        for item in second.limitation:
            self.modifyLimitations(item)

    def toDict(self):
        res = super(MultiplyEntity, self).toDict()
        res['e_type'] = 'mult'
        res['first'] = self._first.toDict()
        res['second'] = self._second.toDict()
        return res

    def __str__(self):
        return self.name()

    def calcValue(self):
        return self._first.getValue() * self._second.getValue()