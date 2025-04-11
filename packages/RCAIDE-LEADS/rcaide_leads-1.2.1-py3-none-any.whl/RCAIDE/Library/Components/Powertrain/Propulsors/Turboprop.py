# RCAIDE/Library/Components/Propulsors/Turboprop.py 
#
#
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                     import Propulsor
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Methods.Powertrain.Propulsors.Turboprop          .append_turboprop_conditions     import append_turboprop_conditions 
from RCAIDE.Library.Methods.Powertrain.Propulsors.Turboprop          .compute_turboprop_performance   import compute_turboprop_performance, reuse_stored_turboprop_data
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan Component
# ---------------------------------------------------------------------------------------------------------------------- 
class Turboprop(Propulsor):
    """
    A turboprop propulsion system model that simulates the performance of a turboprop engine.

    Attributes
    ----------
    tag : str
        Identifier for the turboprop engine. Default is 'turboprop'.
    
    nacelle : Component
        Nacelle component of the engine. Default is None.
        
    compressor : Component
        Compressor component of the engine. Default is None.
        
    turbine : Component
        Turbine component of the engine. Default is None.
        
    combustor : Component
        Combustor component of the engine. Default is None. 
        
    diameter : float
        Diameter of the engine [m]. Default is 0.0.
        
    length : float
        Length of the engine [m]. Default is 0.0.
        
    height : float
        Engine centerline height above the ground plane [m]. Default is 0.5.
        
    design_isa_deviation : float
        ISA temperature deviation at design point [K]. Default is 0.0.
        
    specific_fuel_consumption_reduction_factor : float
        Specific fuel consumption adjustment factor (Less than 1 is a reduction). Default is 0.0.
        
    design_altitude : float
        Design altitude of the engine [m]. Default is 0.0.
        
    propeller_efficiency : float
        Design point propeller efficiency. Default is 0.0.
        
    gearbox.efficiency : float
        Design point gearbox efficiency. Default is 0.0.
        
    design_mach_number : float
        Design Mach number. Default is 0.0.
        
    compressor_nondimensional_massflow : float
        Non-dimensional mass flow through the compressor. Default is 0.0.
        
    reference_temperature : float
        Reference temperature for calculations [K]. Default is 288.15.
        
    reference_pressure : float
        Reference pressure for calculations [Pa]. Default is 101325.0.

    Notes
    -----
    The Turboprop class inherits from the Propulsor base class and implements
    methods for computing turboprop engine performance. A turboprop engine uses
    a gas turbine core to drive a propeller through a reduction gearbox, combining
    the efficiency of a propeller at low speeds with the power of a turbine engine.

    **Definitions**

    'ISA'
        International Standard Atmosphere - standard atmospheric model

    'Mach number'
        Ratio of flow velocity to the local speed of sound

    See Also
    --------
    RCAIDE.Library.Components.Powertrain.Propulsors.Propulsor
    RCAIDE.Library.Components.Powertrain.Propulsors.Turbofan
    RCAIDE.Library.Components.Powertrain.Propulsors.Turbojet
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                                        = 'turboprop'   
        self.nacelle                                    = None 
        self.compressor                                 = None  
        self.turbine                                    = None  
        self.combustor                                  = None       
        self.diameter                                   = 0.0      
        self.length                                     = 0.0
        self.height                                     = 0.0      
        self.design_isa_deviation                       = 0.0
        self.design_altitude                            = 0.0
        self.propeller_efficiency                       = 0.0
        self.gearbox                                    = Data()
        self.specific_fuel_consumption_reduction_factor =  0.0
        self.gearbox.gear_ratio                         = 1.0
        self.gearbox.efficiency                         = 0.0 
        self.design_angular_velocity                    = 0.0
        self.design_mach_number                         = None 
        self.design_freestream_velocity                 = None
        self.compressor_nondimensional_massflow         = 0.0 
        self.reference_temperature                      = 288.15
        self.reference_pressure                         = 1.01325*10**5  
    
    def append_operating_conditions(self,segment,energy_conditions,noise_conditions=None):
        """
        Appends operating conditions to the segment.
        """
        append_turboprop_conditions(self,segment,energy_conditions,noise_conditions)
        return

    def unpack_propulsor_unknowns(self,segment):   
        return 

    def pack_propulsor_residuals(self,segment): 
        return

    def append_propulsor_unknowns_and_residuals(self,segment): 
        return    
    
    def compute_performance(self,state,center_of_gravity = [[0, 0, 0]]):
        """
        Computes turboprop performance including thrust, moment, and power.
        """
        thrust,moment,power_mech,power_elec,stored_results_flag,stored_propulsor_tag =  compute_turboprop_performance(self,state,center_of_gravity)
        return thrust,moment,power_mech,power_elec,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(turboprop,state,network,stored_propulsor_tag = None,center_of_gravity = [[0, 0, 0]]):
        """
        Reuses stored turboprop data for performance calculations.
        """
        thrust,moment,power_mech,power_elec  = reuse_stored_turboprop_data(turboprop,state,network,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power_mech,power_elec 