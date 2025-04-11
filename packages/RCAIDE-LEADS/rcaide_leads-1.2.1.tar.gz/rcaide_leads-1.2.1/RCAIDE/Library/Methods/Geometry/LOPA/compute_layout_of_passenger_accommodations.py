# RCAIDE/Library/Methods/Geometry/LOPA/LOPA_functions.py
# 
# 
# Created: Mar 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE 
from .LOPA_functions import *

# python functions 
import  numpy as  np 
from copy import  deepcopy

# ----------------------------------------------------------------------------------------------------------------------
#  compute_layout_of_passenger_accommodations
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_layout_of_passenger_accommodations(fuselage):
    '''
    Creates the layout of passenger accommodations for a vehicle
    '''  
    #  [ x, y, z , length, width, first-cl flag, business-cl flag, economy-cl flag, seat, emergency-row flag, galley/lav flag, type-A exit flag]    
    LOPA = np.empty(( 0, 14)) 
    side_cabin_offset = 0
    for cabin in fuselage.cabins: 
        cabin_class_origin  = [0, 0, 0]
        for cabin_class in cabin.classes: 
            seat_data ,cabin_class_origin  = create_class_seating_map_layout(cabin, cabin_class,cabin_class_origin, side_cabin_offset)
            side_cabin_offset =  cabin.width / 2
            LOPA = np.vstack((LOPA,seat_data))  
            
    for cabin in fuselage.cabins: 
        for cabin_class in cabin.classes: 
            cabin_class.percentage = cabin_class.length/cabin.length

    fuselage.number_of_passengers               = np.sum(LOPA[:,10])
    fuselage.layout_of_passenger_accommodations = LOPA
    compute_fusselage_dimensions(fuselage)

    return  
 
def compute_fusselage_dimensions(fuselage):
    LOPA = fuselage.layout_of_passenger_accommodations 
    
       # Step 1: plot cabin bounds  
    # get points at x min 
    x_min_locs   =  np.where( LOPA[:,2] == min(LOPA[:,2]))[0]
    x_min        =  LOPA[x_min_locs[0],2] -  LOPA[x_min_locs[0],5]/2
    x_min_y_max  =  max(LOPA[x_min_locs,3] + LOPA[x_min_locs,6]/2 )
    x_min_y_min  =  min(LOPA[x_min_locs,3] - LOPA[x_min_locs,6]/2 ) 
    x_border_pts = [x_min, x_min] 
    y_border_pts = [x_min_y_min, x_min_y_max] 

    # get points at y max 
    y_max_locs   =  np.where( LOPA[:,3] == max(LOPA[:,3]))[0]
    y_max        =  LOPA[y_max_locs[0],3] + LOPA[y_max_locs[0],6]/2 
    y_max_x_max  =  max(LOPA[y_max_locs,2] + LOPA[y_max_locs[0],5]/2)
    y_max_x_min  =  min(LOPA[y_max_locs,2] - LOPA[y_max_locs[0],5]/2) 
    x_border_pts.append(y_max_x_min)
    x_border_pts.append(y_max_x_max)
    y_border_pts.append(y_max)
    y_border_pts.append(y_max) 

    # get points at x max 
    x_max_locs   =  np.where( LOPA[:,2] == max(LOPA[:,2]))[0]
    x_max        =  LOPA[x_max_locs[0],2] + LOPA[x_max_locs[0],5]/2
    x_max_y_max  =  max(LOPA[x_max_locs,3] + LOPA[x_max_locs,6]/2)
    x_max_y_min  =  min(LOPA[x_max_locs,3] - LOPA[x_max_locs,6]/2)  
    x_border_pts.append(x_max)
    x_border_pts.append(x_max)
    y_border_pts.append(x_max_y_max)
    y_border_pts.append(x_max_y_min)
    
    # get points at y min  
    y_min_locs   =  np.where( LOPA[:,3] == min(LOPA[:,3]))[0]
    y_min        =  LOPA[y_min_locs[0],3] - LOPA[y_min_locs[0],6]/2 
    y_min_x_max  =  max(LOPA[y_min_locs,2] + LOPA[y_min_locs[0],5]/2)
    y_min_x_min  =  min(LOPA[y_min_locs,2] - LOPA[y_min_locs[0],5]/2)
    x_border_pts.append(y_min_x_max)  
    x_border_pts.append(y_min_x_min)
    y_border_pts.append(y_min)
    y_border_pts.append(y_min)    
    
    # loop through points and determine if there are duplicates
    y_border_pts = np.array(y_border_pts)
    x_border_pts = np.array(x_border_pts)

    # cut where y is negative
    port_idxs  =  np.where(y_border_pts<0)[0]
    starboard_x_points = np.delete(x_border_pts, port_idxs) 
    starboard_y_points = np.delete(y_border_pts, port_idxs)
    
    cabin_length = max(starboard_x_points)
    cabin_wdith = 2*max(starboard_y_points)

    fuselage.lengths.nose = fuselage.fineness.nose*cabin_wdith
    fuselage.lengths.tail = fuselage.fineness.tail*cabin_wdith  

    fuselage.lengths.total = fuselage.lengths.nose + fuselage.lengths.tail + cabin_length
    fuselage.width  = cabin_wdith

