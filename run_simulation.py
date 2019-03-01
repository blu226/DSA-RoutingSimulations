from create_constants import *
from constants import *
from misc_sim_funcs import *
import os

def run_simulation(DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,src_dst,speed, num_mes, num_chan, num_puser, smart_setting, num_fwd, msg_round, puser_round, msg_mean, ttl, max_mem, replicas, priority_queue_active):

    # a bunch of variables for the constant file
    dir = "DataMules/"              #Starting Directory
    num_messages = num_mes          # not needed anymore
    debug_message = -1              # if a certain msg # needs to be debugged put it here and include if statement in area to debug
    debug_mode = -1                 # same as above but for more general debug purposes
    metric_interval = 30            # interval in which metrics should be generated: every "metric interval" tau
    limited_time_to_transfer = True        # finite resources enabled
    restrict_band_access = True     # for xchants, forget how it works
    restrict_channel_access = True  # is there a limited amount of channels
    # priority_queue_active = True    # do you want to order the msgs in a nodes buffer in some way and send to destination first
    if num_fwd == 0:                # if/else statement for epidemic protocol vs forwarding, 0 = broadcast/epidemic
        broadcast = True
        geo_routing = False
    else:
        broadcast = False
        geo_routing = True
    num_nodes_to_fwd = num_fwd      # if forwarding, how many do you want to forward to, 0 = broadcast/epidemic

    fwd_strat = "broadcast" if broadcast == True else "geo_" + str(num_nodes_to_fwd) # create part of dynamic file directory for metrics

    dataset = DataSet               #UMass or Lexington
    day_or_numMules = Day_Or_NumMules#date (UMass) or number of mules (Lexington)(for lexington this number really doesn't mean anything it is just needed for the file structure)
    round = Round                    #Round number (also not too important anymore, but can be used to keep information from current simulation settings if you want to regenerate a link exist without losing current metrics)
    if Protocol == "Epidemic_Smart":
        protocol = Protocol + "_" + smart_setting    #Protocol in set of [Optimistic, Pessimistic, TV, LTE, ISM, CBRS]
    else:
        protocol = Protocol                         # not used anymore, didn't take out in case it is needed again for xchants

    if priority_queue_active == True:               # if testing with or without priority queue, another part of dynamic file directory for metrics
        buffer = "PQ"
    else:
        buffer = "FIFO"
    band = Band                    #bands to use in set of [ALL, TV, LTE, ISM, CBRS]
    generate_link_exists = Gen_LE   # is a new link exist being generated
    T = t                         #Length of Simulation
    V = v                          #Number of dataMules
    NoOfSources = src_dst[0]        # # of sources
    NoOfDataCenters = src_dst[1]    # # of destinations
    start_time = ts                 # start time
    max_nodes = Max_Nodes                  #All nodes include src and des

    # creates multiple file paths based on the dataset and the variables assigned above
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



    # creates a list of spectrums based on bands being used and the current smart setting
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

    # create the constants file based on all of these parameters
    create_constants(T, V, S, start_time, dataset, max_nodes, dataMule_path, metrics_path, link_exists_path,
                     debug_message, protocol, NoOfDataCenters, NoOfSources, generate_link_exists, generate_messages, num_messages,
                     pkl_fold_num, path_to_day1_LLC, perfect_knowledge, speed, limited_time_to_transfer, restrict_band_access,
                     restrict_channel_access, generate_new_primary_users, num_chan, num_puser, path_to_save_LLC, smart_setting,
                     priority_queue_active, broadcast, geo_routing, num_nodes_to_fwd, msg_round, puser_round, debug_mode, metric_interval,
                     msg_mean, ttl, max_mem, replicas)

    # generate a link exists if needed
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

    # run the simulation and metrics if you are not generating link exists
    if generate_LE == False:
        os.system("python3 main.py")
        os.system("python3 metrics.py")

# function to run simulations for ISC2 paper
def run_various_sims(num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas):
    for band in ["ALL", "TV", "CBRS", "LTE", "ISM"]:
        # print("Band:", band, "MSG round:", msg_round, "MSG mean:", msg_mean)
        if band == "ALL":
            for nodes_tofwd in [1, 0]:
                print("K:", nodes_tofwd)
                print("Optimistic")
                run_simulation(data, day, 3, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               "optimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas, True)
                print()
                print("Pessimistic")
                run_simulation(data, day, 3, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               "pessimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas, True)

        else:

            for nodes_tofwd in [0]:
                print("Band:", band, "K:", nodes_tofwd)
                run_simulation(data, day, 3, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               band, nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas, False)


# (DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,
#  src_dst_arr, speed_arr, num messages, num channels, num primary users, smart setting (optional))

data = "Lexington"
day = "50"
len_T = 360                     #length of simulation
start_time = 0                #start time (to find Link Exists)
bands = ["ALL", "LTE", "TV", "CBRS", "ISM"]  #which bands to use
num_mules = 48                  #number of data mules to use
generate_LE = False             #generate Link Exists
pkl_ID = 1                      #pkl folder ID if Link Exists is being generated
perfect_knowledge = False       #Xchant only
src_dst = [3, 3]                #num src and dst
max_v = num_mules + src_dst[0] + src_dst[1]                     #max number of datamules + src + dst
speed = [135, 400]                  #Lex data only
proto = "Epidemic_Smart"        #[Epidemic_Smart, XChant, SprayNWait (in progress)]
num_Pusers = 150
num_channels = 6
nodes_tofwd = 0
msg_round = 0
puser_round = 0
msg_mean = 15
ttl = 216
mem_size = 150
num_replicas = 10       # number of replicas/copies for geographic SnW


if generate_LE == False:

        run_various_sims(num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas)

    # for msg_round in range(5):
    #
    #     for msg_mean in [5, 10, 15, 20, 25]:
    #         run_various_sims(num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas)
    #
    #     msg_mean = 15
    #     for mem_size in [50, 100, 150, 200, -1]:
    #         run_various_sims(num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas)
    #
    #     mem_size = 150
    #     for ttl in [72, 144, 216, 288, 360]:
    #         run_various_sims(num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas)
    #
    #     # varying num of mules
    #     ttl = 216
    #     for num_mules in [8, 16, 32, 48, 64]:
    #         run_various_sims(num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas)
    #
    #     num_mules = 48
    #     # varying num of channels
    #     for num_channels in [2, 4, 6, 8, 10]:
    #         num_mules = 32
    #         run_various_sims(num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas)
    #
    #     num_channels = 6
    #     # varying num primary users
    #     for num_Pusers in [50, 150, 250, 350, 450]:
    #         num_channels = 6
    #         run_various_sims(num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas)



#Generate Link exists
else:
    run_simulation(data, day, 3, proto, "ALL", len_T, start_time, num_mules, generate_LE, max_v,
                                   pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                                   "optimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas, True)