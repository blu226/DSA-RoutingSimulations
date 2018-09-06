from constants import *
from message import *
from node import *
from primary_user import *



class Network(object):
    def __init__(self):
        self.nodes = []                 #list of nodes in network
        self.primary_users = []            #list of primary users
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

    def activate_primary_users(self):

        for p_user in self.primary_users:
            p = random.uniform(0,1)

            if p < active_channel_prob:
                p_user.active = True
            else:
                p_user.active = False

    def create_primary_users(self, num_C):
            for x in range(num_primary_users):
                p_user = PrimaryUser(num_C)
                p_user.place()
                self.primary_users.append(p_user)

    def save_primary_users(self, num_C):
        with open("Primary_Users/primary_users_" + str(num_C) + ".txt", "w") as f:
            for p_user in self.primary_users:
                line = str(p_user.x) + "\t" + str(p_user.y) + "\t" + str(p_user.channel) + "\t" + str(p_user.band) + "\n"
                f.write(line)

    def load_primary_users(self):
        with open("Primary_Users/primary_users_" + str(num_channels) + ".txt", "r") as f:
            lines = f.readlines()

            for line_ind in range(num_primary_users):
                line_arr = lines[line_ind].strip().split()
                p_user = PrimaryUser()
                p_user.set(float(line_arr[0]), float(line_arr[1]), int(line_arr[2]), int(line_arr[3]))

                self.primary_users.append(p_user)

    def fill_network(self, num_nodes):  # quickly fill network and randomly place nodes
        for i in range(num_nodes):  # create and add nodes to network
            ide = str(i)
            node = Node(ide)
            node.load_pkl()
            self.add_node(node)

    def find_avg_energy_consumption(self, time):
        total_energy = 0

        for node in self.nodes:
            total_energy += node.energy

        avg_energy = total_energy / (V +NoOfDataCenters + NoOfSources)

        f = open(path_to_metrics + consumed_energy_file, 'a')
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

        with open(DataMule_path + "Link_Exists/" + generated_messages_file, "r") as f:
            msg_lines = f.readlines()[1:num_messages + 1]

        with open(path_to_metrics + packet_delivered_file, 'r') as f:
            lines = f.readlines()

        for msg_line in msg_lines:
            msg_arr = msg_line.strip().split()
            msg_id = msg_arr[0]
            msg_size = msg_arr[4]
            num_packets_recieved = 0
            num_packets = math.ceil(int(msg_size) / int(packet_size))
            packetIDs = [x for x in range(num_packets)]

            for line in lines:
                line_arr = line.strip().split()

                if line_arr[0] == msg_id and int(line_arr[6]) in packetIDs:
                    num_packets_recieved += 1
                    packetIDs.remove(int(line_arr[6]))

                if num_packets_recieved == num_packets and len(packetIDs) == 0:
                    f = open(path_to_metrics + delivered_file, "a")
                    f.write(line)
                    f.close()
                    break



    def other_add_messages(self, lines, time):
        for line in lines:
            line_arr = line.strip().split()

            if int(line_arr[5]) == time:
                num_packets = math.ceil(int(line_arr[4]) / int(packet_size))

                for i in range(num_replicas):
                    for j in range(num_packets):
                        new_mes = Message(line_arr[0], line_arr[1], line_arr[2], line_arr[5], line_arr[4], [0, 0, 0, 0], -1, -1, i, j)
                        src = int(line_arr[1])
                        self.nodes[src].buf.append(new_mes)

    def not_delivered_messages(self):
        f = open(path_to_metrics + not_delivered_file, "a")
        for node in self.nodes:
            for mes in node.buf:
                line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(mes.last_sent) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t" + str(mes.curr) + "\t" + str(mes.packet_id) +"\n"
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

                num_packets = math.ceil(int(size) / int(packet_size))
                for packet_id in range(num_packets):
                    band, path = self.get_message_info(path_lines, spec_lines, src, des, t, size)

                    message = Message(id, src, des, t, size, [0, 0, 0, 0], path, band, 0, packet_id)  # create the message
                    curr = int(message.curr)

                    # If a path exists for this message
                    if len(message.path) > 0:
                        self.nodes[curr].buf.append(message)  # put the message in the source nodes buffer
                        self.nodes[curr].buf_size += 1
                        self.message_num += 1

                    else:
                        print("Message generated with no path.")

    def try_forwarding_message_to_all1(self,src_node, message, t, LINK_EXISTS, specBW):
        replica = 0
        #Check if in range with each node
        for des_node in self.nodes:
            to_send = True
            #Check if next node already has the message
            if des_node != src_node:
                for mes in des_node.buf:
                    if mes.ID == message.ID and mes.packet_id == message.packet_id:
                        to_send = False

                if to_send == True:
                    if protocol == "Epidemic":
                        if src_node.try_sending_message_epi(des_node, message, t, replica, LINK_EXISTS, specBW, self):
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
        # clear all channels and check if primary users are active
        self.clear_all_channels()
        self.activate_primary_users()
        # print("TIME:", t)
        #Calculate energy consumption
        if t % 15 == 0 or t == T - 1:
            self.find_avg_energy_consumption(t)

        #Handle different protocols
        if protocol == "XChant":
            self.xchant_add_messages(msg_lines,t,path_lines,spec_lines)

            #TODO: loop thru nodes randomly instead of linearly
            for i in range(len(self.nodes)):  # send all messages to their next hop
                node = self.nodes[i]
                isVisited = len(node.buf)   # Get the initial buffer size
                msg_index = 0               # init index of msg buffer
                was_sent = False            # init variable to check if a message could send

                # Checks to see what spectrum to use for tau
                if len(node.buf) > 0 and len(node.buf[msg_index].bands) > 0:
                    spec_to_use = node.buf[msg_index].bands[len(node.buf[msg_index].bands) - 1]

                while len(node.buf) > 0 and isVisited > 0:
                    msg = node.buf[msg_index]
                    #The band is restricted for a given time slot (i.e., 1 tau) and can not be changed
                    if is_queuing_active == True and restrict_band_access == True:
                        if len(msg.bands) > 0 and msg.bands[len(msg.bands) - 1] == spec_to_use:
                            # TODO: get the suitable non-interfered channel
                            was_sent = node.send_message_xchant(self, msg, t, specBW, LINK_EXISTS)

                    else:
                        # TODO: get the suitable non-interfered channel
                        was_sent = node.send_message_xchant(self, msg, t, specBW, LINK_EXISTS)
                    # the message gets deleted from the current node, and buffer gets shrinked
                    # isVisited is to get to the end of the node buffer even if it is not empty
                    isVisited -= 1
                    if was_sent == False:
                        # print("node:", node.ID, "msg ID:", msg.ID, "pckt ID:", msg.packet_id, "t:", t)
                        msg_index += 1

        elif "Epidemic_Smart" in protocol:
            # add messages to source nodes
            self.other_add_messages(msg_lines, t)

           # loop over each node
            for node in self.nodes:
                # init band based on smart setting
                s, nodes_in_range = choose_spectrum(node, self, LINK_EXISTS, t)
                # send msgs to destinations first if priority queue is enabled
                if priority_queue == True:
                    # order the msg buffer based on genT and if its in range of des
                    node.order_priority_queue(nodes_in_range)
                    # loop until msg at top of buffer can't be sent to its destination
                    for i in range(len(node.buf)):
                        # get msg to be sent
                        msg = node.buf[0]
                        des_node = self.nodes[int(msg.des)]
                        # check if msg has already reached its destination
                        if to_send(msg, des_node) == True:
                            if node.try_sending_message_epi(des_node, msg, t, LINK_EXISTS, specBW, self, s) == False:
                                # if msg can't be sent, break from loop
                                break
                        # if msg has already been sent to its destination then delete from buffer
                        else:
                            node.buf.remove(msg)

                # continue to flood messages that are not in range of their destinations
                for des_node in nodes_in_range:
                    for msg in node.buf:
                        # check if des_node already has packet
                        if to_send(msg, des_node) == True:
                            node.try_sending_message_epi(des_node, msg, t, LINK_EXISTS, specBW, self, s)



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









