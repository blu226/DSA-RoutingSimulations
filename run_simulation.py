from create_constants import *
from constants import *
from misc_sim_funcs import *
import os

def run_simulation(DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,src_dst,speed, num_mes, num_chan, num_puser, smart_setting="optimistic"):

    dir = "DataMules/"              #Starting Directory
    num_messages = num_mes
    debug_message = -1
    is_queuing_active = True
    restrict_band_access = True
    restrict_channel_access = True
    priority_queue_active = True
    broadcast = True
    geo_routing = False
    num_nodes_to_fwd = 1
    generate_new_primary_users = False

    generate_messages = True if pkl_fold_num == 1 else False

    dataset = DataSet               #UMass or Lexington
    day_or_numMules = Day_Or_NumMules#date (UMass) or number of mules (Lexington)
    round = Round                       #Round number (Always 1 for UMass)
    if Protocol == "Epidemic_Smart":
        protocol = Protocol + "_" + smart_setting    #Protocol in set of [XChant, Epidemic, SprayNWait, HotPotato]
    else:
        protocol = Protocol

    if priority_queue_active == True:
        buffer = "PQ"
    else:
        buffer = "FIFO"
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
        metrics_path = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser) + "/"
        path_to_save_LLC = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/"
        if pkl_fold_num == 1:
            path_to_day1_LLC = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/"
        else:
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_" + str(start_time - T) + "_" + str(T) + "/" + protocol + "/" + buffer + "/mules_" + str(V) + "/"

    elif dataset == "Lexington":
        dataMule_path = dir + dataset + "/" + day_or_numMules + "/" + str(round) + "/"
        if pkl_fold_num == 1:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_1_"  + str(T) + "/"
            metrics_path = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser) + "/"
            path_to_day1_LLC = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/"
        else:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_2_" + str(T) + "/"
            metrics_path = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser) + "/"
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_2_" + str(
                T) + "/" + protocol + "/" + buffer + "/mules_" + str(V) +  "/"

        path_to_save_LLC = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/"


    else:
        print("Invalid Dataset")
        return -1

    if band == "ALL":
        S = get_suitable_spectrum_list(smart_setting)
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


    create_constants(T, V, S, start_time, dataset, max_nodes, dataMule_path, metrics_path, link_exists_path, debug_message, \
                     protocol, NoOfDataCenters, NoOfSources,generate_link_exists,generate_messages, num_messages, pkl_fold_num,\
                     path_to_day1_LLC, perfect_knowledge, speed, is_queuing_active, restrict_band_access, restrict_channel_access,\
                     generate_new_primary_users, num_chan, num_puser, path_to_save_LLC, smart_setting, priority_queue_active,\
                     broadcast, geo_routing, num_nodes_to_fwd)

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

        # if num_mes == 25 and num_chan == 10 and num_puser== 100:
    # os.system("python3 STB_main_path.py")

    # #
    # if generate_messages == True and pkl_fold_num == 1 and V + NoOfDataCenters + NoOfSources == Max_Nodes:
    # os.system("python3 generateMessage_new.py")

    os.system("python3 main.py")
    os.system("python3 metrics.py")


# (DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,
#  src_dst_arr, speed_arr, num messages, num channels, num primary users, smart setting (optional))

# Day 1
# print("\nOptimistic")
# run_simulation("UMass", "2007-11-06", 1, "Epidemic_Smart", "ALL", 180, 660, 10, False, 19, 1, False, [6,3], [0,0], 25, 10, 0, "optimistic")

# print("\nPessimistic")
# run_simulation("UMass", "2007-11-06", 1, "Epidemic_Smart", "ALL", 180, 660, 10, False, 19, 1, False, [6,3], [0,0], 50, 10, 0, "pessimistic")
# print("\nRandom")
# run_simulation("UMass", "2007-11-06", 1, "Epidemic_Smart", "ALL", 180, 660, 10, False, 19, 1, False, [6,3], [0,0], 50, 10, 0, "random")
#
# # Day 2

data = "Lexington"
day = "30"
len_T = 180                     #length of simulation
start_time = 0                #start time (to find Link Exists)
bands = "ALL"                   #which bands to use
num_mules = 30                  #number of data mules to use
generate_LE = False             #generate Link Exists
max_v = 42                      #max number of datamules + src + dst
pkl_ID = 2                      #pkl folder ID if Link Exists is being generated
perfect_knowledge = False       #Xchant only
src_dst = [6, 6]                #num src and dst
speed = [350, 700]                  #Lex data only
proto = "Epidemic_Smart"        #[Epidemic_Smart, XChant, SprayNWait (in progress)]
num_messages = 50
num_Pusers = 0
num_channels = 10

# for num_channels in range(10, 1, -2):
#     for num_Pusers in range(0, 125, 25):
#         for num_messages in range(25, 175, 25):

print("-----------------------------------------------------------------------")
print("Channels:", num_channels, "\tPrimary Users:", num_Pusers, "\tMessages:", num_messages)
print("-----------------------------------------------------------------------")

print("\nOptimistic")
run_simulation(data, day, 1, proto, bands, len_T, start_time, num_mules, generate_LE, max_v,
               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
               "optimistic")

print("\nPessimistic")
run_simulation(data, day, 1, "Epidemic_Smart", bands, len_T, start_time, num_mules, generate_LE, max_v,
               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
               "pessimistic")

print("\nWeighted")
run_simulation(data, day, 1, "Epidemic_Smart", bands, len_T, start_time, num_mules, generate_LE, max_v,
               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
               "random")



# data = "UMass"
# day = "2007-11-06"
# len_T = 180                     #length of simulation
# start_time = 840                #start time (to find Link Exists)
# bands = "ALL"                   #which bands to use
# num_mules = 10                  #number of data mules to use
# generate_LE = False             #generate Link Exists
# max_v = 19                      #max number of datamules + src + dst
# pkl_ID = 2                      #pkl folder ID if Link Exists is being generated
# perfect_knowledge = False       #Xchant only
# src_dst = [6, 3]                #num src and dst
# speed = [350, 700]                  #Lex data only
# proto = "Epidemic_Smart"        #[Epidemic_Smart, XChant, SprayNWait (in progress)]
# num_messages = 15
# num_Pusers = 0
# num_channels = 10
#
# # for num_channels in range(10, 1, -2):
# #     for num_Pusers in range(0, 125, 25):
# #         for num_messages in range(25, 175, 25):
#
# print("-----------------------------------------------------------------------")
# print("Channels:", num_channels, "\tPrimary Users:", num_Pusers, "\tMessages:", num_messages)
# print("-----------------------------------------------------------------------")
#
# print("\nOptimistic")
# run_simulation(data, day, 1, proto, bands, len_T, start_time, num_mules, generate_LE, max_v,
#                pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
#                "optimistic")
#
# print("\nPessimistic")
# run_simulation(data, day, 1, "Epidemic_Smart", bands, len_T, start_time, num_mules, generate_LE, max_v,
#                pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
#                "pessimistic")
#
# print("\nWeighted")
# run_simulation(data, day, 1, "Epidemic_Smart", bands, len_T, start_time, num_mules, generate_LE, max_v,
#                pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
#                "random")
