from .ithreadentity import IThreadEntity
import copy

class PlusEntity(IThreadEntity):
    def __init__(self, first: IThreadEntity, second: IThreadEntity):
        self._first = first #copy.copy(first)
        self._second = second #copy.copy(second)
        if first.canExpand() or second.canExpand():
            name = '(' + first.name() + ')+(' + second.name() + ')'
        else:
            name = first.name() + '+' + second.name()
        equation = first.equation() + second.equation()

        super(PlusEntity, self).__init__(name, equation, copy.deepcopy(first.limitation), True)
        for item in second.limitation:
            self.modifyLimitations(item)


    def __str__(self):
        return self.name()

    def toDict(self):
        res = super(PlusEntity, self).toDict()
        res['e_type'] = 'plus'
        res['first'] = self._first.toDict()
        res['second'] = self._second.toDict()
        return res

    def calcValue(self):
        return self._first.getValue() + self._second.getValue()