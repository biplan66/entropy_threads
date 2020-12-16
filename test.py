import numpy as np
import matplotlib.pyplot as plt

def testSubPlots():
    labels = ['Контрольная\nгруппа № %i' % i for i in range(1, 6)]
    value = (12, 24, 18, 11, 6)
    position = np.arange(5)

    fig, ax = plt.subplots()

    ax.barh(position, value)

    #  Устанавливаем позиции тиков:
    ax.set_yticks(position)

    #  Устанавливаем подписи тиков
    ax.set_yticklabels(labels,
                       fontsize=15)

    fig.set_figwidth(10)
    fig.set_figheight(6)

    plt.show()

if __name__ == '__main__':
    from random import gauss
    rands = [gauss(0, 1) for x in range(1000)]
    rands = np.random.normal(0, 1, 1000)
    rands = [np.random.normal(0, 1) for x in range(1000)]
    values = {}
    for x in rands:
        if x not in values:
            values[x] = 0
        values[x] += 1
    fig, ax = plt.subplots()

    ax.hist(rands, 30)
    fig.show()

    import matplotlib.pyplot as plt

    mu, sigma = 0, 1 # mean and standard deviation

    s = np.random.normal(mu, sigma, 1000)

    count, bins, ignored = plt.hist(s, 30)

    # plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) *
    #
    #          np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2)),
    #
    #          linewidth=2, color='r')

    plt.show()



