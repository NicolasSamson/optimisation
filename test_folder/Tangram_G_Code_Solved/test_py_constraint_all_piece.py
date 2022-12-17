#from signal import valid_signals
from pandas import DataFrame

from numpy import identity,array, cos,sin,sum , dot,ones,absolute, multiply,pi ,less,greater,logical_and,argwhere,radians,transpose,ones,vstack,where
from numpy.linalg import norm,inv
from numpy.random import rand


#import matplotlib.pyplot as plt

def craete_array_point_between_2_points(c1,c2,n):
    delta_x_y = (c2-c1)/n
    
    line = array([[delta_x_y[0]*i,delta_x_y[1]*i,0] for i in range(n+1)])
    line += c1 
    return line
def generate_triangle(n,longueur):
    
    
    c1 = array([2*longueur/3,-longueur/3,0])
    c2 = array([-longueur/3,-longueur/3,0])
    c3 = array([-longueur/3,2*longueur/3,0])
    first_set = craete_array_point_between_2_points(c1,c2,n)
    second_set = craete_array_point_between_2_points(c2,c3,n)
    third_set = craete_array_point_between_2_points(c1,c3,n)
    last_set = array([0,0,0])
    triangle = vstack((first_set,second_set,third_set,last_set))

    #plt.scatter(triangle[:,0],triangle[:,1])
    #plt.show()
    return triangle

def generate_rectangle(n,longueur,longueur2):
    
    
    c1 = array([longueur/2,longueur2/2,0])
    c2 = array([longueur/2,-longueur2/2,0])
    c3 = array([-longueur/2,-longueur2/2,0])
    c4 = array([-longueur/2,longueur2/2,0])
    first_set = craete_array_point_between_2_points(c1,c2,n)
    second_set = craete_array_point_between_2_points(c2,c3,n)
    third_set = craete_array_point_between_2_points(c3,c4,n)
    fourth = craete_array_point_between_2_points(c4,c1,n)
    last_set = array([0,0,0])
    triangle = vstack((first_set,second_set,third_set,fourth,last_set))
    #print("test")
    #plt.scatter(triangle[:,0],triangle[:,1])
    #plt.show()
    return triangle


def generate_para(n,longueur):
    largeur_sin45 = longueur*sin(radians(45))
    largeur_sin45_2 = largeur_sin45/2
    

    c1 = array((-largeur_sin45_2,-largeur_sin45_2,0))
    c2 = array((-(largeur_sin45_2+largeur_sin45),largeur_sin45_2,0))
    c3 = array((largeur_sin45_2,largeur_sin45_2,0))
    c4 = array(((largeur_sin45_2+largeur_sin45),-largeur_sin45_2,0))
    first_set = craete_array_point_between_2_points(c1,c2,n)
    second_set = craete_array_point_between_2_points(c2,c3,n)
    third_set = craete_array_point_between_2_points(c3,c4,n)
    fourth = craete_array_point_between_2_points(c4,c1,n)
    last_set = array([0,0,0])
    triangle = vstack((first_set,second_set,third_set,fourth,last_set))
    #triangle[:,2] = ones(triangle.shape[0])*(-45)
    #plt.scatter(triangle[:,0],triangle[:,1])
    #plt.axis('equal')
    #plt.show()
    return triangle
def relative_coordinate_of_each_point():
    n=100
    
    l_tri_big = 46
    bigTriangle = generate_triangle(n,l_tri_big)


    l_tri_small = 23
    smallTriangle = generate_triangle(n,l_tri_small)

    l_tri_mauve = 33
    medTriangle= generate_triangle(n,l_tri_mauve)#array(((2*l_tri_mauve/3,-l_tri_mauve/3,0),(-l_tri_mauve/3,2*l_tri_mauve/3,0),(-l_tri_mauve/3,-l_tri_mauve/3,0)))



    l_square = 23
    
    square= generate_rectangle(n,l_square,l_square)#array(((-l_square/2,-l_square/2,0),(l_square/2,-l_square/2,0),(l_square/2,l_square/2,0),(-l_square/2,l_square/2,0)))
    
    para= generate_para(n,l_tri_small)#array(((-l_tri_small/2,0,0),(-l_tri_small/2,l_tri_small,0),(l_tri_small/2,0,0),(l_tri_small/2,-l_tri_small,0)))
    
    #para = array(((-l_tri_small/2,0,0),(-l_tri_small/2,l_tri_small,0),(l_tri_small/2,0,0),(l_tri_small/2,-l_tri_small,0)))
    #plt.scatter(para[:,0],para[:,1])
    #plt.show()
    list_point_form = [bigTriangle,bigTriangle,smallTriangle,
    smallTriangle,square,para,medTriangle]
    #print(list_point_form)

    list_longueur = [l_tri_big,l_tri_big,l_tri_small,l_tri_small,l_square,l_tri_small,l_tri_mauve]
    return list_point_form,list_longueur

