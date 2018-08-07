from create_constants import *
import os





def run_simulation(DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge):

    dir = "DataMules/"              #Starting Directory
    num_messages = 100
    debug_message = 2
    generate_messages = True

    dataset = DataSet               #UMass or Lexington
    day_or_numMules = Day_Or_NumMules#date (UMass) or number of mules (Lexington)
    round = Round                       #Round number (Always 1 for UMass)
    protocol = Protocol             #Protocol in set of [XChant, Epidemic, SprayNWait, HotPotato]
    band = Band                    #bands to use in set of [ALL, TV, LTE, ISM, CBRS]
    generate_link_exists = Gen_LE
    T = t                         #Length of Simulation
    V = v                          #Number of dataMules
    NoOfSources = 6
    NoOfDataCenters = 3
    start_time = ts
    max_nodes = Max_Nodes                  #All nodes include src and des

    dataMule_path = dir + dataset + "/" + day_or_numMules + "/" + str(round) + "/"
    link_exists_path = dataMule_path + "Link_Exists/" + "LE_" + str(start_time) + "_" + str(T) + "/"
    metrics_path = link_exists_path + protocol + "/" + band + "/" + str(V) + "/"
    if pkl_fold_num == 1:
        path_to_day1_LLC = metrics_path
    else:
        path_to_day1_LLC = dataMule_path + "Link_Exists/LE_" + str(start_time - T) + "_" + str(T) + "/" + protocol + "/" + band + "/" + str(V) + "/"

    if band == "ALL":
        S = [0, 1, 2, 3]  # Spectrums to use
    elif band == "TV":
        S = [0]
    elif band == "ISM":
        S = [1]
    elif band == "LTE":
        S = [2]
    elif band == "CBRS":
        S = [3]
    else:
        S = []
        print("Invalid Band Type")


    create_constants(T, V, S, start_time, dataset, max_nodes, dataMule_path, metrics_path, link_exists_path, debug_message, protocol, NoOfDataCenters, NoOfSources,generate_link_exists,generate_messages, num_messages, pkl_fold_num, path_to_day1_LLC, perfect_knowledge)

    print(protocol)

    if generate_link_exists == True:
        if dataset == "UMass":
            os.system("python3 create_pickles.py")
            os.system("python3 computeLINKEXISTS_UMass.py")
            os.system("python3 STB_main_path.py")

        elif dataset == "Lexington":
            os.system("python3 readLexingtonData_Fixed.py")
            os.system("python3 create_pickles")
            os.system("python3 computeLINKEXISTS_Lex.py")
            os.system("python3 STB_main_path.py")

    if generate_messages == True and pkl_fold_num == 1:
        os.system("python3 generateMessage_new.py")

    if pkl_fold_num == 2:
        os.system("python3 main.py")
        os.system("python3 metrics.py")


# (DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge)


# run_simulation("UMass", "2007-11-06", 1, "XChant", "ALL", 180, 660, 10, False, 19, 1, False)
# run_simulation("UMass", "2007-11-06", 1, "XChant", "ALL", 180, 840, 10, False, 19, 2, False)
# run_simulation("UMass", "2007-11-06", 1, "XChant", "ALL", 180, 840, 10, False, 19, 2, True)
run_simulation("UMass", "2007-11-06", 1, "Epidemic", "ALL", 180, 840, 10, False, 19, 2, False)
run_simulation("UMass", "2007-11-06", 1, "SprayNWait", "ALL", 180, 840, 10, False, 19, 2, False)
# run_simulation("UMass", "2007-11-06", 1, "HotPotato", "ALL", 180, 840, 10, False, 19, 2, False)



