
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import  RCAIDE 
from RCAIDE.Framework.Core    import Units

# python imports 
import  numpy as  np
import  copy 
 
# ----------------------------------------------------------------------------------------------------------------------
# Main Wing Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_wing_weight(vehicle, wing, WPOD, complexity, settings, num_main_wings):
    """
    Calculate the wing weight using FLOPS methodology for general aviation aircraft. The wing weight consists of:
        - Bending Material Weight
        - Shear Material and Control Surface Weight
        - Miscellaneous Items Weight

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing:
            - reference_area : float
                Wing surface area [m^2]
            - mass_properties.max_takeoff : float
                Maximum takeoff weight [kg]
            - flight_envelope.ultimate_load : float
                Ultimate load factor
            - fuselages.width : float
                Width of the fuselage [m]
            - networks : list
                List of propulsion networks
    wing : RCAIDE.Component()
        Wing data structure containing:
            - taper : float
                Wing taper ratio
            - sweeps.quarter_chord : float
                Quarter chord sweep angle [deg]
            - thickness_to_chord : float
                Thickness to chord ratio
            - spans.projected : float
                Wing span [m]
            - chords.root : float
                Root chord [m]
            - chords.tip : float
                Tip chord [m]
            - twists.root : float
                Wing twist at root [deg]
            - twists.tip : float
                Wing twist at tip [deg]
            - flap_ratio : float
                Flap area to wing area ratio
    WPOD : float
        Weight of engine pod including nacelle [kg]
    complexity : str
        Wing weight method, either "simple" or "complex"
    settings : Data()
        Settings containing:
            - FLOPS.aeroelastic_tailoring_factor : float
                Aeroelastic tailoring factor [0-1]
            - FLOPS.strut_braced_wing_factor : float
                Strut braced wing factor [0-1]
            - advanced_composites : bool
                Flag for composite construction
    num_main_wings : int
        Number of main wings

    Returns
    -------
    wing_weight : float
        Total wing weight [kg]

    Notes
    -----
    The function implements two FLOPS methods: a simple and a complex approach.
    The complex method uses detailed spanwise integration for more accurate results.
    
    **Major Assumptions**
        * Wing is elliptically loaded
        * Gloved wing area is 0
        * Load between multiple main wings is distributed equally
        * Wing sweep is fixed
        * For complex method: 500 integration stations used
    
    **Theory**

    Simple Method:
    .. math::
        W_w = W_1 + W_2 + W_3

    Where:
        W_1 (Bending material):
    .. math::
        W_1 = \\frac{DG * CAYE * W_{1NIR} + W_2 + W_3}{1 + W_{1NIR}} - W_2 - W_3

    W_2 (Shear material):
    .. math::
        W_2 = A_2 * (1 - 0.17F_{comp}) * S_{flap}^{A_3} * DG^{A_4}

    W_3 (Miscellaneous):
    .. math::
        W_3 = A_5 * (1 - 0.3F_{comp}) * S_w^{A_6}

    Where:
        - W_w is total wing weight [lb]
        - DG is design gross weight [lb]
        - CAYE is engine weight relief factor
        - F_comp is composite utilization factor
        - S_flap is flap area [ft^2]
        - S_w is wing area [ft^2]
        - A_i are empirical constants

    Complex Method:
    Uses numerical integration of spanwise loads with 500 stations. The complex method accounts for:
        - Actual wing geometry through detailed station data
        - Engine weight relief effects
        - Sweep angle variations
        - Thickness distribution
        - Chord distribution
        - Actual load distribution
    
    The process follows:

    1. Spanwise Load Distribution:
    .. math::
        P(y) = \\sqrt{1 - (\\frac{y}{b/2})^2}

    2. Local Loads and Moments:
    .. math::
        \\Delta P = \\frac{\\Delta y}{6}[c_0(2P_0 + P_1) + c_1(2P_1 + P_0)]
        
        \\Delta M = \\frac{\\Delta y^2}{12}[c_0(3P_0 + P_1) + c_1(P_1 + P_0)]

    3. Cumulative Loads:
    .. math::
        L(y) = \\sum_{i=y}^{b/2} \\Delta P_i
        
        M(y) = \\sum_{i=y}^{b/2} (\\Delta M_i + \\Delta y L_i) \\sec(\\Lambda_i)

    4. Bending Material Area:
    .. math::
        BMA(y) = \\frac{M(y)}{c(y)t(y)} \\sec(\\Lambda)

    5. Engine Effects:
    .. math::
        M_e(y) = \\sum_{i=y}^{b/2} \\Delta y_i E(y_i) \\sec(\\Lambda_i)
        
        BMA_e(y) = \\frac{M_e(y)}{c(y)t(y)} \\sec(\\Lambda)

    6. Final Wing Weight:
    .. math::
        W_w = W_1 + W_2 + W_3

    Where:
        - y is spanwise station location
        - b is wing span
        - c is local chord
        - t is local thickness
        - P is normalized pressure loading
        - Λ is local sweep angle
        - E(y) is engine weight relief
        - W_1 is bending material weight
        - W_2 is shear material weight
        - W_3 is miscellaneous items weight

    References
    ----------
    [1] NASA. (1979). The Flight Optimization System Weights Estimation Method. 
        NASA Technical Report.
    """
    SW          = wing.areas.reference / (Units.ft ** 2)  # Reference wing area, ft^2
    GLOV        = 0 
    SX          = SW - GLOV  # Wing trapezoidal area
    SPAN        = wing.spans.projected / Units.ft  # Wing span, ft
    SEMISPAN    = SPAN / 2
    AR          = SPAN ** 2 / SX  # Aspect ratio
    TR          = wing.taper  # Taper
    
    aeroelastic_tailoring_factor = settings.FLOPS.aeroelastic_tailoring_factor
    strut_braced_wing_factor     = settings.FLOPS.strut_braced_wing_factor
    if settings.advanced_composites: # This considers full or no composite construction
        composite_utilization_factor = 0.0
    else:
        composite_utilization_factor = 1.0
    
    if AR <= 5:
        CAYA = 0
    else:
        CAYA = AR - 5
    # Aeroelastic tailoring factor [0 no aeroelastic tailoring, 1 maximum aeroelastic tailoring]
    FAERT           = aeroelastic_tailoring_factor  
    # Wing strut bracing factor [0 for no struts, 1 for struts]
    FSTRT           = strut_braced_wing_factor 
    
    NENG = 0
    NEW  = 0
    for network in  vehicle.networks:
        for propulsor in network.propulsors:
            if isinstance(propulsor, RCAIDE.Library.Components.Powertrain.Propulsors.Turbofan) or  isinstance(propulsor, RCAIDE.Library.Components.Powertrain.Propulsors.Turbojet):
                NENG += 1  
                if propulsor.wing_mounted: 
                    NEW += 1
                        
    DG              = vehicle.mass_properties.max_takeoff / Units.lbs  # Design gross weight in lb

    if complexity == 'Simple':
        EMS  = 1 - 0.25 * FSTRT  # Wing strut bracing factor
        TLAM = np.tan(wing.sweeps.quarter_chord) \
               - 2 * (1 - TR) / (AR * (1 + TR))  # Tangent of the 3/4 chord sweep angle
        SLAM = TLAM / np.sqrt(1 + TLAM ** 2)  # sine of 3/4 chord wing sweep angle
        C6   = 0.5 * FAERT - 0.16 * FSTRT
        C4   = 1 - 0.5 * FAERT
        CAYL = (1.0 - SLAM ** 2) * \
               (1.0 + C6 * SLAM ** 2 + 0.03 * CAYA * C4 * SLAM)  # Wing sweep factor due to aeroelastic tailoring
        TCA  = wing.thickness_to_chord
        BT   = 0.215 * (0.37 + 0.7 * TR) * (SPAN ** 2 / SW) ** EMS / (CAYL * TCA)  # Bending factor
        CAYE = 1 - 0.03 * NEW

    else:
        NSD             = 500
        N2              = int(NEW / 2) 
        L_fus           = 0
        for fuselage in vehicle.fuselages:
            if L_fus < fuselage.lengths.total:
                ref_fuselage = fuselage 
        ETA, C, T, SWP  = generate_wing_stations(ref_fuselage.width, copy.deepcopy(wing))
        NS, Y           = generate_int_stations(NSD, ETA)
        EETA            = get_spanwise_engine(vehicle.networks,SEMISPAN)
        P0              = calculate_load(ETA[-1])
        ASW             = 0
        EM              = 0
        EL              = 0
        C0              = C[-1]
        S               = 0
        EEL             = 0
        EEM             = 0
        EA0             = 0
        EW              = 0
        
        
        # Replaced FOR LOOP
        # Reverse Order
        Y  = np.flip(Y)
        
        # DY distance
        DY = np.diff(Y)
        
        # Trim the vectors away from the tip and center
        Y  = Y[1:-2]
        DY = -DY[0:-2]
        
        # Get normalized pressure loading across the wing
        P1     = calculate_load(Y)
        P0     = np.zeros_like(P1)
        P0[1:] = P1[0:-1]
        
        # Get local chord length
        C1     = np.interp(Y, ETA, C)
        C0     = np.zeros_like(C1)
        C0[0]  = C[-1]
        C0[1:] = C1[0:-1]
        
        # Calculate local pressure load and moments (DELP and DELM)
        T1   = np.interp(Y, ETA, T)
        SWP1 = find_sweep(Y,ETA,SWP)
        DELP = DY / 6 * (C0 * (2 * P0 + P1) + C1 * (2 * P1 + P0))
        DELM = DY ** 2 * (C0 * (3.0 * P0 + P1) + C1 * (P1 + P0)) / 12.
        
        # Sum loads
        EL     = np.zeros_like(DELP) 
        EL[1:] = np.cumsum(DELP[0:-1])
        
        # Sum moments
        EM     = np.cumsum((DELM + DY * EL) * 1 / np.cos(SWP1))
        
        # Calculate required bending material area
        BMA1     = EM * 1 / np.cos(SWP1) * 1 / (C1 * T1)
        
        BMA0     = np.zeros_like(BMA1)
        BMA0[1:] = BMA1[0:-1]
        
        # Compute segment values
        ASW  = np.cumsum((DY + 2 * Y) * DY * SWP1)
        PM   = np.cumsum((BMA0 + BMA1) * DY / 2.)
        S    = np.cumsum((C0 + C1) * DY / 2.)


        # Adjust for engine loads
        if N2>0: # If there are engines
            EEL   = np.zeros_like(Y)
            DELM2 = np.zeros_like(Y)
            
            # Do a for loop over engine stations
            for ii in range(len(EETA)):
                # Find the station closest to the engine but inboard
                distances              = EETA[ii]-Y
                distances[distances<0] = np.inf
                distance               = np.min(distances)
                loc                    = np.argmin(distances)
                DELM2[loc]             = DELM2[loc] + distance
                EEL[loc+1:]            = EEL[loc+1:] + 1

            DELM2 = DELM2 + EEL*DY

            EEM = np.cumsum(DELM2/np.cos(SWP1))
            EA1 = EEM * 1 / np.cos(SWP1) * 1 / (C1 * T1)
            
            EA0 = np.zeros_like(Y)
            EA0[1:] = EA1[0:-1]
            
            EW  = np.sum((EA0 + EA1) * DY / 2)
            
        # Finalize properties
        EL = EL[-1] + DELP[-1]    
        EM = EM[-1] / EL
        PM = 4. * PM[-1] / EL
        EW = 8. * EW
        SA = np.sin(ASW[-1])
        AR = 2 / S[-1]       
                
        if AR <= 5:
            CAYA = 0
        else:
            CAYA = AR - 5
        DEN = AR ** (.25 * FSTRT) * (1.0 + (.50 * FAERT - .160 * FSTRT) * SA ** 2 /
                                     + .03 * CAYA * (1.0 - .50 * FAERT) * SA)
        BT = PM / DEN
        BTE = EW
        CAYE = 1
        if NEW > 0:
            CAYE = 1 - BTE / BT * WPOD / DG

    A       = wing_weight_constants_FLOPS()  # Wing weight constants
    # Composite utilization factor [0 no composite, 1 full composite]
    FCOMP   = composite_utilization_factor  
    ULF     = vehicle.flight_envelope.ultimate_load
    if len(vehicle.fuselages) == 1:
        CAYF    = 1  # Multiple fuselage factor [1 one fuselage, 0.5 multiple fuselages]
    elif len(vehicle.fuselage) > 1:
        CAYF    = 0.5
    else:
        raise NotImplementedError
    VFACT   = 1  # Variable sweep factor, TODO: add equation to allow variable sweep penalty
    PCTL    = 1/num_main_wings  # Fraction of load carried by this wing
    W1NIR   = A[0] * BT * (1 + np.sqrt(A[1] / SPAN)) * ULF * SPAN * (1 - 0.4 * FCOMP) * (
                1 - 0.1 * FAERT) * CAYF * VFACT * PCTL / 10.0 ** 6  # Wing bending material weight lb
    SFLAP   = wing.flap_ratio * SX

    W2 = A[2] * (1 - 0.17 * FCOMP) * SFLAP ** (A[3]) * DG ** (A[4])  # shear material weight
    W3 = A[5] * (1 - 0.3 * FCOMP) * SW ** (A[6])  # miscellaneous items weight
    W1 = (DG * CAYE * W1NIR + W2 + W3) / (1 + W1NIR) - W2 - W3  # bending material weight
    WWING = W1 + W2 + W3  # Total wing weight

    return WWING * Units.lbs


