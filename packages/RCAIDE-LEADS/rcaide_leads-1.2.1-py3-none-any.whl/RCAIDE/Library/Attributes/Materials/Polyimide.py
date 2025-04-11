# RCAIDE/Library/Attributes/Solids/Polyimide.py
# 

# Created: Jan 2025 M. Clarke

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from .Solid import Solid 
from array import * 

#-------------------------------------------------------------------------------
# Polyimide Insulation Material
#------------------------------------------------------------------------------- 
class Polyimide(Solid): 
    """
    A class representing Polyimide(PI) and its material properties.

    Attributes
    ----------
    electrical_permittivity : float
        Material electrical permittivity in kg/m³ (3.5)
    dielectric_strength_range : list
        Range of dielectric strength in Pa (6E7,8E7)
    density : float
        Material density in kg/m³ (1280)
    thermal_conductivity : float
        Heat conduction coefficient in W/(m·K) (0.4)
    melting_point : float
        Material melting point in K (653)
    temperature_range : list
        Range of temperature in K (33, 533)
    modulus_of_elasticity : float
        Material modulus of elasticity in Pa (3.1E9)
    yield_tensile_strength : float
        Stress at which material begins to deform plastically in Pa (96e6)
    """

    def __defaults__(self):
        """Sets material properties at instantiation. 

        Assumptions:
            None
    
        Source:
            Guo, Ruochen, et al. "Electrical Architecture of 90-seater Electric Aircraft: A Cable Perspective."
            IEEE Transactions on Transportation Electrification (2024).
        """
        self.electrical_permittivity    = 3.5 
        self.dielectric_strength_range  = [6E7,8E7]  # [V/m] 
        self.density                    = 1280 
        self.thermal_conductivity       = 0.4
        self.melting_point              = 653       # Kelvin
        self.temperature_range          = [33, 533] # Kelvin
        self.modulus_of_elasticity      = 3.1E9
        self.yield_tensile_strength     = 96E6 
        return 