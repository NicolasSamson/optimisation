from numpy import identity,array, cos,sin,sum , dot,ones,absolute, multiply,pi ,less,greater,logical_and,argwhere,radians,transpose,ones,vstack,where
from numpy.random import rand
from numpy.linalg import norm
from pandas import DataFrame
from os.path import isfile,join
from test_py_constraint_all_piece import count_number_piece_overlap
from os import remove 
import copy
def generate(tangram_sol,path_folder):
    scaler= 1#2 #-2
    limits = 20
    scaling_factor_x = 460*scaler -2*limits
    scaling_factor_y = 340*scaler -2*limits
    scaling_factor_theta = 360*scaler -2*limits
    math_scaling = array([[scaling_factor_x,0,0],[0,scaling_factor_y,0],[0,0,scaling_factor_theta]])
    math_offset = array([[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0]])
    math_offset = array([1,1,0])
    math_offset_y = math_offset *limits
    #1. Génère une matrice de position de chaque pièce
    i_piece= 0
    safe_radius = 35
    colonne_name = ["triangle_rouge","triangle_rose","triangle_jaune","triangle_orange","square_green","para_blue","tri_purple","w_et_H_hors_tout"]
    
    while i_piece <1:
        
            mat_pos_initial = rand(7,3)
            mat_pos_initial = dot(mat_pos_initial,math_scaling)
            
            mat_pos_initial += math_offset_y
            nbr_overlap = count_number_piece_overlap(mat_pos_initial,mat_pos_initial,colonne_name)
            print(sum(nbr_overlap))
            
            if sum(nbr_overlap)  ==0:    # 
                
                i_piece += 1

            else: print("lol")

    
    """
    while i_piece <7:
        if i_piece == 0:
            mat_pos_initial = rand(1,3)
            mat_pos_initial = dot(mat_pos_initial,math_scaling)
            mat_pos_initial += math_offset_y
            i_piece += 1
        else:


            potentiel_piece = rand(1,3)
            potentiel_piece = dot(potentiel_piece,math_scaling)
            potentiel_piece += math_offset_y

            
            

            distance = norm(mat_pos_initial[:,0:2] - potentiel_piece[:,0:2],ord=2,axis=1)
            
            nbr_dist_petit_radius = greater(distance,safe_radius)
            nbr_pris = argwhere(nbr_dist_petit_radius==False)
            if len(nbr_pris)  ==0:    # 
                mat_pos_initial = vstack((mat_pos_initial,potentiel_piece))
                i_piece += 1
    """
    
    choice = array([tangram_sol,0,0])
    mat_pos_initial = vstack((choice,mat_pos_initial))

    path_file = join(path_folder,r"log_file.csv")
    if isfile(path_file):
        remove(path_file)
    df = DataFrame(mat_pos_initial)
    df.to_csv(path_file,sep=";",line_terminator=';\n',index=False,header=False)
    
    print("generation terminated")
#generate(1)
