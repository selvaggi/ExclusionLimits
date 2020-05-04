import matplotlib._color_data as mcd
import numpy as np

class Limit(object):

    #_______________________________________________________________________________
    def __init__(self, name='limit', color='blue', alpha=0.5):

        self.name = name
        self.color = mcd.XKCD_COLORS["xkcd:{}".format(color)].upper()

        self.alpha = alpha

        self.x_data = []
        self.y_data = []

    #_______________________________________________________________________________
    def add_point(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

    #_______________________________________________________________________________
    def clear_data(self):
        self.x_data = []
        self.y_data = []

    #_______________________________________________________________________________
    def set_data(self, x, y):
        self.x_data = x
        self.y_data = y

    #_______________________________________________________________________________
    def set_func(self, func):
        self.x_data = [float(i) for i in func.x]
        self.y_data = [float(i) for i in func.y]
