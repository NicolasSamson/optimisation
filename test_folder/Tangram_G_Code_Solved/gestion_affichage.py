from os.path import join
import turtle as t

from numpy import array,pi,sin,cos,radians,dot
from pandas import DataFrame, read_csv
class tangram_tortue:
    def __init__(self,tortue_info_rose,sc,width,height,pos_relative=array([0,0,0])):




        l_tri_big = 46
        bigTriangle = ((2*l_tri_big/3,-l_tri_big/3),(-l_tri_big/3,-l_tri_big/3),(-l_tri_big/3,2*l_tri_big/3))
        l_tri_small = 23
        smallTriangle= ((-l_tri_small/3,2*l_tri_small/3),(2*l_tri_small/3,-l_tri_small/3),(-l_tri_small/3,-l_tri_small/3))
        l_square = 23
        l_tri_mauve = 33
        medTriangle= ((2*l_tri_mauve/3,-l_tri_mauve/3),(-l_tri_mauve/3,2*l_tri_mauve/3),(-l_tri_mauve/3,-l_tri_mauve/3))
        
        square= ((-l_square/2,-l_square/2),(l_square/2,-l_square/2),(l_square/2,l_square/2),(-l_square/2,l_square/2))
        para= ((-l_tri_small/2,0),(-l_tri_small/2,l_tri_small),(l_tri_small/2,0),(l_tri_small/2,-l_tri_small))
        
        
        black_shape= ((-height/2,-width/2),(height/2,-width/2),(height/2,width/2),(-height/2,width/2))
    
        shape = 0
        if tortue_info_rose["shape"] == "bigTriangle":
            shape = bigTriangle
        elif tortue_info_rose["shape"] == "smallTriangle":
            shape = smallTriangle
        elif tortue_info_rose["shape"] == "square":
            shape = square
        elif tortue_info_rose["shape"] == "para":
            shape = para
        elif tortue_info_rose["shape"] == "medTriangle":
            shape = medTriangle
        elif tortue_info_rose["shape"] == "blac_plateau":
            shape = black_shape
        else:
            raise ValueError("MDR tes tortue ont une forme étrange")

        t.register_shape(tortue_info_rose["name"],shape)

        tortue = t.RawTurtle(sc)
        tortue.shape(tortue_info_rose["name"])
        tortue.color(tortue_info_rose["colour"])
        tortue.speed(speed="fastest")
        tortue.hideturtle()
        self.tortue = tortue
        self.pos_rel = pos_relative
def stamp_totue(tortue,position):
    tortue.settiltangle(position[2])
    tortue.up()
    tortue.setpos(position[0:2])
    tortue.stamp()

class tangram_solution:
    def __init__(self,list_tortue,pos_centre,hors_tout):

        list_position = []
        for tortue in list_tortue:
            list_position.append(tortue.pos_rel)

        #print(list_position)
        self.pos_rel = array(list_position)

        pos_centre[2] = pos_centre[2]
        self.pos_centre = pos_centre
        self.list_tortue = list_tortue
        theta_rad = radians(pos_centre[2])
        self.matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])
        self.hors_tout = hors_tout
    def set_position_centre(self,position_centre):
        self.pos_centre = position_centre
        theta_rad = radians(position_centre[2])
        self.matrice_rotation = array([[cos(theta_rad),sin(theta_rad),0],
        [cos(theta_rad+pi/2),sin(theta_rad+pi/2),0],
        [0,0,1]])
    def calculate_abso_pos_chaque_piece(self):
        self.position_finale = self.pos_centre+dot(self.pos_rel,self.matrice_rotation)
        #print(self.pos_centre)
        #print(self.pos_rel)
        #print(self.matrice_rotation)
        #print(self.position_finale)
        return self.position_finale 
    def plot_solution(self,offset,array_offset):
        self.calculate_abso_pos_chaque_piece()

        for i in range(self.position_finale.shape[0]):
            pos_i = self.position_finale[i,:]+offset +array_offset[i,:]
            tortue = self.list_tortue[i].tortue
            stamp_totue(tortue,pos_i)
    
    def offset_angle(self,array_offset):
        
        for i in range(self.position_finale.shape[0]):
            pos_i = self.position_finale[i,:]
            tortue = self.list_tortue[i].tortue
            stamp_totue(tortue,pos_i)
    def plot_pos_initiale(self,matrix_position,offset):
        
        for i in range(len(self.list_tortue)):
            tortue = self.list_tortue[i].tortue
            pos_i = matrix_position[i,:]+offset
            stamp_totue(tortue,pos_i)
        
def init_tortue(tortue_info_rose,sc):
        t.register_shape(tortue_info_rose["name"],tortue_info_rose["shape"])

        tortue = t.RawTurtle(sc)
        tortue.shape(tortue_info_rose["name"])
        tortue.color(tortue_info_rose["colour"])
        tortue.speed(speed="fastest")
        tortue.hideturtle()

        
        return tortue