def contrainte_(points,type,longueur,longueur2=False):
    
    
    if type==0: # triangle 
        x_min = -1/3 *longueur
        x_max = 2/3 * longueur
        m = (-1/3 -2/3)/(2/3-(-1/3))  # = -1 hahahaha
        b = (2/3 - m*(-1/3)) * longueur
        y_max = m* points[:,0] + b
        y_min = ones(points.shape[0]) * -1/3* longueur


    if type==1: #carré
        x_min = -0.5*longueur
        x_max = 0.5 * longueur
        y_max = ones(points.shape[0]) * 1/2* longueur
        y_min = ones(points.shape[0]) * -1/2* longueur

    #if type ==2: # //
    if type==2: #//
        # Première partie 
        
        x_min = -0.5*longueur
        x_max = 0 * longueur
        m = (0 -1)/(1/2-(-1/2))  # = -1 hahahaha
        b1 = (1 - m*(-1/2)) * longueur
        b2= -b1
        y_max = m* points[:,0] + b1
        y_min = m* points[:,0] + b2

    if type==3 and longueur2!=False: #Rectangle
        x_min = 0
        x_max = longueur
        y_max = longueur2
        y_min = 0
    
    # 
    x_plus_grand_min = greater(points[:,0],x_min)
    x_plus_petit_max = greater(x_max,points[:,0])
    x_in = logical_and(x_plus_grand_min,x_plus_petit_max)

    y_plus_grand_min = greater(points[:,1],y_min)
    y_plus_petit_max = greater(y_max,points[:,1])
    y_in = logical_and(y_plus_grand_min,y_plus_petit_max)
    
    piece_in = logical_and(x_in,y_in)
    arg_piecin = argwhere(piece_in)
    
    return arg_piecin,piece_in


def contrainte_para(points,type,longueur):
    largeur_sin45 = longueur*sin(radians(45))
    largeur_sin45_2 = largeur_sin45/2
    

    c1 = array((-largeur_sin45_2,-largeur_sin45_2,0))
    c2 = array((-(largeur_sin45_2+largeur_sin45),largeur_sin45_2,0))
    c3 = array((largeur_sin45_2,largeur_sin45_2,0))
    c4 = array(((largeur_sin45_2+largeur_sin45),-largeur_sin45_2,0))

    nbr_piece_in = 0

    # Domaine 1
    x_min = c2[0]
    x_max = c1[0]
    m = (c1[1]-c2[1])/(c1[0]-c2[0])  # = -1 hahahaha
    b = c1[1] - m *c1[0]

    y_min = m* points[:,0] + b
    y_max = ones(points.shape[0]) * largeur_sin45_2

    x_plus_grand_min = greater(points[:,0],x_min)
    x_plus_petit_max = greater(x_max,points[:,0])
    x_in = logical_and(x_plus_grand_min,x_plus_petit_max)

    y_plus_grand_min = greater(points[:,1],y_min)
    y_plus_petit_max = greater(y_max,points[:,1])
    y_in = logical_and(y_plus_grand_min,y_plus_petit_max)
    
    piece_in = logical_and(x_in,y_in)
    arg_piecin = argwhere(piece_in)
    if len(arg_piecin) != 0:
        nbr_piece_in += len(arg_piecin)
    #finall_array = vstack(finall_array,arg_piecin)
    # Domaine 2
    x_min = c1[0]
    x_max = c3[0]
    y_max = c3[1]
    y_min = c1[1]

    x_plus_grand_min = greater(points[:,0],x_min)
    x_plus_petit_max = greater(x_max,points[:,0])
    x_in = logical_and(x_plus_grand_min,x_plus_petit_max)

    y_plus_grand_min = greater(points[:,1],y_min)
    y_plus_petit_max = greater(y_max,points[:,1])
    y_in = logical_and(y_plus_grand_min,y_plus_petit_max)
    
    piece_in = logical_and(x_in,y_in)
    arg_piecin = argwhere(piece_in)

    #finall_array = vstack(finall_array,arg_piecin)
    if len(arg_piecin) != 0:
        nbr_piece_in += len(arg_piecin)
    # Domaine 3
    x_min = c3[0]
    x_max = c4[0]
    m = (c4[1]-c3[1])/(c4[0]-c3[0])  # = -1 hahahaha
    b = c3[1] - m *c3[0]

    y_max = m* points[:,0] + b
    y_min = -ones(points.shape[0]) * largeur_sin45_2

    x_plus_grand_min = greater(points[:,0],x_min)
    x_plus_petit_max = greater(x_max,points[:,0])
    x_in = logical_and(x_plus_grand_min,x_plus_petit_max)

    y_plus_grand_min = greater(points[:,1],y_min)
    y_plus_petit_max = greater(y_max,points[:,1])
    y_in = logical_and(y_plus_grand_min,y_plus_petit_max)
    
    piece_in = logical_and(x_in,y_in)
    arg_piecin = argwhere(piece_in)
    #finall_array = vstack(finall_array,arg_piecin)
    if len(arg_piecin) != 0:
        nbr_piece_in += len(arg_piecin)

    test = array([10]*nbr_piece_in)

    
    if nbr_piece_in == 0:
        final = array([])
    else:
        final = array([0]*nbr_piece_in)

    return final
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################


