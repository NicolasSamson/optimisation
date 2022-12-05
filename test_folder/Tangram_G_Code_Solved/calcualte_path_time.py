import copy 
from pandas import DataFrame, read_csv

from numpy import amax, argmax, stack,diff, hstack,linspace,array_equal,identity,array, cos,sin,sum , dot,ones,absolute, multiply,pi ,less,greater,logical_and,argwhere,radians,transpose,ones,vstack,where
from numpy.linalg import norm,inv
from numpy.random import rand
from scipy.interpolate import interp1d

import test_py_constraint_all_piece as tcp
import optimization_zone_depot as ozd
import create_path as cp
from os.path import join

import matplotlib.pyplot as plt

time_pick_place = 4604/1000 # ms


def create_interpolation_function(general_path):
    # Create the interpolate function of each axes. 
    
    path_x = join(general_path,r"interpolate_funct_time\axe_x.csv")
    path_y = join(general_path, r"interpolate_funct_time\axe_y.csv")
    path_theta = join(general_path,r"interpolate_funct_time\axe_theta.csv")


    df_x = read_csv(path_x,header=None, names = ["deltas","time1","time2"])
    df_y = read_csv(path_y,header=None,names = ["deltas","time1","time2"])
    df_theta = read_csv(path_theta,header= None,names = ["deltas","time1","time2"])



    interpx = interp1d(df_x["deltas"],df_x["time1"],kind="nearest")
    interpy = interp1d(df_y["deltas"],df_y["time1"],kind="nearest")
    interptheta = interp1d(df_theta["deltas"],df_theta["time1"],kind="nearest")

    s= linspace(0,300,1001)
    x_test = interpx(s)
    y_test = interpy(s)
    theta_test = interptheta(s)

    #plt.plot(s,x_test,label="time_x")
    #plt.plot(s,y_test,label="time_y")
    #plt.plot(s,theta_test,label="time_theta")
    #plt.legend()
    #plt.show()
    
    return interpx,interpy,interptheta



def calculate_tim_of_a_solution(sol,interpx,interpy,interptheta):
    """Calcualte the time associated with each movement for all axis and takes the longest one"""
    # 1 calculate the delta x, delta y and delta theta. Theta_i =0 donc theta = delta tetha
    #dico_sol[column_name_with_sol[i_sol]] = {"list_point": [],"ordre_tortue":[],"valid":False,"position_finale":piece_pos_finale,"number_point":0}
    
    list_point_with_0  =[ array([0,0,0])]
    list_point_with_0.extend(sol["list_point"])
    ###
    matrix_point = vstack(list_point_with_0)

    x= matrix_point[:,0]
    y= matrix_point[:,1]
    
    delta_x_abso = abs(diff(x))
    delta_y_abso = abs(diff(y))
    delta_theta_abso = abs(matrix_point[1:,2])

    time_x = interpx(delta_x_abso)
    time_y = interpy(delta_y_abso)
    time_theta = interptheta(delta_theta_abso)

    matrix_time = stack([time_x,time_y,time_theta],axis=1)
    
    max_time = amax(matrix_time,axis=1)
    arg_max = argmax(matrix_time,axis=1)
    
    sol["max_time"] = max_time
    sol["time_array"] = matrix_time
    sol["arg_max"] = arg_max

    total_time_pick_and_place =delta_x_abso.shape[0]/2 *time_pick_place # Nbr piece picked *temps associé
    
    sol["max_time"] = max_time
    sol["time_array"] = matrix_time
    sol["arg_max"] = arg_max
    sol["total_time"]= sum(max_time)/1000 + total_time_pick_and_place
    sol["time_pick_and_place"]= total_time_pick_and_place

    if delta_x_abso.shape[0] == 12:
        sol["type"] = "inplace"
    else:
        sol["type"] = "notinplace"
    
    return sol # With max time vector and the matrix of time of each axis. 
    

def calculate_time_all_solution(dico_sol_valid_path,general_path):
    # 1 generate all the interpolate function 
    interpx,interpy,interptheta = create_interpolation_function(general_path)
    

    #2 generate calculate thte time for each solution
    
    for sol_name, sol in dico_sol_valid_path.items():
        
        if sol["valid"] == True:
            sol_with_time = calculate_tim_of_a_solution(sol,interpx,interpy,interptheta)
            dico_sol_valid_path[sol_name] = sol_with_time
            
        else:
            sol["max_time"] = None
            sol["time_array"] = None
            sol["arg_max"] = None
            sol["total_time"]= None
            sol["time_pick_and_place"]= None
    
    return dico_sol_valid_path