#########################################################
#########################################################
#########################################################
#########################################################
#########################################################
#########################################################

#########################################################
#########################################################
#########################################################
#########################################################
#########################################################
#########################################################

#########################################################
#########################################################
#########################################################
#########################################################
#########################################################
#########################################################
""""
def create_offset_afficahge_x_y():
    path_offset = join(path_to_folder_Tangram_G_Code_Solved,r"path_offset_affichage.csv")
    df_offset = read_csv(path_offset,index_col=0)
    df_offset["x"] = df_offset["x"] -width/2
    df_offset["y"] = df_offset["y"] -height/2
    df_offset.to_csv(path_offset)
"""
def plot_pos_initiale(list_tortue,matrix_position,offset):
        pos_affichage = matrix_position +offset
        for i in range(len(list_tortue)):
            tortue = list_tortue[i].tortue
            pos_i = pos_affichage[i,:]
            stamp_totue(tortue,pos_i)

def print_background(width,height,sc):
    triangle_black_name = "blac_plateau"
    theta_black_jaune = 0 #90
    color_tri_black= "black"
    pos_relative_black = [0,0,0]

    info_fond_noir = {"shape":"blac_plateau",
    "name":triangle_black_name,
    "colour":color_tri_black,
    "pos_rel":pos_relative_black}   
    # Print the background   tortue_info_rose,sc,pos_relative=array([0,0,0]))
    black_fond = tangram_tortue(info_fond_noir,sc,width,height,pos_relative=pos_relative_black)
    stamp_totue(black_fond.tortue,black_fond.pos_rel)
def generate_all_turtle(path_to_folder_Tangram_G_Code_Solved,sc,width,height):
    
    path_to_turtle_info = join(path_to_folder_Tangram_G_Code_Solved,r"turtle_info.csv")

    df_turtle_info = read_csv(path_to_turtle_info,sep=";") 
    #print(df_turtle_info)
    list_turtle = []
    for i in range(df_turtle_info.shape[0]):
        tortue = tangram_tortue(df_turtle_info.iloc[i],sc,width,height)
        list_turtle.append(tortue)

    return list_turtle

    
    
def montre_trajectoire(sc,list_final_point,array_offset,list_turtle,list_turtle_ordonne):
    
    tortue = t.RawTurtle(sc)
    tortue.pencolor("white")

    tortue.shape("turtle")
    tortue.color("white")
    tortue.speed(speed="slowest")
    tortue.pensize(2)
    list_position = list_final_point
    
    # Mettre la tortue à la position 0,0
    tortue.up()
    tortue.setpos(array([0,0])+array_offset[0,0:2])
    tortue.down()
    tortue.stamp()
    # Lance la trajcetoire
    i=0
    for position in list_position:
        tortue_print = list_turtle_ordonne[i].tortue

        tortue_print.settiltangle(position[2])
        tortue_print.setpos(position[0:2])
        

        tortue.settiltangle(position[2])
        tortue.setpos(position[0:2])
        tortue_print.stamp()
        #tortue.stamp()
        
        
        t.delay(10)
        
        i+=1


def affiche_tout_graphiquement(width,height,position_initiale,position_finale,path_to_folder_Tangram_G_Code_Solved,list_final_point,ordre_pour_les_tortue,sc=False):

    if sc == False:

        sc_test = t.Screen()
    else:
        sc_test = sc
    # Generates all the turtle
    list_turtle = generate_all_turtle(path_to_folder_Tangram_G_Code_Solved,sc_test,width,height)
    
    
    # load the offset for printing the pieces in the correct orrientation
    path_offset = join(path_to_folder_Tangram_G_Code_Solved,r"path_offset_affichage.csv")
    df_offset = read_csv(path_offset,index_col=0)
    array_offset = df_offset.to_numpy()
    # Generate the correct order of turtle
    list_turtle_ordonne = []
    list_position_offset = []
    for i in range(len(list_final_point)):
        if list_final_point[i][0]==9999:
            continue
        else:
            list_turtle_ordonne.append(list_turtle[ordre_pour_les_tortue[i]])
            offset = array_offset[ordre_pour_les_tortue[i]]
            point = list_final_point[i]
            list_position_offset.append(point+offset)
    # Print the background
    print_background(width,height,sc_test)

    # TEST generate a position 
    

    # Print the initiale position 
    plot_pos_initiale(list_turtle,position_initiale,array_offset)

    # TEST position_finale 
    
    #plot_pos_initiale(list_turtle,position_finale,array_offset)

    
    montre_trajectoire(sc_test,list_position_offset,array_offset,list_turtle,list_turtle_ordonne)
    #sc_test.mainloop()
    
    