def generate_wing_stations(fuselage_width, wing):
    """ Divides half the wing in sections, using the defined sections
        and adding a section at the intersection of wing and fuselage

        Assumptions:

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            fuselage_width: fuselage width                                      [m]
            wing: data dictionary with wing properties
                    -.taper: taper ration wing
                    -.sweeps.quarter_chord: quarter chord sweep angle           [deg]
                    -.thickness_to_chord: thickness to chord
                    -.spans.projected: wing span                                [m]
                    -.chords.root: root chord                                   [m]
                    -.tip.root: tip chord                                       [m]
                    -.twists.root: twist of wing at root                        [deg]
                    -.twists.tip: twist of wing at tip                          [deg]
                    -.Segments: trapezoidal segments of the wing

       Outputs:
           ETA: spanwise location of the sections normalized by half span
           C: chord lengths at every spanwise location in ETA normalized by half span
           T: thickness to chord ratio at every span wise location in ETA
           SWP: quarter chord sweep angle at every span wise location in ETA

        Properties Used:
            N/A
    """
    SPAN        = wing.spans.projected / Units.ft  # Wing span, ft
    SEMISPAN    = SPAN / 2
    root_chord  = wing.chords.root / Units.ft
    num_seg     = len(wing.segments.keys())

    if num_seg == 0:
        segment                         = RCAIDE.Library.Components.Wings.Segments.Segment()
        segment.tag                     = 'root'
        segment.percent_span_location   = 0.
        segment.twist                   = wing.twists.root
        segment.root_chord_percent      = 1
        segment.dihedral_outboard       = 0.
        segment.sweeps.quarter_chord    = wing.sweeps.quarter_chord
        segment.thickness_to_chord      = wing.thickness_to_chord
        wing.segments.append(segment)

        segment                         = RCAIDE.Library.Components.Wings.Segments.Segment()
        segment.tag                     = 'tip'
        segment.percent_span_location   = 1.
        segment.twist                   = wing.twists.tip
        segment.root_chord_percent      = wing.chords.tip / wing.chords.root
        segment.dihedral_outboard       = 0.
        segment.sweeps.quarter_chord    = wing.sweeps.quarter_chord
        segment.thickness_to_chord      = wing.thickness_to_chord
        wing.segments.append(segment)
        num_seg = len(wing.segments.keys())
        
    ETA    = np.zeros(num_seg + 1)
    C      = np.zeros(num_seg + 1)
    T      = np.zeros(num_seg + 1)
    SWP    = np.zeros(num_seg + 1)

    segment_keys  = list(wing.segments.keys())     
    ETA[0] = wing.segments[segment_keys[0]].percent_span_location
    C[0]   = root_chord * wing.segments[segment_keys[0]].root_chord_percent * 1 / SEMISPAN
    SWP[0] = 0
    
    if hasattr(wing.segments[segment_keys[0]], 'thickness_to_chord'):
        T[0] = wing.segments[segment_keys[0]].thickness_to_chord
    else:
        T[0] = wing.thickness_to_chord
    ETA[1] = fuselage_width / 2 * 1 / Units.ft * 1 / SEMISPAN
    C[1] = determine_fuselage_chord(fuselage_width, wing) * 1 / SEMISPAN

    if hasattr(wing.segments[segment_keys[0]], 'thickness_to_chord'):
        T[1] = wing.segments[segment_keys[0]].thickness_to_chord
    else:
        T[1] = wing.thickness_to_chord
    for i in range(1, num_seg):
        ETA[i + 1] = wing.segments[segment_keys[i]].percent_span_location
        C[i + 1] = root_chord * wing.segments[segment_keys[i]].root_chord_percent * 1 / SEMISPAN
        if hasattr(wing.segments[segment_keys[i]], 'thickness_to_chord'):
            T[i + 1] = wing.segments[segment_keys[i]].thickness_to_chord
        else:
            T[i + 1] = wing.thickness_to_chord
        SWP[i] = np.arctan(np.tan(wing.segments[segment_keys[i-1]].sweeps.quarter_chord) - (C[i - 1] - C[i]))
    SWP[-1] = np.arctan(np.tan(wing.segments[segment_keys[-2]].sweeps.quarter_chord) - (C[-2] - C[-1]))
    return ETA, C, T, SWP


