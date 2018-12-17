#Create Constant file for simulation

def create_constants(T, V, S, start_time, dataset, max_nodes, DataMule_dir, path_to_folder, link_exists_folder, debug_message,\
                     protocol, NoOfDataCenters, NoOfSources, generate_link_exists, generate_messages, num_messages,\
                     pkl_folder_num, path_to_day1_LLC, perfect_knowledge, speed, is_queuing_active, restrict_band_access, \
                     restrict_channel_access, generate_new_primary_users, num_chan, num_puser, path_to_save_LLC, \
                     smart_setting, priority_queue_active, broadcast, geo_routing, num_nodes_to_fwd, msg_file, puser_file, \
                     debug_m, metric_int):

    f = open("constants.py", "w")

    T_line = "T = " + str(T) + "\n"
    V_line = "V = " + str(V) + "\n"
    S_line = "S = " + str(S) + "\n"
    src_line = "NoOfSources = " + str(NoOfSources) + "\n"
    dc_line = "NoOfDataCenters = " + str(NoOfDataCenters) + "\n"
    ds_line = "dataset = " + "\"" +  str(dataset) + "\"" + "\n"
    mn_line = "max_nodes = " + str(max_nodes) + "\n"
    dmd_line = "DataMule_path = \'" + str(DataMule_dir) + "\'\n"
    ptf_line = 'path_to_folder = \'' + str(path_to_folder) + "\'\n"
    st_line = "StartTime = " + str(start_time) + "\n"
    dm_line = "debug_message = " + str(debug_message) + "\n"
    lef_line = "link_exists_folder = \'" + str(link_exists_folder) + "\'\n"
    ptm_line = "path_to_metrics = '" + path_to_folder + "/msgfile" + str(msg_file) + "/puserfile" + str(puser_file) + "/\'\n"
    queue_line = "is_queuing_active = " + str(is_queuing_active) + "\n"
    rb_line = "restrict_band_access = " + str(restrict_band_access) + "\n"
    rc_line = "restrict_channel_access = " + str(restrict_channel_access) + "\n"
    pq_line = "priority_queue = " + str(priority_queue_active) + "\n"
    b_line = "broadcast = " + str(broadcast) + "\n"
    geo_line = "geographical_routing = " + str(geo_routing) + "\n"
    gpu_line = "generate_new_primary_users = " + str(generate_new_primary_users) + "\n"
    generated_messages_file = "Generated_Messages/generated_messages" + str(msg_file) + ".txt'\n"
    gen_LE_line = "generate_link_exists = " + str(generate_link_exists) + "\n"
    gen_mes_line = "generate_messages = " + str(generate_messages) + "\n"
    num_mes_line = "num_messages = " + str(num_messages) + "\n"
    pkl_line = "pkl_folder = \'Day" + str(pkl_folder_num) + "_pkl/\'\n"
    chan_line = "num_channels = " + str(num_chan) + "\n"
    puser_line = "num_primary_users = " + str(num_puser) + "\n"
    pts_line = "path_to_save_LLC = \'" + path_to_save_LLC + "\'\n"
    ss_line = "smart_setting = \'" + smart_setting + "\'\n"
    ntf_line = "num_nodes_to_fwd = " + str(num_nodes_to_fwd) + "\n"
    puser_round = "puser_round = " + str(puser_file) + "\n"
    debug_mode = "debug_mode = " + str(debug_m) + "\n"
    oh_file = "overhead_file = 'overhead.txt'\n"
    met_int = "metric_interval = " + str(metric_int) + "\n"
    if perfect_knowledge == True and protocol == "XChant":
        delivered_file = "delivered_messages_opt.txt"
        consumed_energy_file = "energy_metrics_opt.txt"
        not_delivered_file = "not_delivered_opt.txt"
        metrics_file = "metrics_opt.txt"
        LLC_line = "path_to_LLC = \'" + path_to_folder + "\'\n"
        packet_delivered_file = "packets_delivered_opt.txt"


    else:
        delivered_file = "delivered_messages.txt"
        consumed_energy_file = "energy_metrics.txt"
        not_delivered_file = "not_delivered.txt"
        metrics_file = "metrics.txt"
        packet_delivered_file = "packets_delivered.txt"
        LLC_line = "path_to_LLC = \'" + str(path_to_day1_LLC) + "\'\n"

    if protocol == "SprayNWait":
        num_reps_line = "num_replicas = 20\n"
    else:
        num_reps_line = "num_replicas = 1\n"

    f.write("numSpec = 4\ndt = 1\ntau = 1\n")
    f.write("minBW = [5,20,30,60]\nmaxBW = [5,20,30,60]\nspectRange = [1200,180,800,300]\nspectPower = [4,1,4,10]\nepsilon = 0.5\n")
    f.write("t_sd = 0.5\nt_td = 1\nidle_channel_prob = 0.5\nswitching_delay = 0.001\nsensing_power = 0.04\nlambda_val = 1\nmessageBurst = [2, 5]\n\n")
    f.write("TTL = 120\nminTTL=15\nmaxTau = 1\ndefault_num_channels = 10\nM = [60,600,1500,3000]\npacket_size = 300\nnum_sec_per_tau = 60\nactive_channel_prob = 1\n")

    f.write(T_line)
    f.write(V_line)
    f.write(src_line)
    f.write(dc_line)
    f.write(S_line)
    f.write(mn_line)
    f.write(st_line)
    f.write(dm_line)
    f.write(ds_line)
    f.write(gen_LE_line)
    f.write(gen_mes_line)
    f.write(num_mes_line)
    f.write(dmd_line)
    f.write(ptf_line)
    f.write(ptm_line)
    f.write(pkl_line)
    f.write(LLC_line)
    f.write(num_reps_line)
    f.write(queue_line)
    f.write(rb_line)
    f.write(rc_line)
    f.write(pq_line)
    f.write(b_line)
    f.write(geo_line)
    f.write(ntf_line)
    f.write(gpu_line)
    f.write(chan_line)
    f.write(puser_line)
    f.write(pts_line)
    f.write(puser_round)


    f.write(lef_line)
    f.write("delivered_file = \'" + delivered_file + "\'\n")
    f.write("consumed_energy_file = \'" + consumed_energy_file + "\'\n")
    f.write("not_delivered_file = \'" + not_delivered_file + "\'\n")
    f.write("generated_messages_file = \'" + generated_messages_file + "\n")
    f.write("metrics_file = \'" + metrics_file + "\'\n")
    f.write("packet_delivered_file = \'" + packet_delivered_file + "\'\n")
    f.write("protocol = \'" + protocol + "\'\n")
    f.write(ss_line)
    f.write(debug_mode)
    f.write(oh_file)
    f.write(met_int)

    if dataset == "Lexington":
        f.write("\nVMIN = " + str(speed[0]) + "\n")
        f.write("VMAX = " + str(speed[1]) +"\n")
        f.write("wait_time = [2,7]\n")
        f.write("route_start_time1 = 0\nroute_start_time2 = 5\n")
        f.write("lex_data_directory = \'Lexington/\'\n")
        f.write("day_num = " + str(pkl_folder_num) + "\n")
