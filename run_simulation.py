from create_constants import *
from constants import *
from misc_sim_funcs import *
import os

def run_simulation(DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,src_dst,speed, num_mes, num_chan, num_puser, smart_setting, num_fwd, msg_round, puser_round):

    dir = "DataMules/"              #Starting Directory
    num_messages = num_mes
    debug_message = -1
    debug_mode = -1
    metric_interval = 30
    is_queuing_active = True
    restrict_band_access = True
    restrict_channel_access = True
    priority_queue_active = True
    if num_fwd == 0:
        broadcast = True
        geo_routing = False
    else:
        broadcast = False
        geo_routing = True
    num_nodes_to_fwd = num_fwd
    generate_new_primary_users = False

    generate_messages = True if pkl_fold_num == 1 else False
    fwd_strat = "broadcast" if broadcast == True else "geo_" + str(num_nodes_to_fwd)

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
        metrics_path = link_exists_path + protocol + "/" + buffer + "/" + fwd_strat +"/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser) + "/"
        path_to_save_LLC = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/"
        if pkl_fold_num == 1:
            path_to_day1_LLC = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/"
        else:
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_" + str(start_time - T) + "_" + str(T) + "/" + protocol + "/" + buffer + "/mules_" + str(V) + "/"

    elif dataset == "Lexington":
        dataMule_path = dir + dataset + "/" + day_or_numMules + "/" + str(round) + "/"
        if pkl_fold_num == 1:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_1_"  + str(T) + "/"
            metrics_path = link_exists_path + protocol + "/" + buffer + "/" + fwd_strat + "/mules_" + str(
                V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser) + "/"
            path_to_day1_LLC = link_exists_path
        else:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_2_" + str(T) + "/"
            metrics_path = link_exists_path + protocol + "/" + buffer + "/" + fwd_strat + "/mules_" + str(
                V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser) + "/"
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_2_" + str(
                T) + "/" + protocol + "/" + buffer + "/mules_" + str(V) +  "/"

        path_to_save_LLC = link_exists_path


    else:
        print("Invalid Dataset")
        return -1

    if band == "ALL":
        S = get_suitable_spectrum_list(smart_setting)
    elif band == "TV":
        S = [0, 0, 0, 0]
    elif band == "ISM":
        S = [1, 1, 1, 1]
    elif band == "LTE":
        S = [2, 2, 2, 2]
    elif band == "CBRS":
        S = [3, 3, 3, 3]
    else:
        S = []
        print("Invalid Band Type")


    create_constants(T, V, S, start_time, dataset, max_nodes, dataMule_path, metrics_path, link_exists_path, debug_message, \
                     protocol, NoOfDataCenters, NoOfSources,generate_link_exists,generate_messages, num_messages, pkl_fold_num,\
                     path_to_day1_LLC, perfect_knowledge, speed, is_queuing_active, restrict_band_access, restrict_channel_access,\
                     generate_new_primary_users, num_chan, num_puser, path_to_save_LLC, smart_setting, priority_queue_active,\
                     broadcast, geo_routing, num_nodes_to_fwd, msg_round, puser_round, debug_mode, metric_interval)

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

    if generate_LE == True:
        os.system("python3 STB_main_path.py")

    #
    # if generate_messages == True and pkl_fold_num == 1 and V + NoOfDataCenters + NoOfSources == Max_Nodes:
    # os.system("python3 generateMessage_new.py")

    if generate_LE == False:
        os.system("python3 main.py")
        os.system("python3 metrics.py")


# (DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,
#  src_dst_arr, speed_arr, num messages, num channels, num primary users, smart setting (optional))

data = "Lexington"
day = "50"
len_T = 360                     #length of simulation
start_time = 0                #start time (to find Link Exists)
bands = ["ALL", "LTE", "TV", "CBRS", "ISM"]  #which bands to use
num_mules = 30                  #number of data mules to use
generate_LE = False             #generate Link Exists
pkl_ID = 1                      #pkl folder ID if Link Exists is being generated
perfect_knowledge = False       #Xchant only
src_dst = [6, 6]                #num src and dst
max_v = num_mules + src_dst[0] + src_dst[1]                     #max number of datamules + src + dst
speed = [350, 600]                  #Lex data only
proto = "Epidemic_Smart"        #[Epidemic_Smart, XChant, SprayNWait (in progress)]
num_messages = 206
num_Pusers = 250
num_channels = 5
# nodes_tofwd = 0
# msg_round = 0
puser_round = 0

if generate_LE == False:
    for msg_round in range(10, 50):
        print("MSG File:", msg_round)
        for band in bands:

            print("Band:", band)

            if band == "ALL":
                for nodes_tofwd in [0, 3]:
                    run_simulation(data, day, 1, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                                   pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                                   "optimistic", nodes_tofwd, msg_round, puser_round)

                    run_simulation(data, day, 1, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                                   pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                                   "pessimistic", nodes_tofwd, msg_round, puser_round)

            else:
                nodes_tofwd = 3
                run_simulation(data, day, 1, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                                   pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                                   band, nodes_tofwd, msg_round, puser_round)




#Generate Link exists
else:
    run_simulation(data, day, 1, proto, "ALL", len_T, start_time, num_mules, generate_LE, max_v,
                                   pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                                   "optimistic", nodes_tofwd, msg_round, puser_round)