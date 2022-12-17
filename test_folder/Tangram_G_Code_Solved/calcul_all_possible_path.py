""" Calcule l'ensemble des trajectoires et le temps associées pour la parcourir.

"""

import copy 
from pandas import DataFrame

from numpy import array_equal,identity,array, cos,sin,sum , dot,ones,absolute, multiply,pi ,less,greater,logical_and,argwhere,radians,transpose,ones,vstack,where
from numpy.linalg import norm,inv
from numpy.random import rand

import test_py_constraint_all_piece as tcp
import optimization_zone_depot as ozd
import create_path as cp

#import matplotlib.pyplot as plt
def pos_finale_sur_piece(i_piece,mat_pos_initial,pos_rel_sol):
    """ Calculate the final position of each piece according to the initial position of a specific piece."""
    pos_piece_abso = mat_pos_initial[i_piece,:]
    theta_c = pos_piece_abso[2]-  pos_rel_sol[i_piece,2]



    ## Calculate the position of the center of the solution
    theta_rad = radians(theta_c)
    matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])

    resultat_matrice = dot(pos_rel_sol[i_piece,:],matrice_rotation)
    pos_centre_sol_abso = pos_piece_abso- resultat_matrice
    
    pos_piece_abso = pos_centre_sol_abso+resultat_matrice

    #while pos_centre_sol_abso[2] < 0:
    #    pos_centre_sol_abso[2] += 360
    
    #while pos_centre_sol_abso[2] > 360:
    #    pos_centre_sol_abso[2] -= 360
    ## Calculate the final position of ecah pieces.
    
    final_position_abso = pos_centre_sol_abso + dot(pos_rel_sol,matrice_rotation)

    #final_position_abso = tcp.calculate_pos_final_each_piece(pos_centre_sol_abso,pos_rel_sol)

    
    pos_piece_final = final_position_abso[i_piece,:]
    pos_piece_initi = mat_pos_initial[i_piece,:]
    erreur = sum(pos_piece_final[0:2]-pos_piece_initi[0:2])
    if erreur <1:
            #print("yeahhh")
            test=2
    else:
        raise ValueError("Erreur dans la rotation")
    
    return final_position_abso,pos_centre_sol_abso

def validate_the_vision_limit(position_finale,mat_pos_initial,width,height):
    """ Verify that the solution is in the vision space of the table"""

    # calcule les points des sommets des positions absolues de la solution finale
    list_sommet_position_absolue,list_sommet_chaque_form_rel,list_longueur =tcp.calculate_the_absolute_coordinate_of_each_point_of_each_figure(position_finale)
    nbr_piece = mat_pos_initial.shape[0]

    outOfZone = True
    # Contrairement à l'autre algo, on a juste besoin de faire une forme géométrique soit le plateau
    # Pas besoin de changer de repère à un repère relatif
    list_piece_in_final_piece = []
    for i in range(nbr_piece):
            pos_coins_absolue = list_sommet_position_absolue[i]
            
            #plt.plot(pos_coins_absolue[:,0],pos_coins_absolue[:,1])
            piece_in_piece,piece_in = tcp.contrainte_(pos_coins_absolue,3,width,height)
            #print(piece_in_piece)

            ref_true = array([True]*pos_coins_absolue.shape[0])
            true_array = 123
            if array_equal(ref_true,piece_in):
                list_piece_in_final_piece.append(0)
            else:
                list_piece_in_final_piece.append(1)
    # Si toutes les pièces sont dans le rectangel
    #plt.show()
    if sum(list_piece_in_final_piece) ==0:
        outOfZone = False

    return outOfZone