def generate_int_stations(NSD, ETA):
    """ Divides half of the wing in integration stations

        Assumptions:

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            NSD: number of integration stations requested
            ETA: list of spanwise locations of all sections of the wing

       Outputs:
           NS: actual number of integration stations
           Y: spanwise locations of the integrations stations normalized by half span

        Properties Used:
            N/A
    """
    Y           = [ETA[1]]
    desired_int = (ETA[-1] - ETA[1]) / NSD
    NS          = 0
    for i in range(2, len(ETA)):
        NP = int((ETA[i] - ETA[i - 1]) / desired_int + 0.5)
        if NP < 1:
            NP = 1
        AINT = (ETA[i] - ETA[i - 1]) / NP
        for j in range(NP):
            NS = NS + 1
            Y.append(Y[-1] + AINT)
    return NS, Y


def calculate_load(ETA):
    """ Returns load factor assuming elliptical load distribution

        Assumptions:

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            ETA: list of spanwise locations of all sections of the wing

       Outputs:
           PS: load factor at every location in ETA assuming elliptical load distribution

        Properties Used:
            N/A
    """
    PS = np.sqrt(1. - ETA ** 2)
    return PS


def find_sweep(y, lst_y, swp):
    """ Finds sweep angle for a certain y-location along the wing

        Assumptions:

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            y: spanwise location
            lst_y: list of spanwise stations where sweep is known (eg sections)
            swp: list of quarter chord sweep angles at the locations listed in lst_y

       Outputs:
           swps: sweep angle at y

        Properties Used:
            N/A
    """
    
    # All initial sweeps are the root chord sweep
    swps = np.ones_like(y)*swp[0]
    
    for i in range(len(lst_y)-1):
        e       = lst_y[i]
        swps[y>=e] = swp[i]
        

    return swps