def calculate_pos_final_each_piece(pos_centre,pos_rel):
    theta_rad = radians(pos_centre[2])
    matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])

    position_absolue = pos_centre+dot(pos_rel,matrice_rotation)

    return position_absolue

def calcul_pos_init_rep_rel(pos_repere,position_absolue_initiale):
    """ Projete dans ue repère relatif
    """
    #1 trouver matrice rotation inverse 
    theta_rad = radians(pos_repere[2])
    matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])
    matrice_rotation_inverse = inv(matrice_rotation)
    pos_rel_init = dot(position_absolue_initiale-pos_repere,matrice_rotation_inverse)
    #print(pos_rel_init)

    return pos_rel_init

##################################

##################################

##################################

##################################

##################################

##################################

##################################

def calculate_the_absolute_coordinate_of_each_point_of_each_figure(matrice_position_initiale):
    list_sommet_chaque_form_rel,list_longueur = relative_coordinate_of_each_point()

    list_sommet_position_absolue = []
    for i in range(matrice_position_initiale.shape[0]):
        position_centre_piece = matrice_position_initiale[i,:]

        coin_ = list_sommet_chaque_form_rel[i]

        coin_absolue = calculate_pos_final_each_piece(position_centre_piece,coin_)
        #plt.plot(coin_absolue[:,0],coin_absolue[:,1])
        list_sommet_position_absolue.append(coin_absolue)
    #plt.show()
    return list_sommet_position_absolue,list_sommet_chaque_form_rel,list_longueur

def count_number_piece_overlap(matrice_position_initiale,matrice_position_finale,column_name):

    list_sommet_position_absolue,list_sommet_chaque_form_rel,list_longueur =calculate_the_absolute_coordinate_of_each_point_of_each_figure(matrice_position_initiale)

    nbr_piece = matrice_position_initiale.shape[0]
    list_type = [0,0,0,0,1,2,0]
    list_non_bougee = array([0,1,2,3,4,5,6])
    bilan_interaction = []

    
    for i_ in range(nbr_piece):
        piece_pos_finale = matrice_position_finale[i_]

        # 1 Extrait le vecteur de position absolu jusqu'à la piece 
        longueur_pour_contrainte = list_longueur[i_]
        type_ = list_type[i_]
        list_piece_in_final_piece = [column_name[i_]]
        #if i_ ==5:
        #    piece_pos_finale[2] += -45
        for i in range(nbr_piece):
            # Extrait la position des points de la pièce que l'on vérifie 
            pos_coins_absolue = list_sommet_position_absolue[i]
            # Calcule la position des pièces initiales p/r à la position finale d'une piece. 
            pos_coin_repere_rel = calcul_pos_init_rep_rel(piece_pos_finale,pos_coins_absolue)

            # test
            #piece_final_rel = calcul_pos_init_rep_rel(piece_pos_finale,matrice_position_finale)
            #piece_final_repere_rel = piece_final_rel[i_]
            #piece_final_repere_rel = list_sommet_chaque_form_rel[i_]+piece_final_repere_rel
            #plt.scatter(piece_final_repere_rel[:,0],piece_final_repere_rel[:,1])
            #plt.scatter(pos_coin_repere_rel[:,0],pos_coin_repere_rel[:,1])

            if type_ ==2:
                piece_in_piece = contrainte_para(pos_coin_repere_rel,type_,longueur_pour_contrainte)
            else:
                piece_in_piece,piece_in = contrainte_(pos_coin_repere_rel,type_,longueur_pour_contrainte)
            #print(piece_in_piece)
            
            if len(piece_in_piece) == 0:
                list_piece_in_final_piece.append(0)
            else:
                list_piece_in_final_piece.append(1)
            
            
            test = 1
            #plt.scatter(matrice_position_initiale[:,0],matrice_position_initiale[:,1])
            #plt.scatter(pos_coins_absolue[:,0],pos_coins_absolue[:,1])
        #plt.show()
        if i_ ==0:
            array_final = array(list_piece_in_final_piece[1:])

        else:
            array_final = vstack((array_final,array(list_piece_in_final_piece[1:])))
        bilan_interaction.append(list_piece_in_final_piece)
    
    final_name = ["name_of_the_final_piece"]
    final_name.extend(column_name[:-1])
    df_test = DataFrame.from_records(bilan_interaction,columns=final_name)
    #print(df_test)
    
    test =1
    #print(array_final)
    diago = identity(7)
    matrice_1 = ones((7,7))*-1
    matrice_2 = (diago+ matrice_1)*(-1)
    array_final = matrice_2 *array_final
    #print(array_final)
    return array_final