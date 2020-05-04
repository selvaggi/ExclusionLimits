import matplotlib._color_data as mcd
import numpy as np
from abc import ABC,abstractmethod
from Function import *
import math

debug=False

class Model(ABC):
    #_______________________________________________________________________________
    def __init__(self, mass=1., couplingSquared=1.e-06, ns=1.e10, eff=0.01):

        self.ns = ns
        self.eff = eff
        self.mass = mass
        self.couplingSquared = couplingSquared

        self.tau = -1
        self.br = -1

        super(Model, self).__init__()

    #_______________________________________________________________________________
    def event_yield(self, r_min=0.25, r_max=1.05, z_min=10., z_max=10.5, pt=5.):

        ###FIX ME: for now r, z value are dummy, the accpetance in the nose region
        # is pre-computed, now this is used only to calculate eta
        # in the future require this method to compute from MC the real acceptance
        # in the nose

        theta_min = math.atan(r_min/z_min)
        theta_max = math.atan(r_max/z_max)

        eta_min = - math.log(math.tan(theta_min/2))
        eta_max = - math.log(math.tan(theta_max/2))

        ## cannot take average eta due to steeply falling spectrum
        p = 0.75
        eta = p*eta_min + (1-p)*eta_max
        theta = p*theta_min + (1-p)*theta_max

        ## compute path length inside fiducial volume
        l_min = z_min/math.cos(theta)
        l_max = z_max/math.cos(theta)

        c=3.e+8
        energy = pt*math.cosh(eta)

        gamma=energy/self.mass
        tau = self.tau
        ctau=c*tau
        gct = gamma*ctau

        acceptance=math.exp(-l_min/gct) - math.exp(-l_max/gct)

        br = self.br
        event_yield = self.ns * br * self.eff * acceptance

        if debug:
            print ('mass          =   {:.3f} '.format(self.mass))
            print ('couplingSq    =   {:.2e} '.format(self.couplingSquared))
            print ('eta_min       =   {:.3f} '.format(eta_min))
            print ('eta_max       =   {:.3f} '.format(eta_max))
            print ('l_min         =   {:.3f} m'.format(l_min))
            print ('l_max         =   {:.3f} m'.format(l_max))
            print ('energy        =   {:.3f} GeV'.format(energy))
            print ('tau           =   {:.3f} ns'.format(tau*1e9))
            print ('gamma         =   {:.3f} '.format(gamma))
            print ('ctau          =   {:.3f} m'.format(c*tau))
            print ('gamma*c*tau   =   {:.3f} m'.format(gct))
            print ('----------------------------------------------------------')
            print ('number of S.  =   {:.2e} '.format(self.ns))
            print ('br. ratio     =   {:.2e} '.format(br))
            print ('efficiency    =   {:.2e} '.format(self.eff))
            print ('acceptance    =   {:.2e} '.format(acceptance))
            print ('ev.  yield    =   {:.2e} '.format(event_yield))

        return event_yield

    #_______________________________________________________________________________
    @abstractmethod
    def compute_lifetime(self):
        pass

    #_______________________________________________________________________________
    @abstractmethod
    def compute_branching_ratio(self):
        pass

    #_______________________________________________________________________________
    #def acceptance(self, zmin=10., zmax=10.5):

class MajoranaNeutrinoElectron(Model):

    def compute_lifetime(self):
        self.tau = 1.e-12/self.mass**5/self.couplingSquared

    def compute_branching_ratio(self, data_file):
        br_vs_m = Function('br_b0', data_file)
        self.br = self.couplingSquared * br_vs_m.eval(self.mass)
