# RCAIDE/Library/Methods/Performance/compute_payload_range_diagram.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core import Units , Data  
from RCAIDE.Library.Plots.Common import set_axes, plot_style    
 
# Pacakge imports 
import numpy as np
from matplotlib import pyplot as plt
 
# ----------------------------------------------------------------------
#  Calculate vehicle Payload Range Diagram
# ----------------------------------------------------------------------  
def compute_payload_range_diagram(mission = None, cruise_segment_tag = "cruise", fuel_reserve_percentage=0., plot_diagram = True, fuel_name=None):  
    """
    Calculate and plot the payload range diagram for an aircraft by modifying the cruise segment and weights.
    
    Parameters
    ----------
    mission : Data
        Data structure containing the mission to be analyzed
    cruise_segment_tag : str, optional
        String identifier for the cruise segment in the mission
        Default: "cruise"
    fuel_reserve_percentage : float, optional
        Fraction of maximum fuel to be reserved (not used for range)
        Default: 0.0
    plot_diagram : bool, optional
        Flag to generate payload-range plots
        Default: True
    fuel_name : str, optional
        Name of fuel for plot title
        Default: None
    
    Returns
    -------
    payload_range : Data
        Data structure containing payload range properties
        - range : ndarray
            Range values for each point [m]
        - payload : ndarray
            Payload values for each point [kg]
        - oew_plus_payload : ndarray
            Operating empty weight plus payload for each point [kg]
        - fuel : ndarray
            Fuel weight for each point [kg]
        - takeoff_weight : ndarray
            Takeoff weight for each point [kg]
        - fuel_reserve_percentage : float
            Fraction of fuel reserved
    
    Notes
    -----
    Computes three key points for conventional aircraft:
        1. Maximum payload at maximum takeoff weight
        2. Maximum fuel with maximum takeoff weight
        3. Maximum fuel with zero payload (ferry range)
    
    For electric aircraft computes:
        1. Maximum payload range
        2. Ferry range (zero payload)

    **Major Assumptions**
        * Constant cruise speed and altitude
        * Fixed reserve fuel fraction
        * Linear interpolation between payload-range points
        * Battery energy content remains constant (electric aircraft)
    
    **Theory**
    The payload-range diagram shows the trade-off between how much payload an aircraft
    can carry versus how far it can fly. For conventional aircraft, the diagram typically
    has three segments:
    
    1. Maximum payload segment: Range increases by burning fuel initially loaded
    2. Maximum fuel segment: Range increases by trading payload for fuel
    3. Ferry range segment: Maximum range with zero payload
    
    For electric aircraft, the diagram is simpler with just two points connected by
    a straight line, as there is no fuel weight to trade for payload.
    
    See Also
    --------
    RCAIDE.Library.Methods.Performance.conventional_payload_range_diagram
    RCAIDE.Library.Methods.Performance.electric_payload_range_diagram
    """ 
            
    if mission == None:
        raise AssertionError('Mission not specifed!')
    
    initial_segment =  list(mission.segments.keys())[0]
    
    # perform inital weights analysis 
    weights_analysis   = mission.segments[initial_segment].analyses.weights 
    weights_analysis.evaluate() # evaluate weights to make sure mass variables are defined 
    vehicle = weights_analysis.vehicle 
    
    for network in vehicle.networks:
        if type(network) == RCAIDE.Framework.Networks.Fuel:  
            payload_range  =  conventional_payload_range_diagram(vehicle,mission,cruise_segment_tag,fuel_reserve_percentage,plot_diagram,fuel_name) 
        else:
            payload_range  =  electric_payload_range_diagram(vehicle,mission,cruise_segment_tag,plot_diagram)
    return payload_range 
             
