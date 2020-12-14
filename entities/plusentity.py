from .ithreadentity import IThreadEntity
import copy

class PlusEntity(IThreadEntity):
    def __init__(self, first: IThreadEntity, second: IThreadEntity):
        self._first = copy.copy(first)
        self._second = copy.copy(second)
        if first.canExpand() or second.canExpand():
            name = '(' + first.name() + ')+(' + second.name() + ')'
        else:
            name = first.name() + '+' + second.name()
        equation = first.equation() + second.equation()

        super(PlusEntity, self).__init__(name, equation, True)

    def __str__(self):
        return self.name()

    def calcValue(self):
        return self._first.getValue() + self._second.getValue()