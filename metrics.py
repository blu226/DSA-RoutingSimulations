from constants import *
import math

def compute_overhead(time):

    if protocol == "XChant" or protocol == "HotPotato":
        return 1

    with open( DataMule_path + "Link_Exists/" + generated_messages_file, "r") as f:
        generated_lines = f.readlines()[1:num_messages + 1]

    with open(path_to_metrics + packet_delivered_file, 'r') as f:
        delivered_lines = f.readlines()[1:]

    with open(path_to_metrics + not_delivered_file, 'r') as f:
        NotDelivered_lines = f.readlines()[2:]

    total_packets = 0

    num_mes_gen = 0
    num_mes_del = 0
    num_mes_NotDel = 0

    sum_mes_gen = 0
    sum_mes_del = 0
    sum_mes_NotDel = 0

    for line in generated_lines:
        line_arr = line.strip().split()
        if int(line_arr[5]) < time:
            num_packets = math.ceil(int(line_arr[4]) / int(packet_size))
            total_packets += num_packets
            num_mes_gen += 1
            sum_mes_gen += int(line_arr[4])
    for line in delivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) < time:
            num_mes_del += 1
            sum_mes_del += int(line_arr[6])

    for line in NotDelivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) < time:
            num_mes_NotDel += 1
            sum_mes_NotDel += int(line_arr[6])

    if num_mes_gen == 0:
        return 0

    overhead = (num_mes_del + num_mes_NotDel) / total_packets
    overhead_size = (sum_mes_gen + sum_mes_NotDel)/sum_mes_gen

    return round(overhead, 4)

def find_avg_energy(time):

    with open(path_to_metrics + consumed_energy_file, 'r') as f:
        lines = f.readlines()[1:]

    for line in lines:
        line_arr = line.strip().split()
        if (int(line_arr[0]) == int(time) or int(line_arr[0]) == T - 1):
            return round(float(line_arr[1]), 4)

def message_info(mes_list):
    with open(link_exists_folder + generated_messages_file, 'r') as f:
        lines = f.readlines()

    file = open("NOT_delivered.txt", 'w')

    for id in mes_list:
        for line in lines:
            line_arr = line.strip().split()
            if int(id) == int(line_arr[0]):
                file.write(line)
    file.close()

def compute_band_usage(delivery_time, spec_lines):
    band_usage = [0, 0, 0, 0, 0]
    for sLine in spec_lines:
        sLine = sLine.strip().split()
        sLine = [int(obj) for obj in sLine]

        if sLine[2] + sLine[4] <= delivery_time:
            bands_arr = sLine[5:]
            # print(bands_arr)
            for band in bands_arr:
                if int(band) < 5:
                    band_usage[int(band) - 1] += 1
                else:
                    band_usage[4] += int(int(band)/10)
                    band_usage[int(band)%10 - 1] += 1


    total = sum(band_usage)
    if total > 0:
        band_usage = [round(100*ele/total,2) for ele in band_usage]

    print("Band usage: ",  band_usage, "\n")
    return band_usage


def compute_ave_hop_count(t):

    with open(path_to_metrics + packet_delivered_file, 'r') as f:
        delivered_lines = f.readlines()[1:]

    num_msg = 0
    total_hops = 0

    maxhop = 0

    for line in delivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= t:
            num_msg += 1
            total_hops += int(line_arr[8])
            if int(line_arr[8]) > int(maxhop):
                maxhop = line_arr[8]

    if num_msg > 0:
        return round(total_hops / num_msg, 4), num_msg
    else:
        return 0, num_msg

def compute_hop_counts(t):

    with open(path_to_metrics + packet_delivered_file, 'r') as f:
        delivered_lines = f.readlines()[1:]

    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_above4 = 0

    for line in delivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= t:
            if int(line_arr[8]) == 1:
                count_1 += 1
            elif int(line_arr[8]) == 2:
                count_2 += 1
            elif int(line_arr[8]) == 3:
                count_3 += 1
            elif int(line_arr[8]) == 4:
                count_4 += 1
            else:
                count_above4 += 1
    return count_1, count_2, count_3, count_4, count_above4

