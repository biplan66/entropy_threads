from .ithreadentity import IThreadEntity, ThreadLimitation
from sympy import Symbol
import numpy as np

class DistributionParam:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def toDict(self):
        return {
            'mu': self.mu,
            'sigma': self.sigma
        }

class EntityWithDistribution(IThreadEntity):
    def __init__(self,
                 formula: str,
                 limitation: list,
                 randomDistribution,
                 distribuionParams = DistributionParam(0, 1)):
        super().__init__(formula, Symbol(formula), limitation)
        self.distribution = randomDistribution
        self.param = distribuionParams

    def __str__(self):
        return self.name()

    def toDict(self):
        res = super(EntityWithDistribution, self).toDict()
        res['distribution'] = self.param.toDict()
        return res

    def calcValue(self):
        return self.distribution(self.param.mu, self.param.sigma)

    def exportImage(self, prefixPath = None):
        import numpy as np
        import matplotlib.pyplot as plt

        if prefixPath is None:
            prefixPath = self.name()
        values = []
        for _ in range(1000):
            self.calcValue()
            values.append(self.getValue())

        values = np.array(values, dtype=float)

        fig, ax = plt.subplots(figsize=(15, 15))
        _, _, _ = ax.hist(values, 20, density=1, alpha=0.5)
        fig.savefig(str(prefixPath) + "_" + str(self.param.mu) + '-' + str(self.param.sigma) + ".png")


class EntityWithNumpyDistribution(EntityWithDistribution):
    def __init__(self, formula: str, limitation: list, distributionParams: DistributionParam):
        super().__init__(formula, limitation, np.random.normal, distributionParams)


class EntityWithOriginalRandomDistribution(EntityWithDistribution):
    def __init__(self, formula: str, limitation: list, distributionParams: DistributionParam):
        import random
        super().__init__(formula, limitation, random.gauss, distributionParams)