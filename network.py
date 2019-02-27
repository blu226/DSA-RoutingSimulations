from constants import *
from message import *
from node import *
from primary_user import *

#TODO: recompute link exists with shorter ranges, re run tests. Run for Lexington


class Network(object):
    def __init__(self):
        self.nodes = []                 #list of nodes in network
        self.primary_users = []            #list of primary users
        self.message_num = 0            # something for xchants currently
        self.time = 0                   # keep track of current time in network
        self.band_usage = [0, 0, 0, 0]  # keep track of band usage in network
        self.packets_per_tau = 0        # keep track of how many packets per tau are sent
        self.parallel_coms = 0          # keep track of how many parallel communications are happening per tau
        self.packets_per_tau_list = []  # keep track of how many packets per tau are sent
        self.parallel_coms_list = []    # keep track of how many parallel communications are happening per tau

    def add_node(self, node):  # add node to network
        self.nodes.append(node)

    def print_bandusage(self):
        total = self.band_usage[0] + self.band_usage[1] + self.band_usage[2] + self.band_usage[3]
        print("TV:", self.band_usage[0]/total, "ISM:", self.band_usage[1]/total, "LTE:", self.band_usage[2]/total, "CBRS:", self.band_usage[3]/total)

    def network_status(self):              #console output for debugging (prints all messages in each nodes buffer)
        for i in range(len(self.nodes)):
            self.nodes[i].print_buf()
            print(" ")

    def clear_all_channels(self):           # clears all channels in each node
        for node in self.nodes:
            node.clear_channels()

    def activate_primary_users(self):       # activates all primary users for a given tau

        for p_user in self.primary_users:
            if p_user.on_off[0] == 0:
                p_user.flip_is_active()
                p_user.on_off.pop(0)
            else:
                p_user.on_off[0] = p_user.on_off[0] - 1

    def create_primary_users(self, num_C):  # creates primary users based on current simulation settings
            for x in range(num_primary_users):
                p_user = PrimaryUser(num_C)
                p_user.place()
                self.primary_users.append(p_user)

    def load_primary_users(self):           # loads a pre generated file of primary users and how they should operate
        # read in primary user
        if dataset == "UMass":
            with open("Primary_Users/" + dataset + "/" + str(puser_round) + "/primary_users_" + str(num_channels) + ".txt", "r") as f:
                lines = f.readlines()
        elif dataset == "Lexington":
            with open("Primary_Users/" + dataset + "/" + str(puser_round) + "/primary_usersLEX_" + str(num_channels) + ".txt", "r") as f:
                lines = f.readlines()
        # read in on off times
        with open("Primary_Users/" + dataset + "/" + str(puser_round) + "/on_off_times.txt", "r") as f:
            on_off = f.readlines()

            # create primary user
            for line_ind in range(num_primary_users):
                # get location, band, and channel
                line_arr = lines[line_ind].strip().split()
                p_user = PrimaryUser()
                p_user.set(float(line_arr[0]), float(line_arr[1]), int(line_arr[2]), int(line_arr[3]))
                # store on/off times
                on_off_line = on_off[line_ind].strip().split()
                on_off_ints = []
                for ele in on_off_line:
                    on_off_ints.append(int(ele))

                p_user.on_off = on_off_ints


                self.primary_users.append(p_user)

    def fill_network(self, num_nodes):  # quickly fill network and randomly place nodes for testing purposes
        for i in range(num_nodes):  # create and add nodes to network
            ide = str(i)
            node = Node(ide)
            node.load_pkl()
            self.add_node(node)


    def find_avg_energy_consumption(self, time):    # keep track of energy usage during simulation
        total_energy = 0
        num_packets_delivered = 0

        for node in self.nodes:
            total_energy += node.energy
            num_packets_delivered += len(node.delivered)

        # avg_energy = total_energy / (V +NoOfDataCenters + NoOfSources)


        f = open(path_to_metrics + consumed_energy_file, 'a')
        f.write(str(time) + "\t" + str(total_energy) + "\t" + str(num_packets_delivered) + "\n")
        f.close()

    def get_message_info(self, path_lines, spec_lines, src, des, t, size): # finds a msg's predetermined path (xchants only)
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


    def messages_delivered(self): # creates a file of all delivered packets and their meta data so metrics can be calculated

        with open(generated_messages_file, "r") as f:
            msg_lines = f.readlines()[1:]

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

    def save_packets_per_tau(self):     # creates file for metrics
        with open(path_to_metrics + "packets_per_tau.txt", "w") as f:
            f.write("T\tPacket per tau\tTransmissions per tau\n")
            for i in range(T):
                f.write(str(i) + "\t" + str(self.packets_per_tau_list[i]) + "\t" + str(self.parallel_coms_list[i]) + "\n")



    def other_add_messages(self, lines, time): # adds msgs to network that are generated at the current time
        for line in lines:
            line_arr = line.strip().split()

            if int(line_arr[5]) == time:
                num_packets = math.ceil(int(line_arr[4]) / int(packet_size))


                for j in range(num_packets):
                    new_mes = Message(line_arr[0], line_arr[1], line_arr[2], line_arr[5], line_arr[4], [0, 0, 0, 0], -1, -1, 0, j, 0)
                    new_mes.create_copies(num_replicas)
                    src = int(line_arr[1])
                    self.nodes[src].buf.append(new_mes)

    def not_delivered_messages(self):   # creates file for metrics of packets that are in the network that haven't been delivered
        f = open(path_to_metrics + not_delivered_file, "a")
        for node in self.nodes:
            for mes in node.buf:
                line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(mes.last_sent) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t" + str(mes.curr) + "\t" + str(mes.packet_id) +"\n"
                f.write(line)
        f.close()

    def find_delay(self, size, s, specBW, i, j, t): # finds delay of a packet based on size and bandwidth
        bw = specBW[int(i), int(j), int(s), int(t)]
        return size / bw

    def xchant_add_messages(self, msg_lines, t, path_lines, spec_lines): # adds msgs to network, xchants only

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

    def clear_old_msgs(self, t):                    # clears msgs that have expired their TTL
        f = open(path_to_metrics + not_delivered_file, "a")

        for node in self.nodes:
            for mes in node.buf:
                if t - mes.genT > TTL:
                    # print("MSG:", mes.ID, "curr:", mes.curr, "t:", t, "TTL expired")
                    line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(
                        mes.last_sent) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t" + str(
                        mes.curr) + "\t" + str(mes.packet_id) + "\n"
                    f.write(line)
                    node.buf.remove(mes)

        f.close()

    def get_node_fwd_priority(self, nodes_in_range, msg, t): # finds which nodes should be prioritized in geographic routing
        if len(nodes_in_range) == 0:
            return -1

        des_node = self.nodes[msg.des]
        nodes_moving_toward_dst = []
        nodes_moving_away_dst = []
        node_priority_list = []

        if t == 0:
            tp = 0
        else:
            tp = t - 1

        # check each node in range to see their distance from the destination and if they are moving closer or farther from it
        for node in nodes_in_range:
            node_currX = float(node.coord[t][0])
            node_currY = float(node.coord[t][1])
            node_prevX = float(node.coord[tp][0])
            node_prevY = float(node.coord[tp][1])
            des_nodeX = float(des_node.coord[t][0])
            des_nodeY = float(des_node.coord[t][1])

            curr_dist = find_distance(node_currX, node_currY, des_nodeX, des_nodeY)
            prev_dist = find_distance(node_prevX, node_prevY, des_nodeX, des_nodeY)

            if prev_dist - curr_dist >= 0:
                nodes_moving_toward_dst.append([node, curr_dist])
            else:
                nodes_moving_away_dst.append([node, curr_dist])

        # create final node priority list based on who is closest and moving towards the destination and then who is closest
        # and moving away from the destination
        while(len(nodes_moving_toward_dst) > 0):
            node_dist_arr = find_node_closest_to_dst(nodes_moving_toward_dst)
            node_priority_list.append(node_dist_arr[0])
            nodes_moving_toward_dst.remove(node_dist_arr)

        while (len(nodes_moving_away_dst) > 0):
            node_dist_arr = find_node_closest_to_dst(nodes_moving_away_dst)
            node_priority_list.append(node_dist_arr[0])
            nodes_moving_away_dst.remove(node_dist_arr)


        return node_priority_list


    def network_GO(self, t, specBW, path_lines, spec_lines, msg_lines, LINK_EXISTS):  # function that sends all messages at a given tau
        # clear all channels
        self.clear_all_channels()
        # activate/deactivate primary users
        self.activate_primary_users()
        # clear out old msgs that are past TTL
        self.clear_old_msgs(t)
        #Calculate energy consumption
        if t % metric_interval == 0 or t == T - 1:
            self.find_avg_energy_consumption(t)


        #Handle different protocols
        # XCHANT protocol/code is outdated for current implementation. works for 5D link exists, now we have 4D link exists
        # and the concept of packets instead of messages.
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

        # handles optimistic/pessimistic geo and epidemic along with single band epidemic
        elif "Epidemic_Smart" in protocol:
            # add messages to source nodes
            self.other_add_messages(msg_lines, t)
            # variables for checking how many packets are sent per tau and # of parallel communications
            self.packets_per_tau = 0
            self.parallel_coms = 0

           # loop over each node
            for node in self.nodes:
                # flag to see if a node transmitted to calculate # of parallel communications
                did_node_transmit = False
                # init band based on smart setting
                if smart_setting == "optimistic" or smart_setting == "pessimistic":
                    # chooses spectrum and returns nodes in range for optimistic or pessimistic approaches
                    s, nodes_in_range = choose_spectrum(node, self, LINK_EXISTS, t)
                # if not optimistic or pessimistic then a single band, epidemic protocol is being used so just find nodes
                # in range of that band
                else:
                    s = S[0]
                    nodes_in_range = find_nodes_in_range(node, self, s, LINK_EXISTS, t)

                # send msgs to destinations first if priority queue is enabled
                if priority_queue == True:
                    # order the msg buffer based on genT and if its in range of des
                    node.order_priority_queue(nodes_in_range)
                    # loop until msg at top of buffer can't be sent to its destination
                    msg_index = 0
                    for i in range(len(node.buf)):
                        # get msg to be sent
                        msg = node.buf[msg_index]
                        # get destination node of msg
                        des_node = self.nodes[int(msg.des)]
                        # check if msg has already reached its destination
                        if to_send(msg, des_node, t) == True:
                            # if not at destination try sending
                            if node.try_sending_message_epi(des_node, msg, t, LINK_EXISTS, specBW, self, s) == False:
                                # if msg can't be sent to destination, then no other nodes in the buffer will be able to
                                # based on how the buffer is ordered in node.order_priority_queue
                                break
                            else:
                                # if msg was sent adjust variables for counting packets per tau and # of parallel communications
                                self.packets_per_tau += 1
                                did_node_transmit = True
                        # if a packet in range of its destination has already been sent to its destination, then increment
                        # the index of the buffer to choose the next msg from
                        else:
                            msg_index += 1
                # continue to flood messages that are not in range of their destinations

                # broadcast message to everyone in range, if there are nodes in range
                if broadcast == True and len(nodes_in_range) > 0:
                    # loop through each msg in buffer
                    for msg in node.buf:
                        # get list of nodes in range that do not currently have the msg that is going to be broadcasted
                        nodes_to_broadcast = []
                        for i in range(len(nodes_in_range)):
                            if to_send(msg, nodes_in_range[i], t) == True:
                                nodes_to_broadcast.append(nodes_in_range[i])
                        # calculate time to transfer the msg based on size and band
                        transfer_time, transfer_time_in_sec = node.compute_transfer_time(msg, s, specBW, msg.curr,
                                                                                         nodes_in_range[0].ID, t)
                        # account for time it takes to send if resources aren't infinite
                        if is_queuing_active == True:
                            node.mes_fwd_time_limit += transfer_time_in_sec

                        # check if there is enough time to broadcast msg
                        if node.mes_fwd_time_limit <= num_sec_per_tau:
                            # broadcast msg to everyone in range
                            msg_sent, num_packet_broadcasted = node.try_broadcasting_message_epi(nodes_to_broadcast, msg, t, LINK_EXISTS, specBW, self, s)
                            # if a msg wasn't sent then subtract the time it would've taken to send
                            if msg_sent == False:
                                node.mes_fwd_time_limit -= transfer_time_in_sec
                            # if msg was sent add the amount of packets sent set flag of a node transmitting to true
                            else:
                                self.packets_per_tau += num_packet_broadcasted
                                did_node_transmit = True
                # if geographical forwarding, and nodes are in range
                elif geographical_routing == True and len(nodes_in_range) > 0: #geographical paradigm
                    # loop through each msg in buffer
                    for msg in node.buf:
                        # get a priority list of nodes that are in range that should get the msg first, if number of nodes
                        # to forward to this is used to see which k nodes will receive the forwarded packet
                        nodes_to_broadcast = []
                        node_priority_list = self.get_node_fwd_priority(nodes_in_range, msg, t)
                        # if there are nodes in range and the best node is not the node that currently is trying to forward it
                        if node_priority_list != -1 and node_priority_list[0] != node:
                            # find the nodes to broadcast to based on how many you are forwarding to
                            node_counter = 0
                            for i in range(len(node_priority_list)):
                                if to_send(msg, node_priority_list[i], t) == True and node_counter < num_nodes_to_fwd:
                                    node_counter += 1
                                    nodes_to_broadcast.append(node_priority_list[i])
                        # find transfer time
                        transfer_time, transfer_time_in_sec = node.compute_transfer_time(msg, s, specBW,
                                                                                         msg.curr,
                                                                                         nodes_in_range[0].ID,
                                                                                         t)
                        # account for time it takes to send if resources aren't infinite
                        if is_queuing_active == True:
                            node.mes_fwd_time_limit += transfer_time_in_sec

                        # check if there is enough time to broadcast msg
                        if node.mes_fwd_time_limit <= num_sec_per_tau:
                            msg_sent, num_packet_broadcasted = node.try_broadcasting_message_epi(nodes_to_broadcast, msg, t, LINK_EXISTS,
                                                                         specBW, self, s)
                            # if msg wasn't broadcasted then give transfer time back to node
                            if msg_sent == False:
                                node.mes_fwd_time_limit -= transfer_time_in_sec
                            # if msg was sent adjust variables for counting packets per tau and # of parallel communications
                            else:
                                self.packets_per_tau += num_packet_broadcasted
                                did_node_transmit = True
                # if node transmitted at least 1 packet account for it in parallel communications
                if did_node_transmit:
                    self.parallel_coms += 1
                    # account for band chosen by this node in this tau
                    self.band_usage[s] += 1
            # keep data for how many packets per tau and parallel coms there were per tau in a list to show change in time
            self.packets_per_tau_list.append(self.packets_per_tau)
            self.parallel_coms_list.append(self.parallel_coms)