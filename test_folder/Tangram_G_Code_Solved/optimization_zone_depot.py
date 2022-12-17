from turtle import position
from scipy.optimize import minimize
from scipy.optimize import NonlinearConstraint

from numpy import array, cos,sin,sum , dot,ones,absolute, multiply,pi ,less,greater,logical_and,argwhere,radians,transpose
from numpy.linalg import norm,inv
from numpy.random import rand

def fct_obj2(pos_repere,args):
    # 0 calcul la matrice de rotation 
    mat_pos_rel,position_absolue_initiale,hors_tout  = args[0],args[1],args[2]
    theta_rad = radians(pos_repere[2])
    matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])
        
    # 1 calcul la position de chaque piece
    position_finale = pos_repere+dot(mat_pos_rel,matrice_rotation)

    position_x_y = position_finale[:,:2]
    #print(position_x_y.shape)
    #print(position_absolue_initiale[:,:2].shape)
    erreur_pose = position_x_y-position_absolue_initiale[:,:2]
    distance = norm(erreur_pose,ord=2,axis=1)
    #print(test)

    indice_distance = sum(distance)**2
    # Criteria of angle 

    gain_erreur_angle = 0#100000000
    gain_zone_analysé = 3
    erreur_angle = critere_angulaire(position_absolue_initiale,pos_repere,hors_tout*gain_zone_analysé,mat_pos_rel,distance)
    
    
    #ratio_angle = indice_distance/(erreur_angle*gain_erreur_angle)
    #print(ratio_angle)
    #print(indice_distance)
    return indice_distance+erreur_angle*gain_erreur_angle


#res = minimize(fct_obj, x0=[200,200], method='COBYLA', tol=1e-6,constraints=nlc)
def calcul_pos_4_coins_rep_absolue(position_centre,hors_tout):
    #hors_tout[2] = 0
    half_x =hors_tout[0]/2
    half_y =hors_tout[1]/2
    #matrice_signe #print(matrice_signe)
    pos_rel = array([[half_x,half_y,0],[-half_x,half_y,0],[-half_x,-half_y,0],[half_x,-half_y,0]])
    

    # Calcule la position finale de chaque coin 
    theta_rad = radians(position_centre[2])
    matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])
        
    # 1 calcul la position de chaque pièce
    position_finale = position_centre+dot(pos_rel,matrice_rotation)

    return position_finale




con = lambda x: x[0]**2 + x[1]**2 

nlc = NonlinearConstraint(con, 0, 20)   


def calcul_pos_init_rep_rel(pos_repere,position_absolue_initiale):
    #1 trouver matrice rotation inverse 
    theta_rad = radians(pos_repere[2])
    matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])
    matrice_rotation_inverse = inv(matrice_rotation)
    pos_rel_init = dot(position_absolue_initiale-pos_repere,matrice_rotation_inverse)
    #print(pos_rel_init)

    return pos_rel_init
def critere_angulaire(position_initiale,position_centre,hors_tout,position_relative,distance):
    position_4_coin = calcul_pos_4_coins_rep_absolue(position_centre,hors_tout)
    pos_rel_piece_init = calcul_pos_init_rep_rel(position_centre,position_initiale)
    arg_piece_in = find_id_piece_in_sol(pos_rel_piece_init,hors_tout)

    
    # Calcul position_relative angle 
    
    angle_correction = pos_rel_piece_init[:,2]
    angular_greater_than_360 = less(angle_correction,0)
    correction = angular_greater_than_360.astype(int) * 360
    angle_correction = angle_correction + correction
    pos_rel_piece_init[:,2] = angle_correction

    
    # Technique dans le périmètre
    angular_error = absolute(pos_rel_piece_init[arg_piece_in,[2]]-position_relative[arg_piece_in,[2]])
    ponderation_of_each_error = 360/(angular_error+1)
    
    # Technique du poids en fonction de la distance au carré
    angular_error = absolute(pos_rel_piece_init[:,[2]]-position_relative[:,[2]])
    facteur_ponder = transpose(1/distance**5)
    angular_error = angular_error[0]
    angular_error = multiply(angular_error,facteur_ponder)
    ponderation_of_each_error = angular_error
    ## fin méthode 2
    
    sum_error= ponderation_of_each_error.sum()

    return sum_error
