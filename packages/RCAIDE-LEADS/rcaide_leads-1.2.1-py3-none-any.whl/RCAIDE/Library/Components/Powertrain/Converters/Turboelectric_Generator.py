# RCAIDE/Library/Components/Propulsors/Turboelectric_Generator.py
# 
#  
# Created:  Jan 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
## RCAIDE imports
from RCAIDE.Framework.Core                  import Data 
from .Converter                             import Converter
from RCAIDE.Library.Components.Powertrain.Converters.Turboshaft    import Turboshaft 
from RCAIDE.Library.Components.Powertrain.Converters.DC_Generator  import DC_Generator 
from RCAIDE.Library.Methods.Powertrain.Converters.Turboelectric_Generator.append_turboelectric_generator_conditions      import append_turboelectric_generator_conditions  
from RCAIDE.Library.Methods.Powertrain.Converters.Turboelectric_Generator.compute_turboelectric_generator_performance    import compute_turboelectric_generator_performance, reuse_stored_turboelectric_generator_data
 
# ----------------------------------------------------------------------
#  Turboelectric_Generator
# ----------------------------------------------------------------------
class Turboelectric_Generator(Converter):
    """
    A Turboelectric_Generator propulsion system model that simulates the performance of a Turboelectric_Generator engine.
   

    Attributes
    ----------
    tag : str
        Identifier for the shaft engine. Default is 'turboshaft'. 
        
    turboshaft : Component
        Turboshaft component. Default is the Turboshaft Class.
        
    generator : Component
        Generator component. Default is DC_Generator Class.
        
    gearbox : Component
        Gearbox data structure. Default is None. 
        
    inverse_calculation : Component
        Flag that determines the how calculations are performed. Default is False    

    Notes
    -----
    The Turboelectric_Generator class inherits from the Turboshaft class and implements
    methods for computing Turboelectric_Generator engine performance. Unlike other gas turbine
    engines that produce thrust, a Turboelectric_Generator engine's primary output is shaft
    power, typically used to drive a helicopter rotor or other mechanical systems. 

    See Also
    --------
    RCAIDE.Library.Components.Powertrain.Propulsors.Turboshaft 
    """ 
    def __defaults__(self):
        # setting the default values
        self.tag                       = 'turboelectric_generator'
        self.turboshaft                = Turboshaft()
        self.generator                 = DC_Generator()
        self.gearbox                   = Data()
        self.gearbox.gear_ratio        = None  
        self.inverse_calculation       = False

    def append_operating_conditions(self,segment,energy_conditions,noise_conditions=None): 
        """
        Appends operating conditions to the segment.
        """  
        append_turboelectric_generator_conditions(self,segment,energy_conditions) 
        return
 
    def compute_performance(self,state,fuel_line = None,bus = None):
        """
        Computes Turboelectric_Generator performance including power.
        """
        P_mech,P_elec,stored_results_flag,stored_propulsor_tag =  compute_turboelectric_generator_performance(self,state,fuel_line, bus)
        return P_mech,P_elec,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(turboelectric_generator,state,stored_propulsor_tag):
        power  = reuse_stored_turboelectric_generator_data(turboelectric_generator,state,stored_propulsor_tag)
        return power 
