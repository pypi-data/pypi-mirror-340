

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports
import numpy as np


# ----------------------------------------------------------------------
#  Compressible Mixed Flat Plate
# ----------------------------------------------------------------------

def compressible_mixed_flat_plate(Re,Ma,Tc,xt):
    """Computes the coefficient of friction for a flat plate given the 
    input parameters. Also returns the correction terms used in the
    computation.

    Assumptions:
    Reynolds number between 10e5 and 10e9
    xt between 0 and 1

    Source:
    adg.stanford.edu (Stanford AA241 A/B Course Notes)

    Inputs:
    Re (Reynolds number)                                             [Unitless]
    Ma (Mach number)                                                 [Unitless]
    Tc (temperature)                                                 [K]
    xt (turbulent transition point as a proportion of chord length)  [Unitless]

    Outputs:
    cf_comp (coefficient of friction)                                [Unitless]
    k_comp (compressibility correction)                              [Unitless]
    k_reyn (Reynolds number correction)                              [Unitless]

    Properties Used:
    N/A
    """     
    
    if xt < 0.0 or xt > 1.0:
        raise ValueError("Turbulent transition must be between 0 and 1")

    Rex = Re*xt
    Rex[Rex==0.0] = 0.0001

    theta = 0.671*xt/(Rex**0.5)
    xeff  = (27.78*theta*Re**0.2)**1.25
    Rext  = Re*(1-xt+xeff)
    
    cf_turb  = 0.455/(np.log10(Rext)**2.58)
    cf_lam   = 1.328/(Rex**0.5)
    
    if xt > 0.0:
        cf_start = 0.455/(np.log10(Re*xeff)**2.58)
    else:
        cf_start = 0.0
    
    cf_inc = cf_lam*xt + cf_turb*(1-xt+xeff) - cf_start*xeff
    
    # compressibility correction
    Tw = Tc * (1. + 0.178*Ma*Ma)
    Td = Tc * (1. + 0.035*Ma*Ma + 0.45*(Tw/Tc - 1.))
    k_comp = (Tc/Td) 
    
    # reynolds correction
    Rd_w   = Re * (Td/Tc)**1.5 * ( (Td+216.) / (Tc+216.) )
    k_reyn = (Re/Rd_w)**0.2
    
    # apply corrections
    cf_comp = cf_inc * k_comp * k_reyn
    
    return cf_comp, k_comp, k_reyn