def compute_metrics(lines, total_messages, delivery_time, spec_lines):
    delivered = 0
    latency = 0
    energy = 0
    mes_IDs = []
    band_usage = [0, 0, 0, 0]

    #all_IDs = [x for x in range(num_messages)]
    unique_messages = []

    for line in lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= delivery_time and int(line_arr[0]) not in mes_IDs:
            delivered += 1
            latency += int(line_arr[5])
            # energy += float(line_arr[7])
            unique_messages.append(line_arr)
            mes_IDs.append(int(line_arr[0]))
            band_usage[0] += int(line_arr[8])
            band_usage[1] += int(line_arr[9])
            band_usage[2] += int(line_arr[10])
            band_usage[3] += int(line_arr[11])

    total = band_usage[0] + band_usage[1] + band_usage[2] + band_usage[3]
    if total > 0:
        band_usage = [ele/ total for ele in band_usage]

    if protocol == "XChant":
        band_usage = compute_band_usage(delivery_time, spec_lines)

    if delivered > 0:
        latency = round(float(latency)/delivered, 4)
        energy = float(energy)/delivered

    if total_messages > 0:
        delivered = round(float(delivered) / total_messages, 4)

    avg_energy = find_avg_energy(delivery_time)

    overhead = compute_overhead(delivery_time)

    avg_hops_per_packet, num_packets = compute_ave_hop_count(delivery_time)

    count_1, count_2, count_3, count_4, count_above4 = compute_hop_counts(delivery_time)

    if num_packets > 0:
        eng = round(avg_energy/num_packets, 4)
    else:
        eng = 0

    print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency, " Overhead: ", overhead, "Energy: ",\
          eng, "AVG hops:", avg_hops_per_packet, "#hops [1,2,3,4,5+]: [", count_1, count_2, count_3, count_4, count_above4, "]")

    return delivered, latency, eng, mes_IDs, unique_messages, overhead, band_usage, avg_hops_per_packet

#Main starts here
total_messages = num_messages

metric_file = open(path_to_metrics + metrics_file, "w")
with open(path_to_metrics + delivered_file, "r") as f:
    lines = f.readlines()[2:]

if protocol == "XChant":
    with open(path_to_LLC + "LLC_Spectrum.txt", "r") as f:
        spec_lines = f.readlines()[1:]
else:
    spec_lines = []


fsorted = open(path_to_metrics + "sorted_delivery.txt", "w")
#sort the lines based on LLC i.e., column 5

fsorted.write("ID	s	d	ts	te	LLC	size	parent	parentTime	replica\n")

lines = sorted(lines, key=lambda line: int(line.split()[5]))

for line in lines:
    fsorted.write(line)
fsorted.close()

delivery_times = [i for i in range(0, T + 10, 15)]

metric_file.write("#t\tPDR\tLatency\tEnergy\Overhead\n")
for t in delivery_times:
    avg_pdr, avg_latency, avg_energy, mes_IDs, unique_messages, overhead, band_usage, hops = compute_metrics(lines, total_messages, t, spec_lines)
    metric_file.write(
        str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) + "\t" + str(overhead) + "\t" + str(hops) + "\t" +
        str(band_usage[0]) + "\t" + str(band_usage[1]) + "\t" + str(band_usage[2]) + "\t" + str(band_usage[3]) + "\n")

metric_file.close()
# print("Delivered messages", sorted(mes_IDs))

with open(path_to_metrics + "unique_messages.txt", "w") as f:
    f.write("ID\ts\td\tts\tte\tLLC\tsize\n")
    f.write("------------------------------\n")

    for msg_line in unique_messages:
        for word in msg_line[:7]:
            f.write(str(word) + "\t")
        f.write("\n")

# message_info(all_IDs)

