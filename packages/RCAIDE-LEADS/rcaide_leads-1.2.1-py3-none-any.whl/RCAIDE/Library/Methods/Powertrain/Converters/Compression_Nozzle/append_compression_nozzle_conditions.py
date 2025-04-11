# RCAIDE/Library/Methods/Powertrain/Converters/compression_nozzle/append_compression_nozzle_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports 
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
# append_compression_nozzle_conditions 
# ----------------------------------------------------------------------------------------------------------------------    
def append_compression_nozzle_conditions(compression_nozzle,segment,energy_conditions): 
    """
    Initializes and appends compression nozzle conditions data structure to the energy conditions dictionary.
    
    Parameters
    ----------
    compression_nozzle : CompressionNozzle
        The compression nozzle component for which conditions are being initialized.
    segment : Segment
        The mission segment in which the compression nozzle is operating.
    energy_conditions : dict
        Dictionary containing conditions for all propulsion components.
    
    Returns
    -------
    None
    
    Notes
    -----
    This function creates empty Conditions objects for the compression nozzle's inputs and outputs
    within the energy_conditions dictionary. These conditions will be populated during
    the mission analysis process.
    
    See Also
    --------
    RCAIDE.Library.Methods.Powertrain.Converters.Compression_Nozzle.compute_compression_nozzle_performance
    """
    energy_conditions.converters[compression_nozzle.tag]                     = Conditions()
    energy_conditions.converters[compression_nozzle.tag].inputs              = Conditions()
    energy_conditions.converters[compression_nozzle.tag].outputs             = Conditions()
    return 