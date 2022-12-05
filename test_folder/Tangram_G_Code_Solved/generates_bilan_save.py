import copy 
from pandas import DataFrame, read_csv,concat

from numpy import amax, argmax, stack,diff, hstack,linspace,array_equal,identity,array, cos,sin,sum , dot,ones,absolute, multiply,pi ,less,greater,logical_and,argwhere,radians,transpose,ones,vstack,where
from numpy.linalg import norm,inv
from numpy.random import rand
from scipy.interpolate import interp1d

import test_py_constraint_all_piece as tcp
import optimization_zone_depot as ozd
import create_path as cp
from os.path import join,isfile
from os import listdir

import matplotlib.pyplot as plt


def generates_the_bilan_of_the_solution(dico_solution_with_time,general_path):


    key_best_time = ""
    value_best_time = 100000

    list_valid_name_solution = []
    list_time = []
    list_sol_type = []
    

    nbr_valid_solution = 0
    nbr_invalid_solution = 0

    for sol_name, sol in dico_solution_with_time.items():
        
        if sol["valid"] == True:
            nbr_valid_solution += 1
            list_valid_name_solution.append(sol_name)
            
            list_time.append(sol["total_time"])
            list_sol_type.append(sol["type"])
            # Verify if it is a better solution 
            if value_best_time > sol["total_time"]:
                key_best_time = sol_name
                value_best_time = sol["total_time"]

            
        else:
            nbr_invalid_solution += 1
    

    path_to_folder_time = join(general_path,r"result_time")
    

    nbr_result = len(listdir(path_to_folder_time))

    # Generates the resultat with the time_and_ranking
    
    
    path_to_save_folder_time = join(path_to_folder_time,f"result_time.csv")
    
    if isfile(path_to_save_folder_time):
        current_df = read_csv(path_to_save_folder_time,index_col=0)
        indice_simul = current_df["indice_simulation"].max()+1
    else:
        indice_simul = 0
    
    size = len(list_time)
    col_indice_simulation = [indice_simul]*size
    ratio_sol = [round(nbr_valid_solution/(nbr_valid_solution+nbr_invalid_solution)*100)]*size
    nbr_sol_valid_col = [nbr_valid_solution]*size
    nbr_sol_invalid = [nbr_invalid_solution] * size
    data_frame = DataFrame({"indice_simulation":col_indice_simulation, 
    "name_solution":list_valid_name_solution,"type":list_sol_type, "total_time": list_time,
    "nbr_sol_valid":nbr_sol_valid_col,"nbr_sol_invalid":nbr_sol_invalid,
    "ratio_valid_solution_pourc":ratio_sol})

    data_frame.sort_values(by="total_time",inplace=True,ignore_index=True)
    data_frame["ranking"] = array(data_frame.index)

    # Concat if 
    if isfile(path_to_save_folder_time): 
        result_dataframe = concat((current_df,data_frame),ignore_index=True)
    else:
        result_dataframe = data_frame

    result_dataframe.to_csv(path_to_save_folder_time)

    # Generates the result with the number of viable solution 
    #path_ratio_sol_to_save = join(join(general_path,r"resultat_ratio_sol_viable"),"nbr_valid_sol.csv")
    #df_bilan_result = DataFrame({"indice_simulation":[indice_simul],
    #]})
    #df_bilan_result.to_csv(path_ratio_sol_to_save)

    # Return the best solution 
    return dico_solution_with_time[key_best_time]

