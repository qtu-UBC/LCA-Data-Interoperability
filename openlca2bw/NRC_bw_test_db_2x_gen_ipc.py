import openlca2bw as olca2bw
import brightway2 as bw

"""
===
Prepare for import
===
"""
# specifiy the openlca process folder to be imported
User_folder = {'NRC':'LIB recycling_NMC 811'} # this from "NRC_CNRC-Lithium_Battery_Recycling_Pathways_Public"

# 'selected_methods' argument is a list of methods names that will be extracted
# you can specify [] to import no method or 'all' to import all available methods
# the default value is 'all' 
# you can: print(bw.methods) to check available methods
selected_methods = ['ei -  ReCiPe Midpoint (H) V1.13'] # to save time, just import one method

"""
===
Load data to a new project or update an existing project
===
"""
# [caution] only need to run this once to create the brightway2 project. Make sure to open the 8080 port in openLCA client                    
olca2bw.load_openLCA_IPC(project_name="NRC_test_db_Sep_2023",
                        nonuser_db_name = 'EcoInvent', # <-case sensitive
                        user_databases=User_folder,
                        # excluded_folders=unused_folders,
                        selected_methods=selected_methods,
                        overwrite = True)

# OR, update only the foreground processes
olca2bw.update_openLCA_IPC(project_name="NRC_test_db_Sep_2023",
                        update_databases={'NRC':'LIB recycling_NMC 811'}
                        )

"""
===
Conduct LCA
===
"""
bw.projects.set_current("NRC_test_db_Sep_2023")
print({k: v['number'] for k, v in bw.databases.items()})

# check a random activity from the NRC database
rdm_act = bw.Database('NRC').random()
print(rdm_act)
print('\n')
# print its exchanges
for exc in rdm_act.exchanges():
    print(exc)

# check a random activity from the EcoInvent database 
ei_act = bw.Database('EcoInvent').random()
print(ei_act)
print('\n')
for exc in ei_act.exchanges():
    print(exc)

# check the LCIA score of the random activity from the NRC database
LCIA_method = ('ei -  ReCiPe Midpoint (H) V1.13', 'climate change - GWP100')
lca = bw.LCA({rdm_act: 1},method=LCIA_method)
lca.lci()
lca.lcia()
print('\n')
print(lca.score)