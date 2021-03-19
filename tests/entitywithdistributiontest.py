from entities.entities import EntityWithNumpyDistribution, EntityWithOriginalRandomDistribution, ThreadLimitation, DistributionParam

if __name__ == '__main__':
    testNumpy = EntityWithNumpyDistribution('J1', [ThreadLimitation('J1', 1, 1)], DistributionParam(0, 1))
    testNumpy.exportImage('entity_numpy')

    testOriginal = EntityWithOriginalRandomDistribution('J1', [ThreadLimitation('J1', 1, 1)], DistributionParam(0, 1))
    testOriginal.exportImage('entity_original')