def get_spanwise_engine(networks, SEMISPAN):
    """ Returns EETA for the engine locations along the wing

        Assumptions:

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            networks: data dictionary with all the engine properties
                -.wing_mounted: list of boolean if engine is mounted to wing
                -.number_of_engines: number of engines
                -.origin: origin of the engine
            SEMISPAN: half span                                 [m]
       Outputs:
           EETA: span wise locations of the engines mounted to the wing normalized by the half span

        Properties Used:
            N/A
    """
    EETA =  []
    for network in  networks:
        for propulsor in network.propulsors:
            if isinstance(propulsor, RCAIDE.Library.Components.Powertrain.Propulsors.Turbofan) or  isinstance(propulsor, RCAIDE.Library.Components.Powertrain.Propulsors.Turbojet):
                if propulsor.wing_mounted and propulsor.origin[0][1] > 0:  
                    EETA.append((propulsor.origin[0][1] / Units.ft) * 1 / SEMISPAN) 
    EETA =  np.array(EETA)
    return EETA


def wing_weight_constants_FLOPS():
    """Defines wing weight constants as defined by FLOPS
        Inputs: ac_type - determines type of instruments, electronics, and operating items based on types:
                "short-range", "medium-range", "long-range", "business", "cargo", "commuter", "sst"
        Outputs: list of coefficients used in weight estimations

    """
    A = [30,0,0.25,0.5,0.5,0.16,1.2]
    return A


