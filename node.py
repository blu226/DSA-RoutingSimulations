import pickle
import math
import numpy as np
from constants import *
from message import *
from STB_help import *
from misc_sim_funcs import *




class Node(object):                                                                     #Node Object
    def __init__(self, name):
        self.ID = name                                                                #Node ID or name (string)
        self.buf = []                                                                   #Node message buffer
        self.coord = []
        self.energy = 0
        self.buf_size = 0
        self.mes_fwd_time_limit = 0
        self.can_receive = np.inf
        self.channels = np.full(shape=(len(S), num_channels), fill_value=np.inf)

    def update_channel_occupancy(self, node1, node2, ts, net, s, channel, LINK_EXISTS):
        for other_node in net.nodes:
            if LINK_EXISTS[int(node1.ID), int(other_node.ID), s, ts, ts+1] == 1:
                other_node.channels[s, channel] = node1.ID

    def check_for_available_channel(self, node1, node2, ts, net, s, LINK_EXISTS):
        available = False
        dist1 = 99999
        dist2 = 99999

        # print("Node1.ID:", node1.ID, "Node2.ID:", node2.ID, "Can_receive:", node2.can_receive)
        #make sure receiver is not already receiving from anyone else
        if node2.can_receive == np.inf or node2.can_receive == int(node1.ID):
            for j in range(num_channels):

                #check if a common channel is available between both nodes
                if (node1.channels[s][j] == np.inf and node2.channels[s][j] == np.inf) \
                        or (node1.channels[s][j] == int(node1.ID) and node2.channels[s][j] == int(node1.ID)) \
                        or (node1.channels[s][j] == int(node1.ID) and node2.channels[s][j] == np.inf):
                    available = True

                    #interference due to secondary users
                    for other_node in net.nodes:
                        #no one in range is transmitting on the same channel
                        if other_node != node1 and other_node != node2 and (other_node.channels[s][j] == other_node.ID ):

                            # print("Secondary User using same channel.")

                            if LINK_EXISTS[int(node1.ID), int(other_node.ID), s, ts, ts+1] == 1 or LINK_EXISTS[int(node2.ID), int(other_node.ID), s, ts, ts+1] == 1:
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

                    return True

        # print("No Channel Available")
        return False

    def clear_channels(self):
        self.channels = np.full(shape=(len(S), num_channels),fill_value=np.inf)
        self.can_receive = np.inf
        self.mes_fwd_time_limit = 0

    def use_random_channels(self):
        for i in range(len(self.channels)):
            for j in range(len(self.channels[0])):
                p = random.uniform(0, 1)
                if p < active_channel_prob:
                    self.channels[i][j] = -1

    def print_buf(self):
        print(str(self.ID) +  " Buffer ")
        # if len(self.buf) == 0:
        #     print(">>>>>>>>>>>>> No messages")

        for i in range(len(self.buf)):
            message = self.buf[i].ID
            print("Message ID: " + str(message))

    def load_pkl(self):
        self.coord = pickle.load(open(DataMule_path + pkl_folder + self.ID + ".pkl", "rb"))

    def compute_transfer_time(self, msg, s, specBW, i, j, t):
        # numerator = math.ceil(int(packet_size) / int(specBW[i, j, s, t])) * (t_sd + idle_channel_prob * t_td)
        # time_to_transfer = tau * math.ceil(numerator / tau)
        transmission_time = packet_size / specBW[int(i), int(j), int(s), int(t)]  # in seconds
        time_to_transfer = math.ceil(transmission_time / num_sec_per_tau)  # in tau

        return  time_to_transfer, transmission_time

    def can_transfer(self, size, s, seconds, specBW, i, j, t):
        # numerator = math.ceil(int(size) / specBW[int(i), int(j), int(s), int(t)]) * (t_sd + idle_channel_prob * t_td)
        # time_to_transfer = tau * math.ceil(numerator / tau)
        # if msg.ID == 1:
        #     print("Message : ", msg.ID, msg.src, msg.des, " Int: ", i, j)
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

    def try_sending_message_HP(self, des_node, mes, ts, LINK_EXISTS, specBW):

        if mes.last_sent <= ts:
            max_end = ts + maxTau

            if max_end > T:
                max_end = T

            for te in range(ts+1, max_end):
                spec_to_use = []

                for s in S:

                    if LINK_EXISTS[int(self.ID), int(des_node.ID), s, int(ts), int(te)] == 1:
                        spec_to_use.append(s)

                for s in spec_to_use:
                    if self.can_transfer(packet_size, spec_to_use[s], (te - ts), specBW, self.ID, des_node.ID, ts):
                        if des_node.can_receive == np.inf or des_node.can_receive == mes.curr:
                            des_node.can_receive = mes.curr

                            transfer_time = self.compute_transfer_time(mes, s, specBW, mes.curr, des_node.ID, ts)

                            self.mes_fwd_time_limit += transfer_time

                            if self.mes_fwd_time_limit <= num_sec_per_tau:

                               #append messages to des buffer and remove from src buffer
                                self.buf.remove(mes)
                                mes.set(te, self.ID)
                                mes.band_used(spec_to_use[s])
                                des_node.buf.append(mes)
                                # calculate energy consumed
                                consumedEnergy = self.calculate_energy_consumption(mes, next, s, ts, specBW)

                                self.energy += consumedEnergy
                                des_node.energy += consumedEnergy
                                return True

            return False

    def try_sending_message_epi(self, des_node, mes, ts, replicaID, LINK_EXISTS, specBW, net):

        if mes.last_sent <= ts:
            max_end = ts + maxTau

            if max_end > T:
                max_end = T

            for te in range(ts + 1, max_end):
                spec_to_use = []

                for s in S:

                    if LINK_EXISTS[int(self.ID), int(des_node.ID), int(s), int(ts), int(te)] == 1:
                        if restrict_channel_access == True:
                            channel_available = self.check_for_available_channel(self, des_node, ts, net, s,LINK_EXISTS)
                        else:
                            channel_available = True

                        if channel_available == True:
                            spec_to_use.append(s)
                            break

                for spec in range(len(spec_to_use)):

                    if des_node.can_receive == np.inf or des_node.can_receive == mes.curr:
                        des_node.can_receive = self.ID

                        transfer_time, transfer_time_in_sec = self.compute_transfer_time(mes, spec, specBW, mes.curr, des_node.ID, ts)

                        if is_queuing_active == True:
                            self.mes_fwd_time_limit += transfer_time_in_sec

                        if self.mes_fwd_time_limit <= num_sec_per_tau:
                            # calculate energy consumed
                            consumedEnergy = self.calculate_energy_consumption(mes, des_node.ID, spec, ts, specBW)
                            self.energy += consumedEnergy
                            des_node.energy += consumedEnergy

                            if int(des_node.ID) == (mes.des):
                                write_delivered_msg_to_file(mes, te)
                                self.buf.remove(mes)
                            else:
                                new_message = Message(mes.ID, mes.src, mes.des, mes.genT, mes.size, [mes.band_usage[0], mes.band_usage[1], mes.band_usage[2],mes.band_usage[3]],[0],[0], 0, mes.packet_id)
                                new_message.set(te, replicaID, des_node.ID)
                                new_message.band_used(spec_to_use[spec])

                                des_node.buf.append(new_message)

                            return True

                        else:
                            # print("Msg fwd limit reached:", self.mes_fwd_time_limit, "packet ", mes.ID)
                            self.mes_fwd_time_limit -= transfer_time

            return False

    def choose_messages_to_send(self, mesID):
        all_mes_list = []
        mes_to_send = []

        for mes in self.buf:
            if mes.ID == mesID:
                all_mes_list.append(mes)

        num_mess_to_send = int(math.floor(len(all_mes_list)/2))

        for i in range(num_mess_to_send):
            mes_to_send.append(all_mes_list[i])

        return mes_to_send

    def try_sending_message_SnW(self, des_node, mes, ts, LINK_EXISTS, specBW):

        if mes.last_sent <= ts:
            max_end = ts + maxTau

            if max_end > T:
                return False

            for te in range(ts + 1, max_end):
                spec_to_use = []

                for s in S:

                    if LINK_EXISTS[int(self.ID), int(des_node.ID), s, int(ts), int(te)] == 1:
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



    def send_message_xchant(self, net, message, ts, specBW, LINK_EXISTS):
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

                    if is_queuing_active == True:
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