from ExclusionPlot import *
from Limit import *
from Function import *
from Model import *
from collections import OrderedDict
from scipy import optimize
import numpy as np


debug=True

#_______________________________________________________________________________
def best_limit(ExclusionPlot, parameters, target=10., npoints=100):

    xlist = []
    if ExclusionPlot.logx:
        xlist = np.logspace(np.log10(ExclusionPlot.xmin), np.log10(ExclusionPlot.xmax), num=npoints)
    else:
        xlist = np.linspace((ExclusionPlot.xmin, ExclusionPlot.xmax), num=npoints)


    if ExclusionPlot.logy:
        ylist = np.logspace(np.log10(ExclusionPlot.ymin), np.log10(ExclusionPlot.ymax), num=npoints)
    else:
        ylist = np.linspace((ExclusionPlot.ymin, ExclusionPlot.ymax), num=npoints)

    sols = []

    ## add first and last values for best polygon perf.

    sols.append(ExclusionPlot.ymax)

    ### looping over masses and computing coupling that best matches target
    for x in xlist:

        def f(y):
            for decay_mode in parameters.list_brs:

                model_class = globals()[ExclusionPlot.model]
                model = model_class(parameters, mass=x, coupling=y)

                model.compute_lifetime()
                model.compute_branching_ratios(parameters.list_brs)

                z = model.event_yield()
                #print(x,z)
                return z-target


        sol = ExclusionPlot.ymax

        fys = []

        sg = np.sign(f(ExclusionPlot.ymin))

        ymin=ExclusionPlot.ymin
        ymax=ExclusionPlot.ymax

        for y in ylist:

            val = f(y)
            #print ('finding zeros', y, val)
            if np.sign(val) == sg:
                ymin = y
                ymax = y
            else:
                ymax = y
                break

        #print(x,ymin,ymax)

        if ymin != ymax:
            sol = optimize.brentq(f, ymin, ymax)
        #sol = optimize.bisect(f, ExclusionPlot.ymin, ExclusionPlot.ymax)
        #sols = optimize.fsolve(f, 0.1*(ExclusionPlot.ymax+ExclusionPlot.ymin), maxfev=10)
        #print(x,sols)

        #if len(sols) > 0:
        #       if sols[0] < sol:
        #        sol = sols[0]

        #if debug:
        #     print(x,sol, ExclusionPlot.ymin, ExclusionPlot.ymax, f(ExclusionPlot.ymin), f(ExclusionPlot.ymax) )
        #print('sol',x,sol)
        sols.append(sol)

    # add first and last values for best polygon perf.
    xlist = np.insert(xlist, 0, ExclusionPlot.xmin)
    xlist = np.append(xlist, ExclusionPlot.xmax)
    sols.append(ExclusionPlot.ymax)

    lim = Limit(name=parameters.name, color=parameters.color, alpha=parameters.alpha)
    lim.set_data(xlist,sols)

    return lim


#_______________________________________________________________________________
class Mother(object):
    #_______________________________________________________________________________
    def __init__(self, name='meson', mass=5., fraction=0.4, br_file='file'):
        self.name = name
        self.mass = mass
        self.fraction = fraction
        self.br_file = br_file

#_______________________________________________________________________________
class Detector(object):
    #_______________________________________________________________________________
    def __init__(self, r_min=0.25, r_max=1.05, z_min=10., z_max=10.5):
        self.r_min = r_min
        self.r_max = r_max
        self.z_min = z_min
        self.z_max = z_max
