# RCAIDE/Compoments/Fuselages/Blended_Wing_Body_Fuselage.py
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Fuselage import Fuselage

# python imports 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Blended_Wing_Body_Fuselage
# ----------------------------------------------------------------------------------------------------------------------  
class Blended_Wing_Body_Fuselage(Fuselage):
    """
    A blended wing body (BWB) fuselage design that smoothly integrates the wing and fuselage 
    into a single lifting body configuration.

    Attributes
    ----------
    tag : str
        Unique identifier for the BWB fuselage component, defaults to 'bwb_fuselage'
    
    aft_centerbody_area : float
        Cross-sectional area of the aft centerbody section in square meters
        
    aft_centerbody_taper : float
        Taper ratio of the aft centerbody section, defined as the ratio of tip 
        to root chord lengths
        
    cabin_area : float
        Total available cabin floor area in square meters

    Notes
    -----
    The blended wing body design offers several advantages over conventional tube-and-wing
    configurations:
    
    * Reduced wetted area leading to lower skin friction drag
    * Improved lift-to-drag ratio due to the lifting body design
    * Potential for increased internal volume and better weight distribution

    **Definitions**

    'Centerbody'
        The central section of the BWB that houses the passenger cabin and cargo hold
        
    'Aft Centerbody'
        The rear section of the centerbody that transitions into the outer wing sections

    See Also
    --------
    RCAIDE.Library.Components.Fuselages.Fuselage
        Base fuselage class that provides common functionality
    RCAIDE.Library.Components.Fuselages.Tube_Fuselage
        Conventional tube fuselage design for comparison
    """
    
    def __defaults__(self):
        """
        Sets the default values for the BWB fuselage component attributes.

        Notes
        -----
        This method initializes all required attributes with default values. Users should 
        modify these values based on their specific design requirements after instantiation.
        """      
          
        self.tag                   = 'bwb_fuselage'
        self.aft_centerbody_area   = 0.0
        self.aft_centerbody_taper  = 0.0
        self.cabin_area            = 0.0
        
    def compute_moment_of_inertia(self, center_of_gravity): 
        """
        Computes the moment of inertia tensor for the BWB fuselage.

        Parameters
        ----------
        center_of_gravity : array-like
            The (x, y, z) coordinates of the center of gravity about which to compute
            the moment of inertia

        Returns
        -------
        I : ndarray
            3x3 moment of inertia tensor in kg*m^2

        Notes
        -----
        Currently returns a zero matrix. This is a placeholder that should be implemented
        with actual BWB moment of inertia calculations.
        """
        I = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) 
        return I        