def conventional_payload_range_diagram(vehicle,mission,cruise_segment_tag,fuel_reserve_percentage,plot_diagram, fuel_name): 
    """Calculates and plots the payload range diagram for a fuel-bases aircraft by modifying the
    cruise segment range and weights of the aicraft .

        Sources:
        N/A

        Assumptions:
        None 

        Inputs:
            vehicle             data structure for aircraft                  [-]
            mission             data structure for mission                   [-] 
            cruise_segment_tag  string of cruise segment                     [string]
            fuel_reserve_percentage            reserve fuel                                 [unitless] 
            
        Outputs: 
            payload_range       data structure of payload range properties   [m/s]
    """ 
    #unpack
    mass = vehicle.mass_properties
    if not mass.operating_empty:
        raise AttributeError("Error calculating Payload Range Diagram: Vehicle Operating Empty not defined") 
    else:
        OEW = mass.operating_empty

    if not mass.max_zero_fuel:
        raise AttributeError("Error calculating Payload Range Diagram: Vehicle MZFW not defined") 
    else:
        MZFW = vehicle.mass_properties.max_zero_fuel

    if not mass.max_takeoff:
        raise AttributeError("Error calculating Payload Range Diagram: Vehicle MTOW not defined") 
    else:
        MTOW = vehicle.mass_properties.max_takeoff

    if mass.max_payload == 0:
        MaxPLD = MZFW - OEW  
    else:
        MaxPLD = vehicle.mass_properties.max_payload
        MaxPLD = min(MaxPLD , MZFW - OEW) #limit in structural capability

    if mass.max_fuel == 0:
        MaxFuel = MTOW - OEW # If not defined, calculate based in design weights
    else:
        MaxFuel = vehicle.mass_properties.max_fuel  # If max fuel capacity not defined
        MaxFuel = min(MaxFuel, MTOW - OEW)


    # Define payload range points
    #Point  = [ RANGE WITH MAX. PLD   , RANGE WITH MAX. FUEL , FERRY RANGE   ]
    TOW     = [ MTOW                               , MTOW                   , OEW + MaxFuel ]
    FUEL    = [ min(TOW[1] - OEW - MaxPLD,MaxFuel) , MaxFuel                , MaxFuel       ]
    PLD     = [ MaxPLD                             , MTOW - MaxFuel - OEW   , 0.   ]
    OEW_PLD = [  OEW + MaxPLD                      , MTOW - MaxFuel         , OEW  ]
    
    # allocating Range array
    R       = [0,0,0]

    # loop for each point of Payload Range Diagram
    for i in range(len(TOW)):
        ##    for i in [2]: 
        # Define takeoff weight
        mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff  = TOW[i]
        mission.segments[0].analyses.weights.vehicle.mass_properties.payload  = PLD[i]
        mission.segments[0].analyses.weights.vehicle.mass_properties.fuel     = FUEL[i]

        # Evaluate mission with current TOW
        results = mission.evaluate()
        segment = results.segments[cruise_segment_tag]

        # Distance convergency in order to have total fuel equal to target fuel
        #
        # User don't have the option of run a mission for a given fuel. So, we
        # have to iterate distance in order to have total fuel equal to target fuel
        #

        maxIter = 10    # maximum iteration limit
        tol     = 1.    # fuel convergency tolerance
        err     = 9999. # error to be minimized
        iter    = 0     # iteration count

        while abs(err) > tol and iter < maxIter:
            iter = iter + 1

            # Current total fuel burned in mission
            TotalFuel  = results.segments[-1].conditions.energy.cumulative_fuel_consumption[-1, 0]

            # Difference between burned fuel and target fuel
        
            reserve_fuel = fuel_reserve_percentage * MaxFuel
            missingFuel = FUEL[i] - TotalFuel - reserve_fuel

            # Current distance and fuel consuption in the cruise segment
            CruiseDist = np.diff( segment.conditions.frames.inertial.position_vector[[0,-1],0] )[0]        # Distance [m]
            CruiseFuel = segment.conditions.weights.total_mass[0,0] - segment.conditions.weights.total_mass[-1,0]    # [kg]
            
            # Current specific range (m/kg)
            CruiseSR    = CruiseDist / CruiseFuel        # [m/kg]

            # Estimated distance that will result in total fuel burn = target fuel
            DeltaDist  =  CruiseSR *  missingFuel
            mission.segments[cruise_segment_tag].distance = (CruiseDist + DeltaDist)

            # running mission with new distance
            results = mission.evaluate()
            segment = results.segments[cruise_segment_tag]

            # Difference between burned fuel and target fuel
            err = ( TOW[i] - results.segments[-1].conditions.weights.total_mass[-1,0] ) - FUEL[i] + reserve_fuel

            if iter == maxIter:
                print(f"Did not converge.")
                break

        # Allocating resulting range in ouput array.
        R[i] =  results.segments[-1].conditions.frames.inertial.position_vector[-1,0]   

    # Inserting point (0,0) in output arrays
    R.insert(0,0)
    PLD.insert(0,MaxPLD) 
    OEW_PLD.insert(0,OEW + MaxPLD   ) 
    FUEL.insert(0,0)
    TOW.insert(0,0)

    # packing results
    payload_range                          = Data()
    payload_range.range                    = np.array(R)
    payload_range.payload                  = np.array(PLD)
    payload_range.oew_plus_payload         = np.array(OEW_PLD)
    payload_range.fuel                     = np.array(FUEL)
    payload_range.takeoff_weight           = np.array(TOW)
    payload_range.fuel_reserve_percentage  = fuel_reserve_percentage
     
    if plot_diagram:  
        # get plotting style 
        ps      = plot_style()  
    
        parameters = {'axes.labelsize': ps.axis_font_size,
                      'xtick.labelsize': ps.axis_font_size,
                      'ytick.labelsize': ps.axis_font_size,
                      'axes.titlesize': ps.title_font_size}
        plt.rcParams.update(parameters)
        
        if fuel_name ==  None: 
            fig  = plt.figure( vehicle.tag + ' Fuel_Payload_Range_Diagram')
        else:
            fig  = plt.figure(vehicle.tag + ' Fuel_Payload_Range_Diagram for ' + fuel_name)
        axis_1 = fig.add_subplot(1,2,1)
        axis_1.plot(payload_range.range /Units.nmi,payload_range.payload/Units.lbm  ,color = 'k', linewidth = ps.line_width )
        axis_1.set_xlabel('Range (nautical miles)')
        axis_1.set_ylabel('Payload (lbs)') 
        set_axes(axis_1) 

        axis_2 = fig.add_subplot(1,2,2)
        axis_2.plot(payload_range.range /Units.nmi,payload_range.oew_plus_payload/Units.lbm ,color = 'k', linewidth = ps.line_width )
        axis_2.set_xlabel('Range (nautical miles)')
        axis_2.set_ylabel('OEW + Payload (lbs)') 
        set_axes(axis_2) 
        fig.tight_layout()

    return payload_range 
 
