from create_constants import *
from constants import *
import os
import shutil





def run_simulation(DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,src_dst,speed, num_mes, num_chan, num_puser):

    dir = "DataMules/"              #Starting Directory
    num_messages = num_mes
    debug_message = -1
    is_queuing_active = True
    restrict_band_access = True
    restrict_channel_access = True
    generate_new_primary_users = False

    generate_messages = True if pkl_fold_num == 1 else False

    dataset = DataSet               #UMass or Lexington
    day_or_numMules = Day_Or_NumMules#date (UMass) or number of mules (Lexington)
    round = Round                       #Round number (Always 1 for UMass)
    protocol = Protocol             #Protocol in set of [XChant, Epidemic, SprayNWait, HotPotato]
    band = Band                    #bands to use in set of [ALL, TV, LTE, ISM, CBRS]
    generate_link_exists = Gen_LE
    T = t                         #Length of Simulation
    V = v                          #Number of dataMules
    NoOfSources = src_dst[0]
    NoOfDataCenters = src_dst[1]
    start_time = ts
    max_nodes = Max_Nodes                  #All nodes include src and des


    if dataset == "UMass":
        dataMule_path = dir + dataset + "/" + day_or_numMules + "/" + str(round) + "/"
        link_exists_path = dataMule_path + "Link_Exists/" + "LE_" + str(start_time) + "_" + str(T) + "/"
        metrics_path = link_exists_path + protocol + "/" + band + "/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser) + "/"
        path_to_save_LLC = link_exists_path + protocol + "/" + band + "/mules_" + str(V) + "/"
        if pkl_fold_num == 1:
            path_to_day1_LLC = link_exists_path + protocol + "/" + band + "/mules_" + str(V) + "/"
        else:
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_" + str(start_time - T) + "_" + str(T) + "/" + protocol + "/" + band + "/mules_" + str(V) + "/"

    elif dataset == "Lexington":
        dataMule_path = dir + dataset + "/" + day_or_numMules + "/" + str(round) + "/"
        if pkl_fold_num == 1:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_1_"  + str(T) + "/"
            metrics_path = link_exists_path + protocol + "/" + band + "/" + str(V) + "/"
            path_to_day1_LLC = metrics_path
        else:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_2_" + str(T) + "/"
            metrics_path = link_exists_path + protocol + "/" + band + "/" + str(V) + "/"
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_1_" + str(
                T) + "/" + protocol + "/" + band + "/" + str(V) + "/"  + str(num_chan) + "/" + str(num_puser) + "/"

    else:
        print("Invalid Dataset")
        return -1

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


    create_constants(T, V, S, start_time, dataset, max_nodes, dataMule_path, metrics_path, link_exists_path, debug_message, protocol, NoOfDataCenters, NoOfSources,generate_link_exists,generate_messages, num_messages, pkl_fold_num, path_to_day1_LLC, perfect_knowledge, speed, is_queuing_active, restrict_band_access, restrict_channel_access, generate_new_primary_users, num_chan, num_puser, path_to_save_LLC)

    if generate_new_primary_users == True:
        os.system("python3 generate_primary_users.py")

    if generate_link_exists == True and max_nodes == V + NoOfSources + NoOfDataCenters:

        if dataset == "UMass":
            os.system("python3 create_pickles.py")
            os.system("python3 computeLINKEXISTS_UMass.py")

        elif dataset == "Lexington":
            os.system("python3 readLexingtonData_Fixed.py")
            os.system("python3 create_pickles_Lex.py")
            os.system("python3 computeLINKEXISTS_Lex.py")

    if protocol == "XChant":
        if not os.path.exists(path_to_metrics):
            os.makedirs(path_to_metrics)

        if num_mes == 25 and num_chan == 10 and num_puser== 100:
            os.system("python3 STB_main_path.py")

    # #
    # if generate_messages == True and pkl_fold_num == 1 and V + NoOfDataCenters + NoOfSources == Max_Nodes:
    #     os.system("python3 generateMessage_new.py")



    # if pkl_fold_num == 2:
    #
    os.system("python3 main.py")
    os.system("python3 metrics.py")


# (DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge, src_dst_arr, speed_arr, num messages, num channels, num primary users)
#Day 1
# run_simulation("UMass", "2007-11-06", 1, "XChant", "ALL", 180, 660, 10, False, 19, 1, False, [6,3], [0,0],200, 10, 100)
# Day 2
# run_simulation("UMass", "2007-11-06", 1, "XChant", "ALL", 180, 840, 10, False, 19, 2, False, [6,3], [0,0], 200, 10, 100)













#RUN ALL UMASS SIMULATIONS

dataset = "UMass"
# # days = ["2007-11-01", "2007-11-06", "2007-11-07"]
days = ["2007-11-06"]
round = 1
protocols = ["XChant"]

# print("Bootstrap Round\n")
# for day in days:
#     # for v in range(10,-1,-1):
#     v = 10
#     run_simulation(dataset, day, round, "XChant", "ALL", 180, 660, v, False, 19, 1, False, [6,3], [0,0], 200, 10, 20)
#     run_simulation(dataset, day, round, "XChant", "ALL", 180, 840, v, False, 19, 2, False, [6, 3], [0, 0], 200, 10, 20)
#
print("\nSTARTING SIMULATION\n")
for day in days:
    for num_mules in range(10,0,-1):
        for num_msg in [25, 50, 75, 100, 150, 200]:
            for num_chan in range(10, 1, -1):
                for num_pusers in range(100, 0, -20):

                    print("Day:", day, "| V:", num_mules, "| # msgs:", num_msg, "| # channels:", num_chan, "| # primary users:", num_pusers)
                    print("_____________________________________________________________________________")
                    print("Round 1\n")
                    run_simulation("UMass", day, 1, "XChant", "ALL", 180, 660, num_mules, False, 19, 1, False, [6,3], [0,0],num_msg, num_chan, num_pusers)
                    print("\nRound 2 \n")
                    run_simulation("UMass", day, 1, "XChant", "ALL", 180, 840, num_mules, False, 19, 2, False, [6,3], [0,0],num_msg, num_chan, num_pusers)
                    print("\n")



