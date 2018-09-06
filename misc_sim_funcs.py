from constants import *
import os
import pickle
import random




def get_data_structs():
    if protocol == "XChant":
        with open(path_to_LLC + "LLC_PATH.txt", "r") as f:
            path_lines = f.readlines()[1:]

        with open(path_to_LLC + "LLC_Spectrum.txt", "r") as f:
            spec_lines = f.readlines()[1:]

    else:
        path_lines = []
        spec_lines = []

    with open(DataMule_path + "Link_Exists/" + generated_messages_file, "r") as f:
        msg_lines = f.readlines()[1:num_messages + 1]

    specBW = pickle.load(open(link_exists_folder + "specBW.pkl", "rb"))
    LINK_EXISTS = pickle.load(open(link_exists_folder + "LINK_EXISTS.pkl", "rb"))

    return path_lines, spec_lines, msg_lines, specBW, LINK_EXISTS

def initialize_output_files():

    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)

    if not os.path.exists(path_to_metrics):
        os.makedirs(path_to_metrics)

    output_file = open(path_to_metrics + delivered_file, "w")
    output_file.write("ID\ts\td\tts\tte\tLLC\tPid\tsize\tband usage\n")
    output_file.write("----------------------------------------------------\n")
    output_file.close()

    output_file2 = open(path_to_metrics  + consumed_energy_file, 'w')
    output_file2.write("Time\tEnergy\n")
    output_file2.close()

    output_file3 = open(path_to_metrics + not_delivered_file, "w")
    output_file3.write("ID\ts\td\tts\tte\tLLC\tsize\tcurr node\tpacketID\n")
    output_file3.write("----------------------------------------------------\n")
    output_file3.close()

    output_file4 = open(path_to_metrics + packet_delivered_file, "w")
    output_file4.close()

def write_delivered_msg_to_file(message, te):

    # if message has reached its destination
    # if len(message.path) == 0: #and message.src != message.des: # and message.T  + message.totalDelay <= T:
        output_file = open(path_to_metrics + packet_delivered_file, "a")  # print confirmation to output file
        band_usage_str = str(message.band_usage[0]) + '\t' + str(message.band_usage[1]) + '\t' + str(
            message.band_usage[2]) + "\t" + str(message.band_usage[3])

        output_msg = str(message.ID) + "\t" + str(message.src) + "\t" + str(message.des) + "\t" + str(
            message.genT) + "\t" + str(int(te)) + "\t" + str(
            int(te - message.genT)) + "\t" +  str(message.packet_id) + "\t" + str(message.size) +  "\t" + str(
            message.totalEnergy) + "\t" + band_usage_str + "\n"

        output_file.write(output_msg)
        output_file.close()

def find_nodes_in_range(src_node, net, s, LINK_EXISTS, ts):

    if ts == T - 1:
        te = ts
    else:
        te = ts + 1

    all_nodes = net.nodes
    nodes_in_range = []

    for node in all_nodes:

        if node != src_node and LINK_EXISTS[int(src_node.ID), int(node.ID), int(s), int(ts), int(te)] == 1:
            if smart_setting == "pessimistic" and s < 3:
                if LINK_EXISTS[int(src_node.ID), int(node.ID), int(s + 1), int(ts), int(te)] == 0:
                    nodes_in_range.append(node)
            else:
                nodes_in_range.append(node)



    return nodes_in_range

def initialize_s():
    if smart_setting == "optimistic":
        s = 3
    elif smart_setting == "pessimistic":
        s = 0
    elif smart_setting == "random":
        s = random.randint(0, 3)
    else:
        s = -1

    return s

def update_s(s):


    if smart_setting == "optimistic":
        new_s = s - 1

    elif smart_setting == "pessimistic":
        new_s = s + 1

    elif smart_setting == "random":
        loop_flag = True

        while loop_flag == True:
            new_s = random.randint(0, 3)

            if new_s != s:
                loop_flag = False
    else:
        new_s = -1


    return new_s