def electric_payload_range_diagram(vehicle,mission,cruise_segment_tag,plot_diagram):
    """Calculates and plots the payload range diagram for an electric aircraft by modifying the
    cruise segment distance and payload weight of the aicraft .

        Sources:
        N/A

        Assumptions:
        None 

        Inputs:
            vehicle             data structure for aircraft                  [-]
            mission             data structure for mission                   [-] 
            cruise_segment_tag  string of cruise segment                     [string]
            fuel_reserve_percentage            reserve fuel                                 [unitless] 
            
        Outputs: 
            payload_range       data structure of payload range properties   [m/s]
    """ 
    mass = vehicle.mass_properties
    if not mass.operating_empty:
        raise AttributeError("Error calculating Payload Range Diagram: vehicle Operating Empty Weight is undefined.") 
    else:
        OEW = mass.operating_empty

    if not mass.max_payload:
        raise AttributeError("Error calculating Payload Range Diagram: vehicle Maximum Payload Weight is undefined.") 
    else:
        MaxPLD = mass.max_payload

    if not mass.max_takeoff:
        raise AttributeError("Error calculating Payload Range Diagram: vehicle Maximum Payload Weight is undefined.") 
    else:
        MTOW = mass.max_takeoff

    # Define Diagram Points
    # Point = [Value at Maximum Payload Range,  Value at Ferry Range]
    TOW =   [MTOW,      OEW]    # Takeoff Weights
    PLD =   [MaxPLD,    0.]     # Payload Weights

    # Initialize Range Array
    R = np.zeros(2)

    # Calculate Vehicle Range for Max Payload and Ferry Conditions
    for i in range(2):
        mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff = TOW[i]
        results = mission.evaluate()
        segment = results.segments[cruise_segment_tag]
        R[i]    = segment.conditions.frames.inertial.position_vector[-1,0] 

    # Insert Starting Point for Diagram Construction
    R   = np.insert(R, 0, 0)
    PLD = np.insert(PLD, 0, MaxPLD)
    TOW = np.insert(TOW, 0, 0)

    # Pack Results
    payload_range = Data()
    payload_range.range             = np.array(R)
    payload_range.payload           = np.array(PLD)
    payload_range.takeoff_weight    = np.array(TOW)

    if plot_diagram: 
        # get plotting style 
        ps      = plot_style()  
    
        parameters = {'axes.labelsize': ps.axis_font_size,
                      'xtick.labelsize': ps.axis_font_size,
                      'ytick.labelsize': ps.axis_font_size,
                      'axes.titlesize': ps.title_font_size}
        plt.rcParams.update(parameters)

        fig  = plt.figure('Electric_Payload_Range_Diagram')
        axis = fig.add_subplot(1,1,1)        
        axis.plot(payload_range.range /Units.nmi, payload_range.payload,color = 'k', linewidth = ps.line_width )
        axis.set_xlabel('Range (nautical miles)')
        axis.set_ylabel('Payload (kg)')
        axis.set_title('Payload Range Diagram')
        set_axes(axis) 
        fig.tight_layout()

    return payload_range