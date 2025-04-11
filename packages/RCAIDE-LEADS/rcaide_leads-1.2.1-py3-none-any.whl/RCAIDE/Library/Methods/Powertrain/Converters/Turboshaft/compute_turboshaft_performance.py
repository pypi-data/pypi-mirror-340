# RCAIDE/Methods/Library/Methods/Powertrain/Converters/compute_turboshaft_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports      
from RCAIDE.Framework.Core import Data   
from RCAIDE.Library.Methods.Powertrain.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Powertrain.Converters.Combustor          import compute_combustor_performance
from RCAIDE.Library.Methods.Powertrain.Converters.Compressor         import compute_compressor_performance
from RCAIDE.Library.Methods.Powertrain.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Powertrain.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Powertrain.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Powertrain.Converters.Turboshaft         import compute_power
 
# python imports 
from copy import deepcopy 
# ----------------------------------------------------------------------------------------------------------------------
# compute_turboshaft_performance
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_turboshaft_performance(turboshaft,state,fuel_line=None,bus=None): 
    """ 
    Computes the perfomrance of a turboshaft
    
    Parameters
    ----------
    turboshaft : RCAIDE.Library.Components.Converters.Turboshaft
        Turboshaft engine component with the following attributes:
            - tag : str
                Identifier for the turboshaft
            - working_fluid : Data
                Working fluid properties object
            - ram : Data
                Ram component
                - tag : str
                    Identifier for the ram
            - inlet_nozzle : Data
                Inlet nozzle component
                    - tag : str
                        Identifier for the inlet nozzle
            - compressor : Data
                Compressor component
                    - tag : str
                        Identifier for the compressor
            - combustor : Data
                Combustor component
                    - tag : str
                        Identifier for the combustor
            - high_pressure_turbine : Data
                High pressure turbine component
                    - tag : str
                        Identifier for the high pressure turbine
            - low_pressure_turbine : Data
                Low pressure turbine component
                    - tag : str
                        Identifier for the low pressure turbine
            - core_nozzle : Data
                Core nozzle component
                    - tag : str
                        Identifier for the core nozzle
    state : RCAIDE.Framework.Mission.Common.State
        State object containing:
            - conditions : Data
                Flight conditions
                    - freestream : Data
                        Freestream properties
                            - density : numpy.ndarray
                                Air density [kg/m³]
                    - noise : dict
                        Noise conditions indexed by component tag
                    - energy : dict
                        Energy conditions indexed by component tag
    center_of_gravity : list of lists, optional
        Center of gravity coordinates [[x, y, z]] [m]. Default: [[0.0, 0.0, 0.0]]
    
    Returns
    -------
    thrust : numpy.ndarray
        Thrust force vector [N]
    moment : numpy.ndarray
        Moment vector [N·m]
    power : numpy.ndarray
        Shaft power output [W]
    stored_results_flag : bool
        Flag indicating if results are stored
    stored_propulsor_tag : str
        Tag of the turboshaft with stored results
    
    Notes
    -----
    This function computes the performance of a turboshaft engine by sequentially analyzing
    each component in the engine's thermodynamic cycle. It links the output conditions of
    each component to the input conditions of the next component in the flow path.
    
    The function follows this sequence:
        1. Set working fluid properties
        2. Compute ram performance
        3. Compute inlet nozzle performance
        4. Compute compressor performance
        5. Compute combustor performance
        6. Compute high pressure turbine performance
        7. Compute low pressure turbine performance
        8. Compute core nozzle performance
        9. Compute power output
    
    **Major Assumptions**
        * Steady state operation
        * One-dimensional flow through components
        * Adiabatic components except for the combustor
        * Perfect gas behavior with variable properties
    
    References
    ----------
    [1] Mattingly, J.D., "Elements of Gas Turbine Propulsion", 2nd Edition, AIAA Education Series, 2005. https://soaneemrana.org/onewebmedia/ELEMENTS%20OF%20GAS%20TURBINE%20PROPULTION2.pdf
    
    See Also
    --------
    RCAIDE.Library.Methods.Powertrain.Converters.Turboshaft.compute_power
    """
    conditions                = state.conditions  
    ram                       = turboshaft.ram
    inlet_nozzle              = turboshaft.inlet_nozzle
    compressor                = turboshaft.compressor
    combustor                 = turboshaft.combustor
    high_pressure_turbine     = turboshaft.high_pressure_turbine
    low_pressure_turbine      = turboshaft.low_pressure_turbine 
    core_nozzle               = turboshaft.core_nozzle

    # unpack component conditions 
    turboshaft_conditions   = conditions.energy.converters[turboshaft.tag]
    ram_conditions          = conditions.energy.converters[ram.tag]     
    inlet_nozzle_conditions = conditions.energy.converters[inlet_nozzle.tag]
    core_nozzle_conditions  = conditions.energy.converters[core_nozzle.tag] 
    compressor_conditions   = conditions.energy.converters[compressor.tag] 
    lpt_conditions          = conditions.energy.converters[low_pressure_turbine.tag]
    hpt_conditions          = conditions.energy.converters[high_pressure_turbine.tag]
    combustor_conditions    = conditions.energy.converters[combustor.tag] 

    # Step 1: Set the working fluid to determine the fluid properties
    ram.working_fluid                             = turboshaft.working_fluid

    # Step 2: Compute flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,conditions)

    # Step 3: link inlet nozzle to ram 
    inlet_nozzle_conditions.inputs.stagnation_temperature             = ram_conditions.outputs.stagnation_temperature
    inlet_nozzle_conditions.inputs.stagnation_pressure                = ram_conditions.outputs.stagnation_pressure
    inlet_nozzle_conditions.inputs.static_temperature                 = ram_conditions.outputs.static_temperature
    inlet_nozzle_conditions.inputs.static_pressure                    = ram_conditions.outputs.static_pressure
    inlet_nozzle_conditions.inputs.mach_number                        = ram_conditions.outputs.mach_number
    inlet_nozzle.working_fluid                                        = ram.working_fluid

    # Step 4: Compute flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,conditions)      

    # Step 5: Link low pressure compressor to the inlet nozzle 
    compressor_conditions.inputs.stagnation_temperature  = inlet_nozzle_conditions.outputs.stagnation_temperature
    compressor_conditions.inputs.stagnation_pressure     = inlet_nozzle_conditions.outputs.stagnation_pressure
    compressor_conditions.inputs.static_temperature      = inlet_nozzle_conditions.outputs.static_temperature
    compressor_conditions.inputs.static_pressure         = inlet_nozzle_conditions.outputs.static_pressure
    compressor_conditions.inputs.mach_number             = inlet_nozzle_conditions.outputs.mach_number  
    compressor.working_fluid                             = inlet_nozzle.working_fluid 

    # Step 6: Compute flow through the low pressure compressor
    compute_compressor_performance(compressor,conditions)

    # Step 11: Link the combustor to the high pressure compressor
    combustor_conditions.inputs.stagnation_temperature                = compressor_conditions.outputs.stagnation_temperature
    combustor_conditions.inputs.stagnation_pressure                   = compressor_conditions.outputs.stagnation_pressure
    combustor_conditions.inputs.static_temperature                    = compressor_conditions.outputs.static_temperature
    combustor_conditions.inputs.static_pressure                       = compressor_conditions.outputs.static_pressure
    combustor_conditions.inputs.mach_number                           = compressor_conditions.outputs.mach_number  
    combustor.working_fluid                                           = compressor.working_fluid 

    # Step 12: Compute flow through the high pressor compressor 
    compute_combustor_performance(combustor,conditions)

    #link the high pressure turbione to the combustor 
    hpt_conditions.inputs.stagnation_temperature    = combustor_conditions.outputs.stagnation_temperature
    hpt_conditions.inputs.stagnation_pressure       = combustor_conditions.outputs.stagnation_pressure
    hpt_conditions.inputs.fuel_to_air_ratio         = combustor_conditions.outputs.fuel_to_air_ratio 
    hpt_conditions.inputs.static_temperature        = combustor_conditions.outputs.static_temperature
    hpt_conditions.inputs.static_pressure           = combustor_conditions.outputs.static_pressure
    hpt_conditions.inputs.mach_number               = combustor_conditions.outputs.mach_number 
    hpt_conditions.inputs.compressor                = compressor_conditions.outputs 
    hpt_conditions.inputs.bypass_ratio              = 0.0
    hpt_conditions.inputs.fan                       = Data()
    hpt_conditions.inputs.fan.work_done             = 0.0
    high_pressure_turbine.working_fluid             = combustor.working_fluid
    
    compute_turbine_performance(high_pressure_turbine,conditions)

    #link the low pressure turbine to the high pressure turbine 
    lpt_conditions.inputs.stagnation_temperature              = hpt_conditions.outputs.stagnation_temperature
    lpt_conditions.inputs.stagnation_pressure                 = hpt_conditions.outputs.stagnation_pressure 
    lpt_conditions.inputs.static_temperature                  = hpt_conditions.outputs.static_temperature
    lpt_conditions.inputs.static_pressure                     = hpt_conditions.outputs.static_pressure 
    lpt_conditions.inputs.mach_number                         = hpt_conditions.outputs.mach_number  
    low_pressure_turbine.working_fluid                        = high_pressure_turbine.working_fluid    
    lpt_conditions.inputs.compressor                          = Data()
    lpt_conditions.inputs.compressor.work_done                = 0.0
    lpt_conditions.inputs.compressor.external_shaft_work_done = 0.0
    lpt_conditions.inputs.fuel_to_air_ratio                   = combustor_conditions.outputs.fuel_to_air_ratio 
    lpt_conditions.inputs.bypass_ratio                        = 0.0
    lpt_conditions.inputs.fan                                 = Data()
    lpt_conditions.inputs.fan.work_done                       = 0.0

    compute_turbine_performance(low_pressure_turbine,conditions)

    #link the core nozzle to the low pressure turbine
    core_nozzle_conditions.inputs.stagnation_temperature     = lpt_conditions.outputs.stagnation_temperature
    core_nozzle_conditions.inputs.stagnation_pressure        = lpt_conditions.outputs.stagnation_pressure
    core_nozzle_conditions.inputs.static_temperature         = lpt_conditions.outputs.static_temperature
    core_nozzle_conditions.inputs.static_pressure            = lpt_conditions.outputs.static_pressure  
    core_nozzle_conditions.inputs.mach_number                = lpt_conditions.outputs.mach_number   
    core_nozzle.working_fluid                                = low_pressure_turbine.working_fluid  

    #flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,conditions) 
 
    # Link the thrust component to the core nozzle
    turboshaft_conditions.core_exit_velocity                       = core_nozzle_conditions.outputs.velocity
    turboshaft_conditions.core_area_ratio                          = core_nozzle_conditions.outputs.area_ratio
    turboshaft_conditions.core_nozzle                              = core_nozzle_conditions.outputs

    # Link the thrust component to the combustor
    turboshaft_conditions.fuel_to_air_ratio                        = combustor_conditions.outputs.fuel_to_air_ratio 

    # Link the thrust component to the low pressure compressor 
    turboshaft_conditions.combustor_stagnation_temperature         = combustor_conditions.outputs.stagnation_temperature
    turboshaft_conditions.total_temperature_reference              = compressor_conditions.inputs.stagnation_temperature
    turboshaft_conditions.total_pressure_reference                 = compressor_conditions.inputs.stagnation_pressure 
    turboshaft_conditions.flow_through_core                        =  1.0 #scaled constant to turn on core thrust computation
    turboshaft_conditions.flow_through_fan                         =  0.0 #scaled constant to turn on fan thrust computation     

    # Compute the power
    compute_power(turboshaft,conditions)
 
    compressor_conditions.omega   = compressor.design_angular_velocity * turboshaft_conditions.throttle   
    
    # Pack results    
    power                  = turboshaft_conditions.power   
    stored_results_flag    = True
    stored_propulsor_tag   = turboshaft.tag

    return power,stored_results_flag,stored_propulsor_tag