def find_id_piece_in_sol(pos_rel_piece_init,hors_tout):
    x_min = ones(pos_rel_piece_init.shape[0])*  -hors_tout[0]/2
    x_max = ones(pos_rel_piece_init.shape[0])* hors_tout[0]/2
    y_min = ones(pos_rel_piece_init.shape[0])* -hors_tout[1]/2
    y_max = ones(pos_rel_piece_init.shape[0])* hors_tout[1]/2

    x_plus_grand_min = greater(pos_rel_piece_init[:,0],x_min)
    x_plus_petit_max = greater(x_max,pos_rel_piece_init[:,0])
    x_in = logical_and(x_plus_grand_min,x_plus_petit_max)

    y_plus_grand_min = greater(pos_rel_piece_init[:,1],y_min)
    y_plus_petit_max = greater(y_max,pos_rel_piece_init[:,1])
    y_in = logical_and(y_plus_grand_min,y_plus_petit_max)
    
    piece_in = logical_and(x_in,y_in)
    arg_piecin = argwhere(piece_in)
    return arg_piecin


def constraint_fct(position_centre,hors_tout,limit_plateau):
    
    pos_4_coin = calcul_pos_4_coins_rep_absolue(position_centre,hors_tout)

    x_min = 0
    y_min = 0
    x_max = 460
    y_max = 340

    x_plus_petit_min = less(pos_4_coin[:,0],x_min)
    x_plus_grand_max = less(x_max,pos_4_coin[:,0])
    
    x_hors_norme_min = pos_4_coin[x_plus_petit_min,0] # déjà négatif donc on additionne
    x_hors_norme_max = x_max -pos_4_coin[x_plus_grand_max,0]
    erreur_x = x_hors_norme_min.sum()+x_hors_norme_max.sum()

    y_plus_petit_min = less(pos_4_coin[:,1],y_min)
    y_plus_grand_max = less(y_max,pos_4_coin[:,1])
    
    y_hors_norme_min = pos_4_coin[y_plus_petit_min,1] # déjà négatif donc on additionne
    y_hors_norme_max = y_max -pos_4_coin[y_plus_grand_max,1]
    erreur_y = y_hors_norme_min.sum()+y_hors_norme_max.sum()
    
    erreur_total = erreur_y+erreur_x
    #print(erreur_y)
    return erreur_total

def constraint_empillage(position_centre,hors_tout,limit_plateau):
    pass 

    #pos_4_coin[]

def optimize_the_position(xoyo,mat_pos_rel,position_absolue_initiale,hors_tout_sol):
    args_ = [mat_pos_rel,position_absolue_initiale,hors_tout_sol]
    #calcul_pos_4_coins_rep_absolue(xoyo,hors_tout_sol)
    #calcul_pos_init_rep_rel(xoyo,position_absolue_initiale)
    #critere_angulaire(position_absolue_initiale,xoyo,hors_tout_sol,mat_pos_rel)
    #res = minimize(fct_obj2, x0=xoyo,args=args_, method='Nelder-Mead', tol=1e-6)
    limit_plateau = array([460,340])
    xoyo = array([500,500,200])
    nlc = NonlinearConstraint(con, 0, 20)   
    nlc = {"type":"ineq","fun": constraint_fct,"args": [hors_tout_sol,limit_plateau]}
    res = minimize(fct_obj2, x0=xoyo,args=args_, method='COBYLA', tol=1e-6,constraints=nlc,options={"maxiter":100000})
    #print(res)
    #print(res)
    return res 


def generate_first_guess(width,height):
    #print(mat_pos_initial)
    scaler= 1#2 #-2
    limits = 20
    scaling_factor_x = width*scaler -2*limits
    scaling_factor_y = height*scaler -2*limits
    #2 First guess
    pos_repere_initial = rand(1,3)*array([scaling_factor_x,1,1])*array([1,scaling_factor_y,1])*array([1,1,360])
    pos_repere_initial=pos_repere_initial[0]
    return pos_repere_initial

def calculate_pos_final_each_piece(pos_centre,pos_rel):
    theta_rad = radians(pos_centre[2])
    matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])

    position_absolue = pos_centre+dot(pos_rel,matrice_rotation)

    return position_absolue