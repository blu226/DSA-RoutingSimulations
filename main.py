import pickle
from constants import *
from network import *
import os



def initialize_output_files():
    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)
    output_file = open(path_to_folder + delivered_file, "w")
    output_file.write("ID\ts\td\tts\tte\tLLC\tELC\n")
    output_file.write("----------------------------------------------------\n")
    output_file.close()

    output_file2 = open(path_to_folder  + consumed_energy_file, 'w')
    output_file2.write("Time\tEnergy\n")
    output_file2.close()

    output_file3 = open(path_to_folder + not_delivered_file, "w")
    output_file3.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\tparentTime\treplica\tenergy\n")
    output_file3.write("----------------------------------------------------\n")
    output_file3.close()




initialize_output_files()

net = Network()
net.fill_network(V + NoOfSources + NoOfDataCenters)

#Open LLC_path.txt, LLC_spectrum.txt, generated_messages, specBW, LINK_EXISTS
if protocol == "XChant":
    with open(path_to_LLC + "LLC_PATH.txt", "r") as f:
        path_lines = f.readlines()[1:]

    with open(path_to_LLC + "LLC_Spectrum.txt", "r") as f:
        spec_lines = f.readlines()[1:]

else:
    path_lines = []
    spec_lines = []

with open(DataMule_path + "Link_Exists/" + generated_messages_file, "r") as f:
    msg_lines = f.readlines()[1:]

specBW = pickle.load(open(link_exists_folder + "specBW.pkl", "rb"))
LINK_EXISTS = pickle.load(open(link_exists_folder + "LINK_EXISTS.pkl", "rb"))


for t in range(0, T, tau):

    net.network_GO(t, specBW, path_lines, spec_lines, msg_lines, LINK_EXISTS)
    # net.network_status()

net.all_messages()  #creates not_delivered.txt for overhead computation

