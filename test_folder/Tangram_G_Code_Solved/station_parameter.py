width = 460 
height= 340
from pandas import DataFrame,read_csv
from os.path import join

def read_input_file(path_from_labview,path_to_relative):
    """_summary_

    Args:
        path_from_labview (_type_): Path_to_the_csv_produced_by_labview
        path_to_relative (_type_): Path_to_the_relative_folder_containing_the_exec Tangram_G_Code_Solved.

    Raises:
        ValueError: Error in the solution number

    Returns:
        dict: Containning :  [initial_position,[W,H,pos_rel,name]]
    """


    df_input = read_csv(path_from_labview,sep=";",header=None)

    # Extract the number associated to a soluion
    numero_tangram = int(df_input.iloc[0][0])

    if numero_tangram == 1:
        path_to_sol = join(path_to_relative,r"solution\walkman.csv")
    elif numero_tangram == 2: 
        path_to_sol = join(path_to_relative,r"solution\consdensed_from_csv.csv")
    elif numero_tangram ==3:
        path_to_sol = join(path_to_relative, r"solution\hollow_arrow.csv")
    else:
        raise ValueError("FUCK FUCK FUCK le numéro de solution a fuck up [1,2,3]")

    # Read the solution file 
    df_solution = read_csv(path_to_sol,sep=";")
    #print(df_solution)
    # Extract the rel position of the solution
    pos_relative_piece = df_solution.iloc[0:-1,1:4].to_numpy()

    # Extract the W et H
    last_row = df_solution.iloc[df_solution.shape[0]-1]
    Witdh_of_the_solution = last_row.x 
    Height_of_the_solution = last_row.y

    # Extract the order of the solution 
    piece_order_name = list(df_solution.name)

    
    
    # Extract the initial position of each pieces.     
    position_intial = df_input.iloc[1:,:3].to_numpy()
    
    # Pack the results
    final_dict = {"initial_pos": position_intial,
    "solution":[Witdh_of_the_solution,Height_of_the_solution,pos_relative_piece,piece_order_name]}

    #print(Witdh_of_the_solution)
    #print(Height_of_the_solution)
    #print(pos_relative_piece)
    #print(piece_order_name)

    #print("________________________\n"*2)
    #print(position_intial)
    
    return final_dict
    


def test_unitaire():

    path_from_labview = r"C:\Users\Proprio\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\Tangram_G_Code_Solved\log_file.csv"

    path_to_relative = r"C:\Users\Proprio\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\Tangram_G_Code_Solved"

    read_input_file(path_from_labview,path_to_relative)
#test_unitaire()