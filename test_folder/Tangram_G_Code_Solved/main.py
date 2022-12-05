import optimization_zone_depot as ozd
import gestion_affichage as ga
import generate_random_piece as grp
from numpy import array
from numpy.random import rand
import turtle as t
from os.path import isfile 
from os import remove 
from time import time,sleep

from pandas import DataFrame,read_csv
from os.path import join
import create_path as cp

from station_parameter import *
import test_py_constraint_all_piece as tpc
import calcul_all_possible_path as cal
import calcualte_path_time as cpt
import generates_bilan_save as gbs
def run():
    
    #1. Genere une matrice de position de chaque piece
    #print(res.x)
    start = time()

    path_st = r"C:\Users\Equipe1\Desktop\StationTriage\DocumentEquipe\BanqueVi\AllVi\Tangram_G_Code_Solved"
    path_test = r"C:\Users\nicsa\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\Tangram_G_Code_Solved"
    path_test = r"C:\Users\Proprio\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\Tangram_G_Code_Solved"
    
    # C:\Users\nicsa\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\Tangram_G_Code_Solved\main.py
    path_now = path_test
    #path_now = path_st
    grp.generate(1,path_now)
    #path_to_dataset = r"C:\Users\nicsa\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\data_set_test.csv"
    path_to_dataset =join(path_now,"log_file.csv")
    #path_to_dataset = r"C:\Users\nicsa\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\testExec2\log_file.csv"

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

    #sc = t.Screen()
    #ga.affiche_tout_graphiquement(width,height,mat_pos_initial,
    #dico_best_sol["position_finale"],path_now,dico_best_sol["list_point"],
    #            dico_best_sol["ordre_tortue"],sc=sc)
    #sc.exitonclick()
    #sc.mainloop()
    print("i have finish")

    #array_name = []
    #array_in_space = []
    #array_nb_point = []
    #for nom,value in dico_sol_valid_path.items():
    #    array_name.append(nom)
    #    array_in_space.append(value["valid"])
    #    array_nb_point.append(value["number_point"])
    #df_sol_valid = DataFrame({"name_of_solution":array_name,"Sol_validiti":array_in_space,"Nbr_points":array_nb_point})
    #print(df_sol_valid)

    #for key,value in dico_sol_valid_path.items():
    #    sc = t.Screen()
    #    if True:
    #
    #        
    #
    #        if value["valid"] == True:
    #            ga.affiche_tout_graphiquement(width,height,mat_pos_initial,
    #
    #            value["position_finale"],path_now,value["list_point"],
    #            value["ordre_tortue"],sc=sc)
    #        sleep(2)
    #        sc.clearscreen()

    #matrice_conflit = tpc.count_number_piece_overlap(mat_pos_initial,position_finale,solution_info[3])

    # 6 sauvegarde la solution 
    #list_final_point,ordre_pour_les_tortue = cp.calcule_path(mat_pos_initial,position_finale,path_to_save,matrice_conflit)
    #print("Sauvegarde terminée")
    # 7 Affiche la solution
    #ga.affiche_tout_graphiquement(width,height,mat_pos_initial,position_finale,path_now,list_final_point,ordre_pour_les_tortue)

for i in range(1000):
    run()

