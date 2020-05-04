import matplotlib._color_data as mcd
from scipy import interpolate
import numpy as np
import csv
import os.path
from os import path

class Function(object):

    #_______________________________________________________________________________
    def __init__(self, name='func', file='data/br_B0p_eXN.csv'):

        self.x = []
        self.y = []

        if path.exists(file):
            with open(file) as csvfile:
                ## skip header
                next(csvfile)
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                id = 0
                for data in reader:
                    self.x.append(float(data[0]))
                    self.y.append(float(data[1]))


    #_______________________________________________________________________________
    def eval(self, x):
        tck = interpolate.splrep(self.x, self.y)
        val =  interpolate.splev(x, tck)
        return val

    #_______________________________________________________________________________
    def clear_data(self):
        self.x = []
        self.y = []

    #_______________________________________________________________________________
    def scale_data(self, scale=1.0):

        xr = []
        yr = []

        for x, y in zip(self.x,self.y):
            xr.append(x*scale)
            yr.append(y*scale)

        self.x = xr
        self.y = yr
