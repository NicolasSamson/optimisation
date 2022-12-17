from numpy import array,argmin,argsort,sort,array_equal,around
from pandas import DataFrame,read_csv
from os.path import join
from numpy.linalg import norm

def trouve_piece_plus_proche(position_actuelle,position_pièce_qui_reste):
    
    calcule_distance = norm(position_pièce_qui_reste-position_actuelle)
    i_prochaine_piece = argmin(calcule_distance,ord=2,axis=1)
    return i_prochaine_piece


def calcule_path(matrice_position_initial,matrice_position_finale,path,matrice_conflit,to_save=True):

    i_max = matrice_position_initial.shape[0]

    position_actuelle = array([0,0,0])
    
    list_finale = []
    list_i_deja_ajoute = []
    piece_trouvee = False
    ordre_pour_les_tortue = []
    list_finale_offset = []
    piece_planned = 0
    #for i in range(i_max):
    i=0
    list_non_bougee = [0,1,2,3,4,5,6]
    list_piece_pas_bougee_avec_ii = [0,1,2,3,4,5,6]
    nbr_iteration_globale = 0
    order_validity = True
    while piece_planned <7 and order_validity==True:
        if i == i_max:
            i_max =0 
        # Calcule distance des pièces
        test= matrice_position_initial[:,0:2]
        calcule_distance = norm(matrice_position_initial[:,0:2]-position_actuelle[0:2],ord=2,axis=1)
        i_parse =0
        # Tant que l'on a pas trouvée la pièce la plus proche qui n'est pas 
        # déjà à la bonne position
        # Renvoie les indices dans le bon ordre de la piece la plus proche à la plus loin
        ordre_sorted = argsort(calcule_distance)
        test_sort = sort(calcule_distance)
        piece_trouvee = False
        for numero_piece in ordre_sorted:
            if numero_piece not in list_i_deja_ajoute and piece_trouvee==False:

                i_to_use = numero_piece

                # Vérifie si sa landing zone est chill 
                # Tout en enlevant le conflit avec la même pièce
                
                
                potentiel_conflit = matrice_conflit[i_to_use,:]
                potentiel_conflit= potentiel_conflit[list_non_bougee] 
                #potentiel_conflit = potentiel_conflit[]
                if sum(potentiel_conflit) == 0:
                    # S'il y a un conflit on passe al a prochiane
                
                    #print(test_sort)
                    # Vérifie si la pièce la plus proche n'a pas déjà été déplacé
                    
                        # Si la pièce n'est pas déjà placé on ajoute les deux coordonnées
                        # position initiale de la place et position finale
                        
                        # S'il y a pas de conflit avec les pièces pas bougées on prend ce choix
                        line_to_add =matrice_position_initial[i_to_use,:]
                        line_to_add_final = matrice_position_finale[i_to_use,:]
                        while line_to_add[2] >360:
                            line_to_add[2] = line_to_add[2] -360
                        while line_to_add_final[2] >360:
                            line_to_add_final[2] = line_to_add_final[2] -360
                        # Add the point to the list if the piece is mooved
                        if (array_equal(around(line_to_add_final,decimals=2),around(line_to_add,decimals=2)) == False):
                            list_finale.append(list(line_to_add))
                            list_finale.append(list(line_to_add_final))
                            # Actualise la position actuelle de la pièce avec la position finale de
                            # la pièce que l'on va aller chercher
                            position_actuelle = matrice_position_finale[i_to_use,:]
                            ordre_pour_les_tortue.append(i_to_use)
                            ordre_pour_les_tortue.append(i_to_use)
                        # Ajoute l'indice à la liste d'indice déjà placé.
                        list_i_deja_ajoute.append(i_to_use)
                        piece_trouvee =True
                        
                        list_non_bougee.remove(i_to_use)
                        piece_planned += 1
                        
                
            
        
        #piece_trouvee =False
        i+= 1
        nbr_iteration_globale += 1
        if nbr_iteration_globale>7: # 7 fois 
            order_validity = False
            print("et une autre solution mauvaise")
    
    
    
    if to_save ==True:
        df_final = DataFrame(list_finale)

        df_final.to_csv(path,sep=";",line_terminator=';\n',index=False,header=False)
        print("path_created_and_saved")
    return list_finale,ordre_pour_les_tortue,order_validity



