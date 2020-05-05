import matplotlib.pyplot as plt
import numpy as np
from Limit import *
from Model import *


class ExclusionPlot(object):

    #_______________________________________________________________________________
    def __init__(self, name='dummy', xlabel='xlabel', ylabel='ylabel',
                 xmin=0.0, xmax=10.0, ymin=1.e-3, ymax=1.e-1,
                 model='MajoranaNeutrinoElectron',
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

        self.model = model

    #_______________________________________________________________________________
    def add_limit(self, limit):
        self.ax.fill(limit.x_data, limit.y_data,
                     color=limit.color,  alpha=limit.alpha)

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
