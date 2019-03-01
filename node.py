import pickle
import math
import numpy as np
from constants import *
from message import *
from STB_help import *
from misc_sim_funcs import *


class Node(object):
    def __init__(self, name):
        self.ID = name                                                              # Node ID or name (string)
        self.buf = []                                                               # Node message buffer
        self.delivered = []                                                         # packets that have been delivered to self
        self.coord = []                                                             # coordinates at each tau
        self.energy = 0                                                             # energy consumed
        self.buf_size = 0                                                           # current size of buffer
        self.mes_fwd_time_limit = 0                                                 # amount of time spent transmitting in a tau
        self.can_receive = np.inf                                                   # current ID of node you can receive data from in a given tau, inf if any can still
        self.channels = np.full(shape=(len(S), num_channels), fill_value=np.inf)    # matrix of bands and channels in the band

    def handle_buffer_overflow(self, mem_size):     # handle a buffer overflow
        # if the size of the buffer is larger than the mem size and mem size isnt 0 (means infinite buffer)
        if len(self.buf) > mem_size and mem_size > 0:

            if smart_setting != "optimistic" and smart_setting != "pessimistic":
                self.buf.remove(self.buf[0])

            else:
                min_gen_t = T

                # find smallest generation time
                for mes in self.buf:
                    if mes.genT < min_gen_t:
                        min_gen_t = mes.genT

                # find smallest message size packet to delete
                for mes in self.buf:
                    if mes.genT == min_gen_t:
                        self.buf.remove(mes)
                        return
                # Possible code to delete the smallest msg sized packet in buffer
                # for mes in self.buf:
                #     if mes.genT == min_gen_t and mes.size == M[1]:
                #         self.buf.remove(mes)
                #         return
                #
                # for mes in self.buf:
                #     if mes.genT == min_gen_t and mes.size == M[2]:
                #         self.buf.remove(mes)
                #         return
                #
                # for mes in self.buf:
                #     if mes.genT == min_gen_t and mes.size == M[3]:
                #         self.buf.remove(mes)
                #         return

    def update_channel_occupancy(self, node1, node2, ts, net, s, channel, LINK_EXISTS): # update channels being used between 2 nodes
        if ts == T - 1:
            te = ts
        else:
            te = ts + 1
        # ISM does not have channel restrictions
        if s != 1:
            # node 1 is transmitting to node 2, so make it so node2 can only receive msgs from node1 for the remainder of this tau
            node2.can_receive = int(node1.ID)
            # change this channel in node1 to node1's ID so node1 knows it is the only person allowed to transmit on this channel
            node1.channels[s, channel] = int(node1.ID)
            # for every other node in the network, if they are in range with node1 over current band, make sure they know
            # only node1 can transmit on that channel
            for other_node in net.nodes:
                if LINK_EXISTS[int(node1.ID), int(other_node.ID), s, ts] == 1:
                    other_node.channels[s, channel] = int(node1.ID)

    def handle_energy(self, mes, next_node, s, ts, specBW):      # energy handling for xchants
        consumedEnergy = self.calculate_energy_consumption(mes, next_node.ID, s, ts, specBW)
        self.energy += consumedEnergy
        next_node.energy += consumedEnergy

    def order_priority_queue(self, nodes_in_range):         # orders the buffer of a node based on msgs in range of destination
        # get all IDs of nodes in range
        msgs_in_range, msgs_not_in_range = get_msg_lists(nodes_in_range, self)

        # sort msgs based on generation time and combine lists
        new_buf = sort_and_combine_msg_lists(msgs_in_range, msgs_not_in_range)

        # store new buf in node
        self.buf = new_buf

    def check_for_available_channel(self, node1, node2, ts, net, s, LINK_EXISTS): # check if a channel is available between 2 nodes
        available = False
        dist1 = 99999
        dist2 = 99999

        # make sure receiver is not already receiving from anyone else
        if node2.can_receive == np.inf or node2.can_receive == int(node1.ID):
            for j in range(num_channels):
                # check if a common channel is available between both nodes
                if (node1.channels[s][j] == np.inf and node2.channels[s][j] == np.inf) \
                        or (node1.channels[s][j] == int(node1.ID) and node2.channels[s][j] == int(node1.ID)) \
                        or (node1.channels[s][j] == int(node1.ID) and node2.channels[s][j] == np.inf):
                    available = True

                    # interference due to secondary users
                    for other_node in net.nodes:
                        # check to make sure no one in range is transmitting on the same channel
                        if other_node != node1 and other_node != node2 and (other_node.channels[s][j] == other_node.ID ):
                            if LINK_EXISTS[int(node1.ID), int(other_node.ID), s, ts] == 1 or LINK_EXISTS[int(node2.ID), int(other_node.ID), s, ts] == 1:
                                available = False

                    # interference due to primary users
                    for p_user in net.primary_users:
                        if p_user.active == True and s == int(p_user.band) and j == int(p_user.channel):
                            if dataset == "UMass":
                                dist1 = funHaversine(float(node1.coord[ts][1]), float(node1.coord[ts][0]),
                                                     float(p_user.y), float(p_user.x))
                                dist2 = funHaversine(float(node2.coord[ts][1]), float(node2.coord[ts][0]),
                                                     float(p_user.y), float(p_user.x))
                            elif dataset == "Lexington":
                                dist1 = euclideanDistance(float(node1.coord[ts][0]), float(node1.coord[ts][1]),
                                                          float(p_user.x), float(p_user.y))
                                dist2 = euclideanDistance(float(node2.coord[ts][0]), float(node2.coord[ts][1]),
                                                          float(p_user.x), float(p_user.y))
                            if (dist1 < spectRange[s] or dist2 < spectRange[s]):
                                node1.channels[s][j] = -1
                                node2.channels[s][j] = -1
                                available = False
                                # print("Primary User using channel")

                if available == True: # if channel is available then update the network
                    self.update_channel_occupancy(node1,node2,ts,net,s,j, LINK_EXISTS)
                    # return channel index of available channel
                    return j
        # return -1 if no channel available
        return -1

    # same as above but for when a channel has already been decided and you are transmitting to someone new, check if they
    # also have that channel available
    def check_if_channel_available(self, node1, node2, ts, net, s, LINK_EXISTS, channel):
        available = False
        dist1 = 99999
        dist2 = 99999
        j = channel

        # print("Node1.ID:", node1.ID, "Node2.ID:", node2.ID, "Can_receive:", node2.can_receive)
        #make sure receiver is not already receiving from anyone else
        if node2.can_receive == np.inf or node2.can_receive == int(node1.ID):
            #check if a common channel is available between both nodes
            if (node1.channels[s][j] == np.inf and node2.channels[s][j] == np.inf) \
                    or (node1.channels[s][j] == int(node1.ID) and node2.channels[s][j] == int(node1.ID)) \
                    or (node1.channels[s][j] == int(node1.ID) and node2.channels[s][j] == np.inf) \
                    or (node1.channels[s][j] == np.inf and node2.channels[s][j] == int(node1.ID)):
                available = True

                #interference due to secondary users
                for other_node in net.nodes:
                    #no one in range is transmitting on the same channel
                    if other_node != node1 and other_node != node2 and (other_node.channels[s][j] == other_node.ID ):

                        print("Secondary User using same channel.")

                        if LINK_EXISTS[int(node1.ID), int(other_node.ID), s, ts] == 1 or LINK_EXISTS[int(node2.ID), int(other_node.ID), s, ts] == 1:
                            # print("Secondary User in range")
                            available = False

                #interference due to primary users
                for p_user in net.primary_users:
                    if p_user.active == True and s == p_user.band and j == p_user.channel:
                        if dataset == "UMass":
                            dist1 = funHaversine(float(node1.coord[ts][1]), float(node1.coord[ts][0]),
                                                 float(p_user.y), float(p_user.x))
                            dist2 = funHaversine(float(node2.coord[ts][1]), float(node2.coord[ts][0]),
                                                 float(p_user.y), float(p_user.x))
                        elif dataset == "Lexington":
                            dist1 = euclideanDistance(float(node1.coord[ts][0]), float(node1.coord[ts][1]),
                                                      float(p_user.x), float(p_user.y))
                            dist2 = euclideanDistance(float(node2.coord[ts][0]), float(node2.coord[ts][1]),
                                                      float(p_user.x), float(p_user.y))
                        if (dist1 < spectRange[s] or dist2 < spectRange[s]):
                            node1.channels[s][j] = -1
                            node2.channels[s][j] = -1
                            available = False
                            # print("Primary User using channel")

            if available == True:
                self.update_channel_occupancy(node1,node2,ts,net,s,j, LINK_EXISTS)
                return j

        # print("No Channel Available")
        return -1

    def clear_channels(self):   # clears channels at the beginning of a tau
        self.channels = np.full(shape=(len(S), num_channels),fill_value=np.inf)
        self.can_receive = np.inf
        self.mes_fwd_time_limit = 0

    def print_buf(self):        # debugging function
        print(str(self.ID) +  " Buffer ")
        # if len(self.buf) == 0:
        #     print(">>>>>>>>>>>>> No messages")

        for i in range(len(self.buf)):
            message = self.buf[i].ID
            print("Message ID: " + str(message))

    # finds a common channel between 2 nodes in the case of forwarding to destination
    def is_channel_available(self, des_node, s, ts, net, LINK_EXISTS):
        # check if des_node has an open channel
        if (des_node.can_receive == np.inf or des_node.can_receive == int(self.ID)):
            if restrict_channel_access == True:
                channel_available = self.check_for_available_channel(self, des_node, ts, net, s, LINK_EXISTS)
            else:
                channel_available = 0

        else:
            channel_available = -1


        return channel_available

    # quickly check if there exists an open channel on a spectrum
    def is_there_an_open_channel(self, s):

        chan_avail = False
        for chan in range(num_channels):
            if self.channels[s][chan] == np.inf:
                chan_avail = True

        return chan_avail

    # load coordinates of a node from its pickle file
    def load_pkl(self):
        self.coord = pickle.load(open(DataMule_path + pkl_folder + self.ID + ".pkl", "rb"))

    # compute transfer time of sending a msg
    def compute_transfer_time(self, msg, s, specBW, i, j, t):
        # numerator = math.ceil(int(packet_size) / int(specBW[i, j, s, t])) * (t_sd + idle_channel_prob * t_td)
        # time_to_transfer = tau * math.ceil(numerator / tau)
        transmission_time = packet_size / specBW[int(i), int(j), int(s), int(t)]  # in seconds
        time_to_transfer = math.ceil(transmission_time / num_sec_per_tau)  # in tau

        return  time_to_transfer, transmission_time

    # checks if a node has enough time to transfer
    def can_transfer(self, size, s, seconds, specBW, i, j, t):
        time_to_transfer = math.ceil(packet_size / specBW[i, j, s, t])
        if time_to_transfer <= seconds:
            return True
        else:
            return False

    def calculate_energy_consumption(self, message, next, s, ts, specBW):
        curr = int(message.curr)
        size = packet_size
        bw = (specBW[curr, int(next), s, ts])
        sensing_energy = math.ceil(size / bw) * t_sd * sensing_power
        switching_energy = math.ceil(size / (specBW[curr, int(next), int(s), int(ts)])) * idle_channel_prob * switching_delay
        transmission_energy = math.ceil(size / specBW[curr, int(next), int(s), int(ts)]) * idle_channel_prob * t_td * spectPower[s]

        consumedEnergy = sensing_energy + switching_energy + transmission_energy
        consumedEnergy = round(consumedEnergy, 2)

        return consumedEnergy

    # used to send msg to its destination, not technically flooding, but used for priority queue
    def try_sending_message_epi(self, des_node, mes, ts, LINK_EXISTS, specBW, net, s):
        if ts == T - 1:
            return False
        # check if nodes are in range

        if LINK_EXISTS[int(self.ID), int(des_node.ID), s, int(ts)] == 1:
            if debug_message == mes.ID:
                print("in range")
            # Check if des_node has already received a msg from another node and has an available channel in the current tau
            if self.is_channel_available(des_node, s, ts, net, LINK_EXISTS) >= 0:
                # update who the des_node can receive from
                des_node.can_receive = self.ID

                # calculate transfer time
                transfer_time, transfer_time_in_sec = self.compute_transfer_time(mes, s, specBW, mes.curr, des_node.ID, ts)

                # account for time it takes to send if resources aren't infinite
                if limited_time_to_transfer == True:
                    self.mes_fwd_time_limit += transfer_time_in_sec

                # Check if there is enough time to transfer packet
                if self.mes_fwd_time_limit <= num_sec_per_tau:
                    # calculate energy consumed
                    self.handle_energy(mes, des_node, s, ts, specBW)


                    if geographical_routing == True or broadcast == True:
                        if int(des_node.ID) == (mes.des):
                            new_message = Message(mes.ID, mes.src, mes.des, mes.genT, mes.size,
                                                  [mes.band_usage[0], mes.band_usage[1], mes.band_usage[2],
                                                   mes.band_usage[3]], [0],
                                                  [0], 0, mes.packet_id, mes.hops)
                            new_message.set(ts + 1, mes.replica + 1, des_node.ID)
                            new_message.band_used(s)
                            # mes.hops += 1
                            write_delivered_msg_to_file(new_message, mes.last_sent + 1)
                            des_node.delivered.append(new_message)
                            des_node.handle_buffer_overflow(max_packets_in_buffer)

                            #if geographical_routing:
                            self.buf.remove(mes)
                            return True

                        else:
                            print("Try sending message directly to next hop should never be called", des_node.ID, mes.des)
                            # mes.hops += 1
                            # mes.last_sent = ts
                            # mes.curr = des_node.ID
                            # des_node.buf.append(mes)
                            # self.buf.remove(mes)

                    # else:
                    #     # create replica of message
                    #     new_message = Message(mes.ID, mes.src, mes.des, mes.genT, mes.size,
                    #                           [mes.band_usage[0], mes.band_usage[1], mes.band_usage[2], mes.band_usage[3]], [0],
                    #                           [0], 0, mes.packet_id, mes.hops)
                    #     new_message.set(ts + 1, mes.replica + 1, des_node.ID)
                    #     new_message.band_used(s)
                    #     # handle msg if it is being sent to its destination
                    #     if int(des_node.ID) == (mes.des):
                    #         write_delivered_msg_to_file(new_message, new_message.last_sent)
                    #         des_node.delivered.append(new_message)
                    #         # remove msg from buffer if sent to dst
                    #         # self.buf.remove(mes)
                    #
                    #     # handle msg if it is being sent to a relay node
                    #     else:
                    #         print("Try sending message directly to next hop should never be called")
                    #         des_node.buf.append(new_message)

                else:
                    if mes.ID == debug_message:
                        print("out of time")
            else:
                if mes.ID == debug_message:
                    print("no channel")
        else:
            if mes.ID == debug_message:

                print("link DNE from node", self.ID, "to node", des_node.ID, "over s:", s)

        return False

    # attempt to broadcast a msg to everyone sent to this function in "nodes_in_range"
    def try_broadcasting_message_epi(self, nodes_in_range, mes, ts, LINK_EXISTS, specBW, net, s):
        # variable to see if message is sent to any nodes in range
        message_broadcasted = False
        # init channel to use
        channel_to_use = -1
        # variable to keep track of how many packets are sent per tau
        packets_sent = 0

        # try to find an open channel, and if you don't just give up broadcasting message on the chosen band and leave this module
        for next_node in nodes_in_range:
            temp_channel = self.is_channel_available(next_node, s, ts, net, LINK_EXISTS)
            if  temp_channel >= 0:
                channel_to_use = temp_channel
                break

        # try sending msg over found channel to every node in range
        for next_node in nodes_in_range:
             # check if node has the available channel
            channel_available = self.check_if_channel_available(self, next_node, ts, net, s, LINK_EXISTS, channel_to_use)
            # if node has the chosen channel available send him the msg
            if channel_available >= 0 and to_send(mes, next_node, ts) == True and mes in self.buf:
                # msg was broadcasted to at least 1 node
                message_broadcasted = True
                # calculate energy consumed
                consumedEnergy = self.calculate_energy_consumption(mes, next_node.ID, s, ts, specBW)
                next_node.energy += consumedEnergy
                # create replica of message
                new_message = Message(mes.ID, mes.src, mes.des, mes.genT, mes.size,
                                      [mes.band_usage[0], mes.band_usage[1], mes.band_usage[2], mes.band_usage[3]], [0],
                                      [0], 0, mes.packet_id, mes.hops)

                if geographical_routing == True:
                    copies_to_send = math.ceil(mes.num_copies / 2)
                    copies_to_keep = mes.num_copies - copies_to_send
                    new_message.set(ts + 1, copies_to_send, next_node.ID)
                    mes.change_num_copies(copies_to_keep)

                else:
                    new_message.set(ts + 1, mes.replica + 1, next_node.ID)
                new_message.band_used(s)
                packets_sent += 1
                # check if the destination nodes buffer will overflow by receiving this packet, and drop a packet if necessary
                next_node.handle_buffer_overflow(max_packets_in_buffer)
                # handle if msg is sent to destination
                if int(next_node.ID) == (mes.des):
                    write_delivered_msg_to_file(new_message, new_message.last_sent)
                    next_node.delivered.append(new_message)
                    break

                # handle msg if it is being sent to a relay node
                else:
                    # add new msg to destination nodes buffer
                    next_node.buf.append(new_message)
                    # if forwarding and not flooding, delete msg from current nodes buffer after sending

                # if mes in self.buf and num_nodes_to_fwd > 0:
                if mes in self.buf and geographical_routing and mes.num_copies == 0:
                    self.buf.remove(mes)
        # if a msg was broadcasted, handle energy consumed at the sending nodes end
        if(message_broadcasted == True):
            self.energy += consumedEnergy

        return message_broadcasted, packets_sent


    def choose_messages_to_send(self, mesID): # used to implement SnW in xchant
        all_mes_list = []
        mes_to_send = []

        for mes in self.buf:
            if mes.ID == mesID:
                all_mes_list.append(mes)

        num_mess_to_send = int(math.floor(len(all_mes_list)/2))

        for i in range(num_mess_to_send):
            mes_to_send.append(all_mes_list[i])

        return mes_to_send

    def try_sending_message_SnW(self, des_node, mes, ts, LINK_EXISTS, specBW): # xchants only

        if mes.last_sent <= ts:
            max_end = ts + maxTau

            if max_end > T:
                return False

            for te in range(ts + 1, max_end):
                spec_to_use = []

                for s in S:

                    if LINK_EXISTS[int(self.ID), int(des_node.ID), s, int(ts)] == 1:
                        spec_to_use.append(s)

                for spec in range(len(spec_to_use)):
                    if self.can_transfer(packet_size, spec_to_use[spec], (te - ts), specBW, self.ID, des_node.ID, ts):

                        # create list of messages to send
                        mes_to_send = self.choose_messages_to_send(mes.ID)
                        if len(mes_to_send) == 0 and mes.des == des_node.ID:
                            self.buf.remove(mes)
                            mes.set(te, self.ID)
                            des_node.buf.append(mes)

                            # append messages to des buffer and remove from src buffer
                        for message in mes_to_send:
                            # calculate energy consumed
                            if des_node.can_receive == np.inf or des_node.can_receive == message.curr:

                                des_node.can_receive = message.curr
                                transfer_time = self.compute_transfer_time(message, s, specBW, message.curr, des_node.ID, ts)


                                self.mes_fwd_time_limit += transfer_time

                                if self.mes_fwd_time_limit <= num_sec_per_tau:

                                    self.buf.remove(message)
                                    message.set(te, self.ID)
                                    message.band_used(spec_to_use[spec])
                                    des_node.buf.append(message)

                                    consumedEnergy = self.calculate_energy_consumption(message, des_node.ID, s, ts, specBW)
                                    self.energy += consumedEnergy
                                    des_node.energy += consumedEnergy

                                else:
                                    self.mes_fwd_time_limit -= transfer_time
                                    # print("Msg fwd limit reached:", self.mes_fwd_time_limit, "packet ", message.ID)

                        return True

            return False



    def send_message_xchant(self, net, message, ts, specBW, LINK_EXISTS): # xchants only
        nodes = net.nodes

        if len(message.path) > 0 and '' not in message.path:  # if the message still has a valid path
            next = int(message.path[len(message.path) - 1])  # get next node in path

            s = int(message.bands[len(message.bands) - 1])  # get band to use

            # Change s in between 0 and S
            if s > 9:
                s = s % 10
            s = s - 1

            transfer_time, transfer_time_in_secs = self.compute_transfer_time(message, s, specBW, message.curr, next, ts)
            te = ts + transfer_time

            if te >= T:
                te = T - 1

            # and (nodes[next].can_receive == np.inf or nodes[next].can_receive == message.curr)
            if LINK_EXISTS[int(nodes[message.curr].ID), int(nodes[next].ID), s, ts, te] == 1:
                if restrict_channel_access == True:
                    channel_available = self.check_for_available_channel(self, nodes[next], ts, net, s, LINK_EXISTS)
                else:
                    channel_available = True

                if channel_available == True:
                    nodes[next].can_receive = self.ID

                    if limited_time_to_transfer == True:
                        self.mes_fwd_time_limit += transfer_time_in_secs

                    if self.mes_fwd_time_limit <= num_sec_per_tau:
                        # calculate energy consumed
                        consumedEnergy = self.calculate_energy_consumption(message, next, s, ts, specBW)
                        self.energy += consumedEnergy
                        net.nodes[next].energy += consumedEnergy

                        message.path.pop()
                        message.bands.pop()
                        message.last_sent = ts + transfer_time
                        message.band_used(s)

                        self.buf.remove(message)  # remove message from current node buffer
                        self.buf_size -= 1  # update current nodes buffer

                        if message.des == next:
                            #message is delivered, write to file
                            write_delivered_msg_to_file(message, ts)

                        else:
                            # handle message transferred
                            nodes[next].buf.append(message)  # add message to next node buffer
                            message.curr = next  # update messages current node

                        return True

                    else:
                        if message.ID == debug_message:
                            print("Out of time to transfer, node - packetID:",  self.ID, message.packet_id)
                        self.mes_fwd_time_limit -= transfer_time_in_secs
                        return False
                else:
                    if message.ID == debug_message:
                        print("channel unavailable")

            else:
                if message.ID == debug_message:
                    print("out of range, node - packetID:", self.ID, message.packet_id)
                return False

        return False
            #This is to empty the message.path so that the source node knows that the message has been delivered
            # elif int(message.des) == int(next):
            #     message.path.pop()
            #     message.bands.pop()
            #     # message.last_sent += 1


        # This is else to the len(message.path) > 0
        # else:  # Message has been delivered