# checks if a given packet is already in a nodes buffer
def to_send(msg, node):

    # check if packet is in buffer
    for m in node.buf:
        if m.ID == msg.ID and m.packet_id == msg.packet_id:
            return False
    # check if packet has been delivered
    for m in node.delivered:
        if m.ID == msg.ID and m.packet_id == msg.packet_id:
            return False

    return True

def sort_by_genT(msg_list):
    sorted_list = []

    # while there are msgs to be sorted
    while(len(msg_list) > 0):

        # init sorting vars
        lowest_ind = -1
        lowest_val = 1000000
        # find msg with lowest genT
        for i in range(len(msg_list)):
            if msg_list[i].genT < lowest_val:
                lowest_val = msg_list[i].genT
                lowest_ind = i
        # add msg to new list
        sorted_list.append(msg_list[lowest_ind])
        msg_list.pop(lowest_ind)

    return sorted_list

def get_msg_lists(nodes_in_range, curr_node):
    nodes_in_range_IDs = []
    for node in nodes_in_range:
        nodes_in_range_IDs.append(node.ID)

    msgs_in_range = []
    msgs_not_in_range = []
    # check if any messages in buffer are in range with destination
    for msg in curr_node.buf:
        if msg.des in nodes_in_range_IDs:
            msgs_in_range.append(msg)
        else:
            msgs_not_in_range.append(msg)

    return msgs_in_range, msgs_not_in_range

def sort_and_combine_msg_lists(msgs_IR, msgs_OR):
    # sort lists
    sorted_msgs_IR = sort_by_genT(msgs_IR)
    sorted_msgs_OR = sort_by_genT(msgs_OR)

    #combine lists
    final_buffer = []
    for i in range(len(sorted_msgs_IR)):
        final_buffer.append(sorted_msgs_IR[i])

    for i in range(len(sorted_msgs_OR)):
        final_buffer.append(sorted_msgs_OR[i])

    return final_buffer

def des_in_range(nodes_in_range, node):
    nodes_in_range_IDs = []
    for nodeIR in nodes_in_range:
        nodes_in_range_IDs.append(nodeIR.ID)

    # checks if there exists a msg in range with its destination
    for msg in node.buf:
        if msg.des in nodes_in_range_IDs:
            return True

    return False

def choose_spectrum(node, net, LINK_EXISTS, t):
    # s = initialize_s()
    it = 0
    s = S[it]

    # loop through bands until a valid one is chosen
    while s >= 0 and s < 4 and it < 4:
        # get nodes in range of s
        nodes_in_range = find_nodes_in_range(node, net, s, LINK_EXISTS, t)

        if len(nodes_in_range) > 0:
            # if priority queue is active send to destinations first
            if priority_queue == True:
                # if any destinations are in range use this band
                if des_in_range(nodes_in_range, node) == True:
                    return s, nodes_in_range
                else:
                    # s = update_s(s)
                    it += 1
                    if it < 4:
                        s = S[it]
            else:
                return s, nodes_in_range

        else:
            # s = update_s(s)
            it += 1
            if it < 4:
                s = S[it]

    # in the case that priority queue is enabled and no msg is in range with its dst over any band, choose
    # the first band, based on smart setting, that is in range with at least 1 node
    # s = initialize_s()
    it = 0
    s = S[it]

    # loop through bands until a valid one is chosen
    while s >= 0 and s < 4 and it < 4:
        # get nodes in range of s
        nodes_in_range = find_nodes_in_range(node, net, s, LINK_EXISTS, t)

        if len(nodes_in_range) > 0:
            return s, nodes_in_range

        else:
            # s = update_s(s)
            it += 1
            if it < 4:
                s = S[it]

    # if a node is not in range with anyone then initial band is returned
    # s = initialize_s()
    s = S[0]
    nodes_in_range = find_nodes_in_range(node, net, s, LINK_EXISTS, t)
    return s, nodes_in_range
