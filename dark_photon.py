from ExclusionPlot import *
from Limit import *
from Function import *
from Model import *
from Utils import *
from collections import OrderedDict
from scipy import optimize
import numpy as np

#_______________________________________________________________________________
def main():


    ## ns in the number of Bhadrons produced in the whole detector after some triggering (ie Bparking)
    ## eff is the acceptance efficiency in some fiducial eta region (e.g nose)

    #model = MajoranaNeutrinoElectron(mass=2., coupling=1.e-05,
    #                                 ns=1.e13, eff=0.1)

    #model.compute_lifetime()
    #model.compute_branching_ratio('data/br_BpD0str_eXN.csv')

    ## nose acceptance
    #model.event_yield(r_min=0.25, r_max=1.05,
    #                  z_min=10., z_max=10.5,
    #                  pt=5.)


    ep = ExclusionPlot(name='dark_photon', xlabel='$m_{Z_D} \, [GeV]$', ylabel='$\epsilon^2$',
                       model='dark_photon',
                       xmin=10, xmax=70, ymin=1.e-7, ymax=1.e-5,
                       dimx=5, dimy=5, logx=False, logy=True)



    ## inclusive limit from all experiments
    lim_atlascms_300fb = Limit(name='present', color='goldenrod', alpha=0.)
    lim_atlascms_300fb.set_func(Function('lim_atlascms_300fb', 'data/atlascms_zd_300fb.csv'))

    lim_lhcb_15fb = Limit(name='present', color='blue grey', alpha=0.)
    lim_lhcb_15fb.set_func(Function('lhcb_zd_15fb', 'data/lhcb_zd_15fb.csv'))

    lim_lhcb_50fb = Limit(name='present', color='grey', alpha=0.)
    lim_lhcb_50fb.set_func(Function('lhcb_zd_50fb', 'data/lhcb_zd_50fb.csv'))

    lim_lhcb_500fb = Limit(name='present', color='light grey', alpha=0.)
    lim_lhcb_500fb.set_func(Function('lhcb_zd_500fb', 'data/lhcb_zd_500fb.csv'))

    lim_cen_3000fb = Limit(name='present', color='blue', alpha=0.)
    lim_cen_3000fb.set_func(Function('cen_3000fb', 'data/zd_EE_C_10.csv'))

    lim_nose_3000fb = Limit(name='present', color='dark blue', alpha=0.)
    lim_nose_3000fb.set_func(Function('nose_3000fb', 'data/zd_EEMM_C_20.csv'))

    lim_nose2_3000fb = Limit(name='present', color='black', alpha=0.)
    lim_nose2_3000fb.set_func(Function('nose_3000fb', 'data/zd_EEMM_F_20.csv'))


    ep.add_limit(lim_lhcb_15fb)
    #ep.add_limit(lim_lhcb_50fb)
    #ep.add_limit(lim_lhcb_500fb)
    ep.add_limit(lim_atlascms_300fb)

    ep.add_limit(lim_nose_3000fb)
    ep.add_limit(lim_nose2_3000fb)
    ep.add_limit(lim_cen_3000fb)

    ep.plot()

#_______________________________________________________________________________
if __name__ == "__main__":
    main()
