import pickle
from STB_help import *
import math




def get_data_structs():
    if protocol == "XChant":
        with open(path_to_LLC + "LLC_PATH.txt", "r") as f:
            path_lines = f.readlines()[1:]

        with open(path_to_LLC + "LLC_Spectrum.txt", "r") as f:
            spec_lines = f.readlines()[1:]

    else:
        path_lines = []
        spec_lines = []

    with open(generated_messages_file, "r") as f:
        msg_lines = f.readlines()[1:]

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
    output_file4.write("ID\ts\td\tts\tte\tLLC\tPID\tsize\thops\tband usage\n")
    output_file4.close()

    output_file5 = open(path_to_metrics + overhead_file, "w")
    output_file5.close()

def write_delivered_msg_to_file(message, te):

    # if message has reached its destination
    # if len(message.path) == 0: #and message.src != message.des: # and message.T  + message.totalDelay <= T:
        output_file = open(path_to_metrics + packet_delivered_file, "a")  # print confirmation to output file
        band_usage_str = str(message.band_usage[0]) + '\t' + str(message.band_usage[1]) + '\t' + str(
            message.band_usage[2]) + "\t" + str(message.band_usage[3])

        output_msg = str(message.ID) + "\t" + str(message.src) + "\t" + str(message.des) + "\t" + str(
            message.genT) + "\t" + str(int(te)) + "\t" + str(
            int(te - message.genT)) + "\t" +  str(message.packet_id) + "\t" + str(message.size) + "\t" + str(message.hops) + "\t" + band_usage_str + "\n"

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
        if node != src_node and LINK_EXISTS[int(src_node.ID), int(node.ID), int(s), int(ts)] == 1:
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

def write_to_not_delivered(mes):
    f = open(path_to_metrics + not_delivered_file, "a")

    line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(
        mes.last_sent) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t" + str(
        mes.curr) + "\t" + str(mes.packet_id) + "\n"
    f.write(line)
    f.close()

# checks if a given packet is already in a nodes buffer
def to_send(msg, node, t):

    #check if message was received by node in current time slot
    if t < msg.last_sent:
        return False

    # check if packet is in buffer
    for m in node.buf:
        if m.ID == msg.ID and m.packet_id == msg.packet_id:
            return False
    # check if packet has been delivered
    for m in node.delivered:
        if m.ID == msg.ID and m.packet_id == msg.packet_id:
            return False

    return True

# sorts msgs by generation time. original code puts earlier generation times first, returning reversed so newer gen times

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

    #sort by highest genT
    return list(reversed(sorted_list))
    #sort by lowest genT
    # return list(sorted_list)


def get_msg_lists(nodes_in_range, curr_node):
    nodes_in_range_IDs = []
    for node in nodes_in_range:
        nodes_in_range_IDs.append(int(node.ID))

    msgs_in_range = []
    msgs_not_in_range = []
    # check if any messages in buffer are in range with destination
    for msg in curr_node.buf:
        if int(msg.des) in nodes_in_range_IDs:
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

def des_in_range(nodes_in_range, node, t):
    nodes_in_range_IDs = []
    for nodeIR in nodes_in_range:
        nodes_in_range_IDs.append(int(nodeIR.ID))

    # checks if there exists a msg in range with its destination
    for msg in node.buf:

        if msg.des in nodes_in_range_IDs:
            #get des node
            for nodeIR in nodes_in_range:
                if int(nodeIR.ID) == int(msg.des):
                    des_node = nodeIR
                    # break
            # check if des node has already received msg
                    if to_send(msg, des_node, t) == True:
                        if (node.ID == "15" and t == 60 and des_node.ID == "7" and debug_mode == 1):
                            print("Delivered:", [str(msg.ID) + " " + str(msg.packet_id) for msg in des_node.delivered])
                        return True

    return False