def reuse_stored_turboshaft_data(turboshaft,state,network,fuel_line,bus,stored_converter_tag):
    '''Reuses results from one turboshaft for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure     [-]  
    fuel_line            - fuelline                                [-] 
    turboshaft           - turboshaft data structure              [-] 
    total_power          - power of turboshaft group               [W] 

    Outputs:  
    total_power          - power of turboshaft group               [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                  = state.conditions  
    turboshaft                  = turboshaft.turboshaft
    ram                         = turboshaft.ram
    inlet_nozzle                = turboshaft.inlet_nozzle 
    compressor                  = turboshaft.compressor
    high_pressure_compressor    = turboshaft.high_pressure_compressor
    combustor                   = turboshaft.combustor 
    low_pressure_turbine        = turboshaft.low_pressure_turbine
    core_nozzle                 = turboshaft.core_nozzle 
    turboshaft_0                = fuel_line.converters[stored_converter_tag].turboshaft
    ram_0                       = fuel_line.converters[stored_converter_tag].ram
    inlet_nozzle_0              = fuel_line.converters[stored_converter_tag].inlet_nozzle 
    compressor_0                = fuel_line.converters[stored_converter_tag].compressor
    high_pressure_compressor_0  = fuel_line.converters[stored_converter_tag].high_pressure_compressor
    combustor_0                 = fuel_line.converters[stored_converter_tag].combustor
    low_pressure_turbine_0      = fuel_line.converters[stored_converter_tag].low_pressure_turbine
    core_nozzle_0               = fuel_line.converters[stored_converter_tag].core_nozzle

    # deep copy results  
    conditions.energy.converters[turboshaft.tag]               = deepcopy(conditions.energy.converters[turboshaft_0.tag]             ) 
    conditions.energy.converters[ram.tag]                      = deepcopy(conditions.energy.converters[ram_0.tag]                     )
    conditions.energy.converters[inlet_nozzle.tag]             = deepcopy(conditions.energy.converters[inlet_nozzle_0.tag]            ) 
    conditions.energy.converters[compressor.tag]               = deepcopy(conditions.energy.converters[compressor_0.tag] )
    conditions.energy.converters[high_pressure_compressor.tag] = deepcopy(conditions.energy.converters[high_pressure_compressor_0.tag])
    conditions.energy.converters[combustor.tag]                = deepcopy(conditions.energy.converters[combustor_0.tag]               )
    conditions.energy.converters[low_pressure_turbine.tag]     = deepcopy(conditions.energy.converters[low_pressure_turbine_0.tag]    ) 
    conditions.energy.converters[core_nozzle.tag]              = deepcopy(conditions.energy.converters[core_nozzle_0.tag]             ) 
  
    P_mech = conditions.energy.converters[turboshaft.tag].power
    P_elec = P_mech * 0
    
    return P_mech , P_elec