def create_class_seating_map_layout(cabin,cabin_class,cabin_class_origin, side_cabin_offset):  
    
    s_y_coord, cabin_class_origin = get_seat_y_coords(cabin, cabin_class,cabin_class_origin)
    s_x_coord,object_type, cabin_class_origin = get_seat_x_coords(cabin, cabin_class,cabin_class_origin) 
         
    # concatenate arrays 
    length   =  cabin_class.seat_length * np.ones_like(s_x_coord) 
    length[object_type[:,2] == 1] = cabin.galley_lavatory_length
    length[object_type[:,3] == 1] = cabin.type_A_door_length
    
    X_coords   = np.atleast_2d((np.tile(s_x_coord[:,None], (1, len(s_y_coord)))).flatten()).T
    Y_coords   = np.atleast_2d((np.tile(s_y_coord[None,:], (len(s_x_coord), 1))).flatten()).T
    Z_coords   = np.atleast_2d((np.zeros_like(Y_coords)).flatten()).T 
    length     = np.atleast_2d((np.tile(length[:,None], (1, len(s_y_coord)))).flatten()).T 
    width      = cabin_class.seat_width * np.ones_like(Z_coords) 
    n_rows     = cabin_class.number_of_rows * np.ones_like(Z_coords) 
    n_seats_y  = cabin_class.number_of_seats_abrest  * np.ones_like(Z_coords) 
    object_vec = np.repeat(object_type, len(s_y_coord), axis=0)
     
    # cabin class flags 
    F_c  =  np.zeros_like(Z_coords)
    B_c  =  np.zeros_like(Z_coords)
    E_c  =  np.zeros_like(Z_coords)     
    if type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.First: 
        F_c  =  np.ones_like(Z_coords) 
    elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Business: 
        B_c  =  np.ones_like(Z_coords) 
    elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Economy: 
        E_c  =  np.ones_like(Z_coords)  
    
    # [n_rows , n_seats_y, x, y, z , length, width, first-cl flag, business-cl flag, economy-cl flag, seat, emergency-row flag, galley/lav flag, type-A exit flag]    
    seat_data = np.hstack((n_rows , n_seats_y, X_coords,Y_coords, Z_coords, length ,width,F_c,B_c,E_c,object_vec))
     
    if type(cabin) == RCAIDE.Library.Components.Fuselages.Cabins.Side_Cabin:
        
        seat_data[:, 3] += cabin.width / 2
        seat_data  = update_seat_map_layout_using_cabin_taper(seat_data,cabin) 
        seat_data[:, 3] += side_cabin_offset  
        
        # make copy about center
        seat_data_        = deepcopy(seat_data)
        seat_data_[:, 3] *= -1 
        seat_data         = np.vstack((seat_data,seat_data_))
        
    return seat_data ,cabin_class_origin 


    
    