def choose_spectrum(node, net, LINK_EXISTS, t):
    chosen_spec = S[0]

    # if (node.ID == "15" and t == 60):
    #     print("MSG des:", [msg.ID for msg in node.buf])

    #Handle priority queue
    # if priority queue is active send to destinations first
    if priority_queue == True:
        is_dest_node_found = False
        for s in S:

            if node.is_there_an_open_channel(s) == True:

                if (node.ID == "15" and t == 60 and debug_mode == 1):
                    print("S:", s)

                nodes_in_range = find_nodes_in_range(node, net, s, LINK_EXISTS, t)

                if (node.ID == "15" and t == 60 and debug_mode == 1):
                    print("nodes in range", [node.ID for node in nodes_in_range])

                if len(nodes_in_range) > 0:
                    # if any destinations are in range use this band
                    if des_in_range(nodes_in_range, node, t) == True:

                        is_dest_node_found = True
                        chosen_spec = s

                        return chosen_spec, nodes_in_range


        if is_dest_node_found == False:
            if (node.ID == "15" and t == 60 and debug_mode == 1):
                print("dest not in range", [node.ID for node in nodes_in_range])
            chosen_spec = default_spec_band(node, net, LINK_EXISTS, t)

    else: #FIFO
        chosen_spec = default_spec_band(node, net, LINK_EXISTS, t)
    return chosen_spec


def default_spec_band(node, net, LINK_EXISTS, t):
    chosen_spec = S[0]
    nodes_in_range = find_nodes_in_range(node, net, chosen_spec, LINK_EXISTS, t)



    if len(nodes_in_range) > 0 and smart_setting != "pessimistic" and node.is_there_an_open_channel(chosen_spec) == True:
        return chosen_spec, nodes_in_range

    #If NOT pessimistic, and no nodes in range or is a pessimistic approach
    # loop through bands until a valid one is chosen
    for i in range(1, 4):
        if node.is_there_an_open_channel(chosen_spec) == True:
            next_nodes_in_range = find_nodes_in_range(node, net, S[i], LINK_EXISTS, t)
            if len(next_nodes_in_range) > 0:
                if smart_setting != "pessimistic":
                    chosen_spec = S[i]
                    nodes_in_range = next_nodes_in_range
                    break

                else:
                    if nodes_in_range == next_nodes_in_range:
                        nodes_in_range = next_nodes_in_range
                        chosen_spec = S[i]

                    else:
                        break

    return chosen_spec, nodes_in_range

        # # print("nodes in range", S[i], ":", [node.ID for node in nodes_in_range])
        # if len(nodes_in_range) > 0:
        #     # if priority queue is active send to destinations first
        #     if priority_queue == True:
        #         # if any destinations are in range use this band
        #         if des_in_range(nodes_in_range, node) == True:
        #             return S[i], nodes_in_range
        #
        #     else:
        #         return S[i], nodes_in_range

    # in the case that priority queue is enabled and no msg is in range with its dst over any band, choose
    # the first band, based on smart setting, that is in range with at least 1 node
    # loop through bands until a valid one is chosen
    # for i in range(4):
    #     # get nodes in range of s
    #     nodes_in_range = find_nodes_in_range(node, net, i, LINK_EXISTS, t)
    #
    #     if len(nodes_in_range) > 0:
    #         return S[i], nodes_in_range
    #
    # # if a node is not in range with anyone then initial band is returned
    # s = S[0]
    # nodes_in_range = find_nodes_in_range(node, net, s, LINK_EXISTS, t)


def find_distance(x1, y1, x2, y2):
    if dataset == "Lexington":
        dist = euclideanDistance(x1, y1, x2, y2)
    elif dataset == "UMass":
        dist = funHaversine(y1, x1, y2, x2)

    return dist

def get_suitable_spectrum_list(setting):
    w1 = 0
    w2 = 0
    sum_list = []
    S = []
    if "optimistic" in setting:
        w2 = 1
    elif "pessimistic" in setting:
        w1 = 1
    else:
        w1 = .2
        w2 = .8

    for i in range(len(spectRange)):
        sum = (w1 * math.exp(-(1/(spectRange[i]/1000)))) + (w2 * math.exp(-(1/minBW[i])))
        sum_list.append(sum)


    for i in range(4):
        ind = sum_list.index(max(sum_list))
        S.append(ind)
        sum_list[ind] = 0

    return S


def find_node_closest_to_dst(node_list):
    min_dist = 9999999

    for node in node_list:
        if node[1] < min_dist:
            min_dist = node[1]
            node_to_forward = node

    return node_to_forward
