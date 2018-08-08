from constants import *
from message import *
from node import *



class Network(object):
    def __init__(self):
        self.nodes = []                 #list of nodes in network
        self.message_num = 0
        self.time = 0

    def add_node(self, node):  # add node to network
        self.nodes.append(node)

    def network_status(self):                          #console output for debugging (prints all messages in each nodes buffer)
        for i in range(len(self.nodes)):
            self.nodes[i].print_buf()
            print(" ")

    def clear_all_channels(self):
        for node in self.nodes:
            node.clear_channels()

    def use_channels(self):
        for node in self.nodes:
            node.use_random_channels()

    def fill_network(self, num_nodes):  # quickly fill network and randomly place nodes
        for i in range(num_nodes):  # create and add nodes to network
            ide = str(i)
            node = Node(ide)
            # node.load_pkl()
            self.add_node(node)

    def find_avg_energy_consumption(self, time):
        total_energy = 0

        for node in self.nodes:
            total_energy += node.energy

        avg_energy = total_energy / (V +NoOfDataCenters + NoOfSources)

        f = open(path_to_folder + consumed_energy_file, 'a')
        f.write(str(time) + "\t" + str(avg_energy) + "\n")
        f.close()

    def get_message_info(self, path_lines, spec_lines, src, des, t, size):
        path = []
        band = []
        for ind in range(len(path_lines)):  # read each line from file to see if a new message needs to be generated
            path_line = path_lines[ind].strip()
            path_line_arr = path_line.split("\t")

            spec_line = spec_lines[ind].strip()
            spec_line_arr = spec_line.split("\t")

            if int(path_line_arr[2]) == int(t) and int(path_line_arr[0]) == int(src) and int(path_line_arr[1]) == int(des) and int(path_line_arr[3]) == int(size):

                path = path_line_arr[5: len(path_line_arr) - 1]
                band = spec_line_arr[5:]
        return path, band

        # Function messages_delivered: deletes messages that have been delivered
    def messages_delivered(self):
        for node in self.nodes:
            for mes in node.buf:
                if int(mes.des) == int(node.ID):
                    f = open(path_to_folder + delivered_file, "a")
                    band_usage_str = str(mes.band_usage[0]) + '\t' + str(mes.band_usage[1]) + '\t' + str(mes.band_usage[2]) + '\t' + str(mes.band_usage[3])

                    line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(mes.last_sent) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) +"\t\t" + str(mes.replica) + '\t' + band_usage_str + "\n"

                    f.write(line)
                    f.close()
                    node.buf.remove(mes)

    def other_add_messages(self, lines, time):
        for line in lines:
            line_arr = line.strip().split()

            if int(line_arr[5]) == time:
                for i in range(num_replicas):
                    new_mes = Message(line_arr[0], line_arr[1], line_arr[2], line_arr[5], line_arr[4], [0, 0, 0, 0], -1, -1, i)
                    src = int(line_arr[1])
                    self.nodes[src].buf.append(new_mes)

    def all_messages(self):
        f = open(path_to_folder + not_delivered_file, "a")
        for node in self.nodes:
            for mes in node.buf:
                line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(mes.last_sent) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t\t" + str(mes.replica) + "\n"
                f.write(line)
        f.close()

    def find_delay(self, size, s, specBW, i, j, t):
        bw = specBW[int(i), int(j), int(s), int(t)]
        return size / bw

    def xchant_add_messages(self, msg_lines, t, path_lines, spec_lines):

        for msg_id in range(len(msg_lines)):
            msg_line = msg_lines[msg_id].strip()
            msg_line_arr = msg_line.split("\t")

            if (int(msg_line_arr[5]) == t):  # if a new message needs to be generated at this time
                id = msg_line_arr[0]
                src = msg_line_arr[1]
                des = msg_line_arr[2]
                size = msg_line_arr[4]

                band, path = self.get_message_info(path_lines, spec_lines, src, des, t, size)

                message = Message(id, src, des, t, size, [0, 0, 0, 0], path, band,0)  # create the message
                curr = int(message.curr)

                # If a path exists for this message
                if len(message.path) > 0:
                    self.nodes[curr].buf.append(message)  # put the message in the source nodes buffer
                    self.nodes[curr].buf_size += 1
                    self.message_num += 1

    def try_forwarding_message_to_all1(self,src_node, message, t, LINK_EXISTS, specBW):
        replica = 0
        for des_node in self.nodes:
            to_send = True

            if des_node != src_node:
                for mes in des_node.buf:
                    if mes.ID == message.ID:
                        to_send = False

                if to_send == True:
                    if protocol == "Epidemic":
                        if src_node.try_sending_message_epi(des_node, message, t, replica, LINK_EXISTS, specBW):
                            replica += 1
                    elif protocol == "SprayNWait":
                        # if message.ID == debug_message:
                        #     print("curr", message.curr, "des", message.des)
                        src_node.try_sending_message_SnW(des_node, message, t, LINK_EXISTS, specBW)

    def try_forwarding_message_to_all2(self,src_node, message, t, LINK_EXISTS, specBW):

        real_des_node = self.nodes[message.des]
        #try to send to destination first
        if src_node.try_sending_message_HP(real_des_node, message, t, LINK_EXISTS, specBW) == False:
        #if destination not in range, try to send message to node with the least delay
            delays = []

            for des_node in self.nodes:
                temp_delays = []

                if des_node != src_node:

                    for s in S:
                        delay = self.find_delay(message.size, s, specBW, src_node.ID, des_node.ID, t)
                        temp_delays.append(delay)

                    min_delay = min(temp_delays)

                    delays.append(min_delay)

            best_min_delay = min(delays)
            MF_des_node = self.nodes[delays.index(best_min_delay)]

            src_node.try_sending_message_HP(MF_des_node, message, t, LINK_EXISTS, specBW)

    def network_GO(self, t, specBW, path_lines, spec_lines, msg_lines, LINK_EXISTS):  # function that sends all messages at a given tau

        self.clear_all_channels()
        self.use_channels()

    #Calculate energy consumption
        if t % 15 == 0 or t == T - 1:
            self.find_avg_energy_consumption(t)
    #Handle different protocols
        if protocol == "XChant":
            self.xchant_add_messages(msg_lines,t,path_lines,spec_lines)

            for i in range(len(self.nodes)):  # send all messages to their next hop
                node = self.nodes[i]
                isVisited = len(node.buf)  # Get the initial buffer size

                while len(node.buf) > 0 and isVisited > 0:
                    msg = node.buf[isVisited - 1]
                    if msg.ID == debug_message:
                        print("curr:", msg.curr, "PATH:", msg.path)
                    node.send_message_xchant(self, msg, t, specBW, LINK_EXISTS)
                    # the message gets deleted from the current node, and buffer gets shrinked
                    # isVisited is to get to the end of the node buffer even if it is not empty
                    isVisited -= 1
        else:
            self.other_add_messages(msg_lines,t)

            for i in range(len(self.nodes)):
                node = self.nodes[i]
                # For each message in this nodes buffer
                for mes in node.buf:
                    if mes.last_sent <= t:
                        if protocol == "HotPotato":
                            self.try_forwarding_message_to_all2(node,mes,t,LINK_EXISTS,specBW)
                        else:
                            self.try_forwarding_message_to_all1(node, mes, t, LINK_EXISTS, specBW)
            # Handle messages that got delivered
            self.messages_delivered()







