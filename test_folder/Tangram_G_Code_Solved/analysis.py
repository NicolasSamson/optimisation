import pandas as pd 
import numpy as np
#df =pd.read_csv(r"C:\Users\nicsa\OneDrive - Université Laval\École\A 2022\Investigation\optimisation_2\test_folder\Tangram_G_Code_Solved\result_time\result_time_500_photo.csv")
df = pd.read_csv(r"C:\Users\Proprio\OneDrive - Université Laval\École\A 2022\Investigation\optimisation_2\test_folder\Tangram_G_Code_Solved\result_time\result_time_500_photo_3.csv")

# extrait les 500 première lignes
df= df.loc[df.indice_simulation <500]

# 1 extrait le meilleur temps de chaque simulation 
df_best_time = df.loc[df.ranking==0]
print(df_best_time.type.value_counts())

# 2 génère dataframe avec les valeurs de temps de la meilleur solution des deux types
df__best_time_deux_methodes = df.drop_duplicates(subset=["indice_simulation","type"],keep="first")

df__not_inpalce = df__best_time_deux_methodes.loc[df__best_time_deux_methodes.type=="notinplace"]
indice_simul_not_in_place = list(df__not_inpalce.indice_simulation.values)

df__inplace = df__best_time_deux_methodes.loc[df__best_time_deux_methodes.type=="inplace"]
indice_simul_in_place = list(df__inplace.indice_simulation.values)
print(df__not_inpalce)

print(df__best_time_deux_methodes.loc[df__best_time_deux_methodes.indice_simulation==0])

print("ratio de solution trouvée sur pas trouvée inplace",len(indice_simul_in_place)/500)
print("ratio de solution trouvée sur pas trouvée not inplace",len(indice_simul_not_in_place)/500,len(indice_simul_not_in_place))
list_diff_temp = []
list_temp_inplace = []
list_temp_not_inpalce = []

list_nbr_sol_val_in_place = []
for i in range(500):
    
    if i not in indice_simul_not_in_place or i not in indice_simul_in_place:
        df_i = df__best_time_deux_methodes.loc[df__best_time_deux_methodes.indice_simulation == i]
        #print(df_i)
        continue
    df_i = df__best_time_deux_methodes.loc[df__best_time_deux_methodes.indice_simulation == i]
    #print(df_i)
    df_inplace = df_i.loc[df_i.type=="inplace"]
    #print(df_inplace.total_time.values)
    list_temp_inplace.append(df_inplace.total_time.values[0])
    df_not_inplace = df_i.loc[df_i.type=="notinplace"]
    #print(df_not_inplace)
    
    list_temp_not_inpalce.append(df_not_inplace.total_time.values[0])

    # Extract inplace value
    df_i_pas_best = df.loc[df.indice_simulation == i]
    nbr_sol_val = df_i_pas_best.loc[df_i_pas_best.type=="inplace"]
    nbr_sol_val = nbr_sol_val.shape[0]
    #print(nbr_sol_val)
    list_nbr_sol_val_in_place.append(nbr_sol_val)
    #list_diff_temp.append(df_inplace.total_time-df_not_inplace.total_time)
#list_temp_inplace = np.array(list_temp_inplace)
#list_temp_not_inpalce = np.array(list_temp_not_inpalce)
# 3. Calcul toutes les solutions in place différentes
# df_not_inplace 
array_nbr_sol_val_inplace = np.array(list_nbr_sol_val_in_place)
df_nbr_detection = pd.DataFrame.from_dict({"nbr_inpalce":array_nbr_sol_val_inplace})

print(df_nbr_detection.describe())
df_result = pd.DataFrame.from_dict({"best_time_inplace":list_temp_inplace,"best_time_not_implace":list_temp_not_inpalce})

df_result.to_csv(r"C:\Users\Proprio\OneDrive - Université Laval\École\A 2022\Investigation\optimisation_2\test_folder\Tangram_G_Code_Solved\result_time\result_time_500_best_sol_2_hypothesis.csv")
#print(df["total_time"].describe())
df_result.drop(df_result[df_result['best_time_inplace'] == 20.013].index, inplace = True)

df_result["erreur_moins_not"] = df_result.best_time_inplace - df_result.best_time_not_implace
##grouped = df.groupby(by="type")
print(df_result.describe())
#print(grouped["total_time"].describe())

print("\n"*8)
#print(df[df["nbr_sol_valid"] ==0])

print(23*np.sqrt(2)/2)

print(8.125 /np.cos(np.radians(45)))

print(2/3*32.5*np.sin(np.radians(45)))
print(0.8/5.4)
