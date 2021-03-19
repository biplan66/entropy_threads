import numpy as np
import matplotlib.pyplot as plt

def npPlot(mu = 0, sigma = 1.0):

    s = np.random.normal(mu, sigma, 1000)

    fig, ax = plt.subplots(figsize=(15, 15))
    _, bins, _ = ax.hist(s, 20, density=1, alpha=0.5)
    fig.savefig("export/normal_first_" + str(mu) + '-' + str(sigma) + ".png")
    a = 10


def pythonGauss(mu = 0, sigma = 1.0):
    from random import gauss

    s = [gauss(mu, sigma) for _ in range(1000)]

    fig, ax = plt.subplots(figsize=(15, 15))
    _, bins, _ = ax.hist(s, 20, density=1, alpha=0.5)
    fig.savefig("export/normal_second_" + str(mu) + '-' + str(sigma) + ".png")

if __name__ == '__main__':
    mu = 0
    sigma = 1/5
    npPlot(mu, sigma)
    pythonGauss(mu, sigma)