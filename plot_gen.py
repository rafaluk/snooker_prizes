from matplotlib import pyplot as plt
import numpy as np
from DataPrepare import DataPrepare


class PlotGenerator:

    @staticmethod
    def plot_and_save():
        x = np.arange(1, 100, 10)
        y = np.random.rand(10)
        plt.clf()
        plt.plot(x, y)
        plt.savefig('app/static/images/wykresso.png')
        print("plot genereted")
        return

