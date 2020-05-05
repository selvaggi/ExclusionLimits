import matplotlib._color_data as mcd
import numpy as np
from abc import ABC,abstractmethod
from Function import *
import math

class Model(ABC):
    #_______________________________________________________________________________
    def __init__(self, parameters, mass=1., coupling=1.e-06):

        self.ns0 = parameters.ns0
        self.trigger_eff = parameters.trigger_eff
        self.meson_br = parameters.meson_br
        self.eta_eff = parameters.eta_eff

        self.r_min = parameters.r_min
        self.r_max = parameters.r_max
        self.z_min = parameters.z_min
        self.z_max = parameters.z_max

        self.pt = parameters.pt

        self.mass = mass
        self.coupling = coupling

        self.tau = -1
        self.br = -1

        super(Model, self).__init__()

    #_______________________________________________________________________________
    def event_yield(self, debug=False):

        ###FIX ME: for now r, z value are dummy, the accpetance in the nose region
        # is pre-computed, now this is used only to calculate eta
        # in the future require this method to compute from MC the real acceptance
        # in the nose

        theta_min = math.atan(self.r_min/self.z_min)
        theta_max = math.atan(self.r_max/self.z_max)

        eta_min = - math.log(math.tan(theta_min/2))
        eta_max = - math.log(math.tan(theta_max/2))

        ## cannot take average eta due to steeply falling spectrum
        p = 0.75
        eta = p*eta_min + (1-p)*eta_max
        theta = p*theta_min + (1-p)*theta_max

        ## compute path length inside fiducial volume
        l_min = self.z_min/math.cos(theta)
        l_max = self.z_max/math.cos(theta)

        c=3.e+8
        energy = self.pt*math.cosh(eta)

        gamma=energy/self.mass
        tau = self.tau
        ctau=c*tau
        gct = gamma*ctau

        acceptance=math.exp(-l_min/gct) - math.exp(-l_max/gct)

        br = self.br
        event_yield = self.ns0
        event_yield *= self.meson_br
        event_yield *= self.trigger_eff
        event_yield *= self.eta_eff
        event_yield *= br
        event_yield *= acceptance

        if debug:
            print ('mass          =   {:.3f} '.format(self.mass))
            print ('coupling      =   {:.2e} '.format(self.coupling))
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
            print ('number of S.  =   {:.2e} '.format(self.ns0))
            print ('meson BR      =   {:.2e} '.format(self.meson_br))
            print ('trigger eff   =   {:.2e} '.format(self.trigger_eff))
            print ('eta_eff       =   {:.2e} '.format(self.eta_eff))
            print ('br. ratio     =   {:.2e} '.format(br))
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
        self.tau = 1.e-12/self.mass**5/self.coupling**2

    def compute_branching_ratio(self, data_file):
        br_vs_m = Function('br_b0', data_file)
        self.br = br_vs_m.eval(self.mass) * self.coupling**2
