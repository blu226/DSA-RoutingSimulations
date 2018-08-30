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

def update_s(s, spec_chosen):
    if spec_chosen == False:

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

    else:
        new_s = -1

    return new_s

# checks if a given packet is already in a nodes buffer
def to_send(msg, node):

    for m in node.buf:
        if m.ID == msg.ID and m.packet_id == msg.packet_id:
            return False

    for m in node.delivered:
        if m.ID == msg.ID and m.packet_id == msg.packet_id:
            return False

    return True






