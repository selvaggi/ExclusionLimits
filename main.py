from ExclusionPlot import *
from Limit import *
from Function import *
from Model import *
from collections import OrderedDict

#_______________________________________________________________________________
def main():


    ## ns in the number of Bhadrons produced in the whole detector after some triggering (ie Bparking)
    ## eff is the acceptance efficiency in some fiducial eta region (e.g nose)
    model = MajoranaNeutrinoElectron(mass=2., couplingSquared=1.e-05,
                                     ns=1.e13, eff=0.1)

    model.compute_lifetime()
    model.compute_branching_ratio('data/br_B0p_eXN.csv')

    ## nose acceptance
    model.event_yield(r_min=0.25, r_max=1.05,
                      z_min=10., z_max=10.5,
                      pt=5.)

    ## initialize parameter grid
    param_ranges = OrderedDict()

    param_ranges['$m_X \, [GeV]$'] = (0.01, 7 , False) #min, max, log or not
    param_ranges['$|U_e|^2$'] = (1e-03, 1e-08 , True) #tau_i





    ep = ExclusionPlot(name='dummy', xlabel='$m_X \, [GeV]$', ylabel='$|U_e|$',
                       xmin=1e-01, xmax=1e01, ymin=1.e-5, ymax=1.e-2,
                       dimx=7, dimy=7, logy=True)

    #funct_test = Function('test', 'data/br_B0p_eXN.csv')
    #print(funct_test.eval(2.6))


    lim = Limit(name='present', color='silver', alpha=0.2)
    lim.set_func(Function('ex_pres', 'data/une_present.csv'))

    ep.add_limit(lim)
    ep.plot()

#_______________________________________________________________________________
if __name__ == "__main__":
    main()