def determine_fuselage_chord(fuselage_width, wing):
    """ Determine chord at wing and fuselage intersection

        Assumptions:
            Fuselage side of body is between first and second wing segments.

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            fuselage_width: width of fuselage                                   [m]
            wing: data dictionary with wing properties
                    -.taper: taper ratio
                    -.sweeps.quarter_chord: quarter chord sweep angle           [deg]
                    -.thickness_to_chord: thickness to chord
                    -.spans.projected: wing span                                [m]
                    -.chords.root: root chord                                   [m]
                -.fuselages.fuselage.width: fuselage width                      [m]
       Outputs:
           chord: chord length of wing where wing intersects the fuselage wall [ft]

        Properties Used:
            N/A
    """

    segment_keys    = list(wing.segments.keys())      
    root_chord      = wing.chords.root / Units.ft
    SPAN            = wing.spans.projected / Units.ft  # Wing span, ft
    SEMISPAN        = SPAN / 2
    c1              = root_chord * wing.segments[segment_keys[0]].root_chord_percent
    c2              = root_chord * wing.segments[segment_keys[-1]].root_chord_percent
    y1              = wing.segments[segment_keys[0]].percent_span_location
    y2              = wing.segments[segment_keys[1]].percent_span_location
    b               = (y2 - y1) * SEMISPAN
    taper           = c2 / c1
    y               = fuselage_width / 2 * 1 / Units.ft
    chord           = c1 * (1 - (1 - taper) * 2 * y / b)
    return chord