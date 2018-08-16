from constants import *
import os
import pickle




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
    output_file.write("ID\ts\td\tts\tte\tLLC\tELC\n")
    output_file.write("----------------------------------------------------\n")
    output_file.close()

    output_file2 = open(path_to_metrics  + consumed_energy_file, 'w')
    output_file2.write("Time\tEnergy\n")
    output_file2.close()

    output_file3 = open(path_to_metrics + not_delivered_file, "w")
    output_file3.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\tparentTime\treplica\tenergy\n")
    output_file3.write("----------------------------------------------------\n")
    output_file3.close()

    output_file4 = open(path_to_metrics + packet_delivered_file, "w")
    output_file4.close()

def write_delivered_msg_to_file(nodes, message, ts):

    # if message has reached its destination
    # if len(message.path) == 0: #and message.src != message.des: # and message.T  + message.totalDelay <= T:
    if ts <= T:  # delivered time is less than the allowed TTL deadline
        output_file = open(path_to_metrics + packet_delivered_file, "a")  # print confirmation to output file
        band_usage_str = str(message.band_usage[0]) + '\t' + str(message.band_usage[1]) + '\t' + str(
            message.band_usage[2]) + "\t" + str(message.band_usage[3])

        output_msg = str(message.ID) + "\t" + str(message.src) + "\t" + str(message.des) + "\t" + str(
            message.genT) + "\t" + str(int(message.last_sent)) + "\t" + str(
            int(message.last_sent - message.genT)) + "\t" + str(message.size) + "\t" + str(
            message.totalEnergy) + "\t" + band_usage_str + "\n"

        output_file.write(output_msg)
        output_file.close()