def calculate_final_position_of_in_place_solution(mat_pos_initial,pos_rel_sol,width,height,column_name):
    """Generates all the solution if we assume that we let one piece in place"""
    # Ajoute)les_solutions_des_4_cotées du carré verts
    matrice_green2 = copy.deepcopy(mat_pos_initial) 
    
    matrice_green2[4,2] += 90

    matrice_green3 =  copy.deepcopy(mat_pos_initial) 
    matrice_green3[4,2] += 180

    matrice_green4 =  copy.deepcopy(mat_pos_initial) 
    matrice_green4[4,2] += 270

    # Ajoute deuxième solution parallellograme
    matrice_para = copy.deepcopy(mat_pos_initial) 
    matrice_para[5,2] += 180
    
    
    # Liste matrice position initiale
    list_mat_pos_ini = [mat_pos_initial,mat_pos_initial,mat_pos_initial,mat_pos_initial,mat_pos_initial,
    mat_pos_initial,mat_pos_initial,matrice_green2,matrice_green3,matrice_green4,matrice_para]

    column_name_with_sol = copy.deepcopy(column_name[0:7]) 
    column_name_with_sol.extend(["square_green_2","square_green_3","square_green_4","para_180"])

    nbr_solution = len(list_mat_pos_ini)
    nbr_piece = nbr_solution
    
    dico_sol ={}
    
    list_i_piece = [0,1,2,3,4,5,6,4,4,4,5]

    for i_sol in range(nbr_solution):
        # Si on analyse solution supp, i_piece=square
        i_piece = list_i_piece[i_sol]
        
        # Extrait la matrice de position_initiale de cette piece
        mat_pos_initial = list_mat_pos_ini[i_piece]

        # 1. calculate the final position of 
        piece_pos_finale,pos_centre_sol_abso = pos_finale_sur_piece(i_piece,mat_pos_initial,pos_rel_sol)

        # 2. Vérifie que la solution est bien dans la zone
        outOfZone = validate_the_vision_limit(piece_pos_finale,mat_pos_initial,width,height)

        
        

        if outOfZone == False:
            # The solution is Valid, let's continue
            # 3 Validate that all the pieces are in the zone to solve.
            ovelap_matrice = tcp.count_number_piece_overlap(mat_pos_initial,piece_pos_finale,column_name)
            valid_solution = True

            #4 Generate the path
            uselesss_path = r""
            list_finale,ordre_pour_les_tortue,order_validity = cp.calcule_path(mat_pos_initial,piece_pos_finale,uselesss_path,ovelap_matrice,to_save=False)

            if order_validity==True:
                dico_sol[column_name_with_sol[i_sol]] = {"list_point": list_finale,"ordre_tortue":ordre_pour_les_tortue,"valid":True,"position_finale":piece_pos_finale,"number_point":len(ordre_pour_les_tortue)}
            else: 
                dico_sol[column_name_with_sol[i_sol]] = {"list_point": [],"ordre_tortue":[],"valid":False,"position_finale":piece_pos_finale,"number_point":0}

        else:
            dico_sol[column_name_with_sol[i_sol]] = {"list_point": [],"ordre_tortue":[],"valid":False,"position_finale":piece_pos_finale,"number_point":0}

    return dico_sol
def generate_10_sol_with_minimized_distance(width,height,position_rel_solution,mat_pos_initial,solution_info_height_width,column_name,dico_G_code_solution):
    # 1 Calculate the solution with the minimal distance travel
        

    for i in range(10):
        # 1.1 génère repère initial
        pos_repere_initial = ozd.generate_first_guess(width,height)

        # 1.2 calculate the optimal position de centre.
        opti_centre = ozd.optimize_the_position(pos_repere_initial,position_rel_solution,mat_pos_initial,array(solution_info_height_width))
        # 1.3 calculate the final position of each piece 
        position_finale = ozd.calculate_pos_final_each_piece(opti_centre.x,position_rel_solution)

        matrice_conflit = tcp.count_number_piece_overlap(mat_pos_initial,position_finale,column_name)

        # 1.4 Génère la trajectoire
        useless_path = ""
        list_final_point,ordre_pour_les_tortue,order_validity = cp.calcule_path(mat_pos_initial,position_finale,useless_path,matrice_conflit,to_save=False)
        #1.5 Add to the posssible solution
        dico_G_code_solution[f"Opti_zone_depot_{i}"] = {"list_point": list_final_point,"ordre_tortue":ordre_pour_les_tortue,"valid":True,"position_finale":position_finale,"number_point":len(ordre_pour_les_tortue)}
    return dico_G_code_solution
def generate_all_the_tested_solution(mat_pos_initial,position_rel_solution,solution_info_height_width,width,height,column_name):
    """Generates the path _associate to each valid solution : 1. Solution ou distance minimisé. 2. Solution ou on laisse une palce à la même place."""
    # 0 Génère les solutions in place (une pièce reste à la même place) 
    # Prochainement ajouté l'option de l'enlever
    dico_G_code_solution = calculate_final_position_of_in_place_solution(mat_pos_initial,position_rel_solution,width,height,column_name)
    



    dico_G_code_solution = generate_10_sol_with_minimized_distance(width,height,position_rel_solution,mat_pos_initial,solution_info_height_width,column_name,dico_G_code_solution)
    
    # 
    
    
    return dico_G_code_solution


