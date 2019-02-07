from matplotlib import pyplot as plt
import numpy as np
import matplotlib.mlab as mlab


class PlotGenerator:

    def __init__(self, x, y=1, title="Plot"):
        self._x = x
        self._y = y
        self._title = title

    def plot_and_save_hist(self, bins=30, normal_dist=False):
        x = self._x
        title = self._title
        x_mean = np.round(np.mean(x), 2) # mu
        x_std = np.round(np.std(x), 2) # sigma
        plt.clf()

        if normal_dist:
            fig, ax = plt.subplots()
            ax.hist(x, bins, density=1)
            k = np.linspace(x_mean - 3 * x_std, x_mean + 3 * x_std, 100)
            ax.plot(k, mlab.normpdf(k, x_mean, x_std))
        else:
            fig, ax = plt.subplots()
            ax.hist(x, bins)

        ax.set_xlabel('Values')
        ax.set_ylabel('Counts')
        # plt.xlim(0)
        plt.title("Histogram of " + title + " ($\mu=" + str(x_mean) + "$, $\sigma=" + str(x_std) + "$)")
        plt.savefig('app/static/images/histogram.png')
        print("histogram genereted")
        return

