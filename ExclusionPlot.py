import matplotlib.pyplot as plt
import numpy as np
from Limit import *
from Model import *


class ExclusionPlot(object):

    #_______________________________________________________________________________
    def __init__(self, name='dummy', xlabel='xlabel', ylabel='ylabel',
                 xmin=0.0, xmax=10.0, ymin=1.e-3, ymax=1.e-1,
                 dimx=7, dimy=5,
                 logx=True, logy=True):

        fig, ax = plt.subplots(figsize=(dimx, dimy))

        self.fig = fig
        self.ax = ax

        self.name = name
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.xmin = xmin
        self.xmax = xmax

        self.ymin = ymin
        self.ymax = ymax

        self.logx = logx
        self.logy = logy

    #_______________________________________________________________________________
    def add_limit(self, limit):


        x_data = limit.x_data
        y_data = limit.y_data

        x_data.append(10)
        y_data.append(0.01)
        x_data.append(0.1)
        y_data.append(0.01)
        x_data.append(0.1)
        y_data.append(0.00001)

        print(x_data)
        print(y_data)


        self.ax.fill(x_data, y_data,
                             color=limit.color,  alpha=limit.alpha)

        #self.ax.scatter(limit.x_data, limit.y_data, color='r')

    #_______________________________________________________________________________
    def plot(self):

        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)

        if self.logx:
            self.ax.set_xscale('log')
        if self.logy:
            self.ax.set_yscale('log')

        self.fig.tight_layout()

        filename = '{}.png'.format(self.name)
        self.fig.savefig('plots/{}'.format(filename))
        print('')
        print('created plots/{}'.format(filename))
