from time import time,sleep
start_import = time()
from premain import run

finish_import = time()




print("time to import ",finish_import-start_import)

run(affichage_graphique=1,select_tangram=1,random_generation=1)


time_to_run = time()
print(time_to_run-finish_import)


