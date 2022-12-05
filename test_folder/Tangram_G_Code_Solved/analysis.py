import pandas as pd 

df =pd.read_csv(r"C:\Users\Proprio\OneDrive - Université Laval\École\A 2022\Investigation\optimisation\test_folder\Tangram_G_Code_Solved\result_time\result_time.csv")

print(df["total_time"].describe())

grouped = df.groupby(by="type")

print(grouped["total_time"].describe())