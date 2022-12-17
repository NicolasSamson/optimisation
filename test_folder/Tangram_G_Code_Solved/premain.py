from time import time,sleep
start_import = time()

import optimization_zone_depot as ozd
import gestion_affichage as ga
import generate_random_piece as grp
from numpy import array
from numpy.random import rand
import turtle as t
from os.path import isfile 
from os import remove 


from pandas import DataFrame,read_csv
from os.path import join,dirname,realpath
import create_path as cp

from station_parameter import *
import test_py_constraint_all_piece as tpc
import calcul_all_possible_path as cal
import calcualte_path_time as cpt
import generates_bilan_save as gbs


def run(path_to_the_Tangram_G_Code_Solved_folder=dirname(realpath(__file__)),
    affichage_graphique=0,random_generation=0,select_tangram=None):
    """
    path_to_the_Tangram_G_Code_Solved_folder := The path to the current file. Normally it find itself. 
    affichage_graphique [0,1] := 1 for affichage ||| 0 pour pas afficher.
    random_generation [0,1] := 1 pour générer aélatoirement les positions initiales des pièces. 0 pour aps le faire.
    select_tangram [1,2,3] := pour choisir une des trois solutions. 
    """
    #1. Genere une matrice de position de chaque piece
    #print(res.x)
    start = time()

    
    # C:\Users\nicsa\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\Tangram_G_Code_Solved\main.py
    path_now = path_to_the_Tangram_G_Code_Solved_folder
    #path_now = path_st
    if random_generation==1:
        grp.generate(1,path_now)

    
    
    #path_to_dataset = r"C:\Users\nicsa\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\data_set_test.csv"
    path_to_dataset =join(path_now,"log_file.csv")
    #path_to_dataset = r"C:\Users\nicsa\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\testExec2\log_file.csv"
    if select_tangram !=None:
        df_input = read_csv(path_to_dataset,sep=";",header=None)
        # Extract the number associated to a soluion
        df_input.iloc[0][0] = select_tangram
        df_input.to_csv(path_to_dataset,sep=";",header=None,index=False)

    path_to_save = join(path_now,"log_file_opti.csv")

    path_offset_affichage = join(path_now,r"path_offset_affichage.csv")


    # 1. Extract information 
    final_dict = read_input_file(path_to_dataset,path_now)
    mat_pos_initial = final_dict["initial_pos"]
    # 2. Info solution
    solution_info = final_dict["solution"]
    
    # 3 génère repère initial
    #pos_repere_initial = ozd.generate_first_guess(width,height)

    # 4 calculate the optimal position de centre.
    #opti_centre = ozd.optimize_the_position(pos_repere_initial,tangram_solution.pos_rel,mat_pos_initial,tangram_solution.hors_tout)
    #opti_centre = ozd.optimize_the_position(pos_repere_initial,solution_info[2],mat_pos_initial,array(solution_info[0:2]))

    # 5 calculate the final position of each piece 
    #position_finale = ozd.calculate_pos_final_each_piece(opti_centre.x,solution_info[2])
    
    print("Calcul terminé")
    test = time()-start
    #print(f"Time : {test}")

    # 3 Génère toutes les paths possible 
    solution_width_and_height = array(solution_info[0:2])
    pos_rel_solut = solution_info[2]
    column_name = solution_info[3]
    dico_sol_valid_path = cal.generate_all_the_tested_solution(mat_pos_initial,pos_rel_solut,solution_width_and_height,width,height,column_name)
    
    dico_sol_with_time = cpt.calculate_time_all_solution(dico_sol_valid_path,path_now)


    dico_best_sol= gbs.generates_the_bilan_of_the_solution(dico_sol_with_time,path_now)

    # Save the final solution 
    list_point = dico_best_sol["list_point"]
    if len(list_point)!=14:
        list_point.append([9999,0,0])
        list_point.append([9999,0,0])

    df_final = DataFrame(list_point)

    df_final.to_csv(path_to_save,sep=";",line_terminator=';\n',index=False,header=False)
    #print("path_created_and_saved")
    if affichage_graphique == 1:
        sc = t.Screen()
        ga.affiche_tout_graphiquement(width,height,mat_pos_initial,
        dico_best_sol["position_finale"],path_now,dico_best_sol["list_point"],
                dico_best_sol["ordre_tortue"],sc=sc)
        sc.exitonclick()
        sc.mainloop()

#path_st = r"C:\Users\Equipe1\Desktop\StationTriage\DocumentEquipe\BanqueVi\AllVi\Tangram_G_Code_Solved"
  

