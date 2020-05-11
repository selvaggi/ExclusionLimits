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


    ep = ExclusionPlot(name='dummy', xlabel='$m_X \, [GeV]$', ylabel='$|U_e|$',
                       model='MajoranaNeutrinoElectron',
                       xmin=1e-01, xmax=1e+01, ymin=1.e-5, ymax=1.e-2,
                       dimx=7, dimy=7, logy=True)


    #isolines = [100, 10, 3]
    isolines = [100,10,3]
    npoints = 10

    ### B meson branching ratios
    meson_br_B0 = 0.43
    meson_br_Bp = 0.43
    meson_br_Bs = 0.10
    meson_br_Bc = 8.5e-04

    ## acceptance in eta region for different pt cuts (to be assessed in sim)
    nose_acceptance = dict()
    nose_acceptance[5.] = 0.141
    nose_acceptance[10.] = 0.117
    nose_acceptance[20.] = 0.071

    hgc_acceptance = dict()
    hgc_acceptance[5.] = 0.356
    hgc_acceptance[10.] = 0.335
    hgc_acceptance[20.] = 0.31


    class Parameters(object):
        ns0=1.e15   ## number of bb pairs at HL-LHC
        trigger_eff=0.01   ## B-parking / or whatever other cuts needed to trigger
        #eta_eff=nose_acceptance[5.] ## acceptance for the Bmeson to go in particular direction
        pt=10.
        eta_eff=hgc_acceptance[pt] ## acceptance for the Bmeson to go in particular direction

        ## fraction of Bmesons produced in particular mode
        list_brs = [
                        (meson_br_Bp,'data/br_Bp_eN.csv'),
                        (meson_br_Bp,'data/br_Bp_D0eN.csv'),
                        (meson_br_Bp,'data/br_Bp_D0steN.csv'),
                        (meson_br_Bp,'data/br_Bp_pi0eN.csv'),
                        (meson_br_Bp,'data/br_Bp_rho0eN.csv'),
                        (meson_br_B0,'data/br_B0_DpeN.csv'),
                        (meson_br_B0,'data/br_B0_rhopeN.csv'),
                        (meson_br_B0,'data/br_B0_pipeN.csv'),
                        (meson_br_B0,'data/br_B0_DpsteN.csv'),
                        (meson_br_Bs,'data/br_Bs_DssteN.csv'),
                        (meson_br_Bs,'data/br_Bs_KpsteN.csv'),
                        (meson_br_Bs,'data/br_Bs_KpeN.csv'),
                        (meson_br_Bs,'data/br_Bs_DseN.csv'),
                        (meson_br_Bc,'data/br_Bc_eN.csv')
                   ]


        '''
        ### Nose
        r_min=0.25
        r_max=1.05
        z_min=10.
        z_max=10.5
        '''

        ## HGC
        r_min=0.40
        r_max=2.20
        z_min=300.
        z_max=520.


        pt=10.
        name='Nose'
        color='red'
        alpha=0.2

    nose_limits = OrderedDict()
    for target in isolines:
        nose_limits[target] = best_limit(ExclusionPlot=ep, parameters=Parameters,
                                         target=target, npoints=npoints)


    '''
    Parameters.meson_br = meson_br_Bc
    Parameters.llp_br = 'data/br_Bc_eXN.csv'
    Parameters.color = 'red'

    for target in isolines:
        nose_limits_Bc[target] = best_limit(ExclusionPlot=ep, parameters=Parameters,
                                         target=target, npoints=npoints)

    Parameters.meson_br = meson_br_B0
    Parameters.llp_br = 'data/br_B0_pipeN.csv'
    Parameters.color = 'red'

    for target in isolines:
        nose_limits_B0_pipeN[target] = best_limit(ExclusionPlot=ep, parameters=Parameters,
                                                  target=target, npoints=npoints)


    Parameters.meson_br = meson_br_Bp
    Parameters.llp_br = 'data/br_Bp_eN.csv'
    Parameters.color = 'red'

    for target in isolines:
        nose_limits_Bp_eN[target] = best_limit(ExclusionPlot=ep, parameters=Parameters,
                                               target=target, npoints=npoints)

    '''
    #model_class = globals()[ep.model]
    #model = model_class(Parameters, mass=2.9763514416313175, coupling=0.008)

    #model.compute_lifetime()
    #model.compute_branching_ratio(Parameters.llp_br)
    #model.event_yield(debug=True)



    ## inclusive limit from all experiments
    lim_present = Limit(name='present', color='grey', alpha=0.5)
    lim_present.set_func(Function('ex_pres', 'data/limit_HNL_UNe_present.csv'))

    ## projected limit from FASER2
    lim_faser = Limit(name='FASER', color='pale yellow', alpha=0.5)
    lim_faser.set_func(Function('ex_pres', 'data/limit_HNL_UNe_FASER.csv'))

    ### limit from CMS W->lN search (rescaled to HL-LHC)
    lim_cms = Limit(name='CMS - WNe (HL-LHC)', color='light blue', alpha=0.5)
    func = Function('ex_pres', 'data/limit_HNL_UNe_CMS_137invfb.csv')
    func.pow_data(0.5) ## take sqrt to convert
    func.scale_data(math.sqrt(137./3000.)) ## take sqrt to convert
    lim_cms.set_func(func)

    ep.add_limit(lim_present)
    ep.add_limit(lim_faser)
    ep.add_limit(lim_cms)


    for target in nose_limits.keys():
        ep.add_limit(nose_limits[target])

    ep.plot()

#_______________________________________________________________________________
if __name__ == "__main__":
    main()
