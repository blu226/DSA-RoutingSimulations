import numpy as np
import matplotlib.pyplot as plt
from constants import *

time_epochs = 5

msg_files = 5
puser_files = 1

# arrays for broadcast
# arrays for broadcast
Epidemic_opt_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_pes_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_wei_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
bro_opt_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
bro_pes_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
bro_wei_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_TV = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_LTE = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_CBRS = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_ISM = np.zeros(shape=(time_epochs, msg_files, puser_files))

num_mules = 92
# num_channels = 5
num_Pusers = 200
msg_mean = 15
T = 360
channels = 6
ttl = 180
max_memory = [25, 50, 100, 150, 200]
startTime = 1
days = "50"
dataset = "Lexington"
buffer_type = ["PQ", "FIFO"]
protocols = ["optimistic", "pessimistic", "weighted"]
# protocols = ["Epidemic_Smart_optimistic"]
# fwd_strat = ["geo_3"]
num_replicas = 1
metrics_file = "metrics.txt"
sim_round = 5

p_id = 4 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(msg_files):
    for j in range(puser_files):
        for mem_size in max_memory:
            for protocol in protocols:
                t = max_memory.index(mem_size)

                path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(startTime) + \
                       "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[0] + "/geo_" + str(num_replicas) + "/mules_" + \
                       str(num_mules) + "/channels_" + str(channels) + "/P_users_" + str(num_Pusers) + \
                       "/msgfile_" + str(i) + "_" + str(msg_mean)+ "/puserfile_" + str(j) + "/TTL_" + str(ttl) + "/BuffSize_" + str(mem_size) + "/"


                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()
                    if int(line_arr[0]) == 360:
                        if "optimistic" in protocol:
                            Epidemic_opt_PQ[t, i, j] = float(line_arr[p_id])
                        elif "pessimistic" in protocol:
                             Epidemic_pes_PQ[t, i, j] = float(line_arr[p_id])
                        elif "weighted" in protocol:
                             Epidemic_wei_PQ[t, i, j] = float(line_arr[p_id])

#For broadcast
for i in range(msg_files):
    for j in range(puser_files):
        for mem_size in max_memory:
            for protocol in ["optimistic", "pessimistic", "weighted", "TV", "LTE", "CBRS", "ISM"]:
                t = max_memory.index(mem_size)

                if protocol in ["optimistic", "pessimistic", "weighted"]:
                    path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(
                        startTime) + \
                           "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[0] + "/broadcast/mules_" + \
                           str(num_mules) + "/channels_" + str(channels) + "/P_users_" + str(num_Pusers) + \
                           "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(
                        ttl) + "/BuffSize_" + str(mem_size) + "/"

                else:
                    path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(
                        startTime) + \
                           "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[1] + "/broadcast/mules_" + \
                           str(num_mules) + "/channels_" + str(channels) + "/P_users_" + str(num_Pusers) + \
                           "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(
                        ttl) + "/BuffSize_" + str(mem_size) + "/"


                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()
                    if int(line_arr[0]) == 360:
                        if "optimistic" in protocol:
                            bro_opt_PQ[t, i, j] = float(line_arr[p_id])
                        elif "pessimistic" in protocol:
                             bro_pes_PQ[t, i, j] = float(line_arr[p_id])
                        elif "weighted" in protocol:
                             bro_wei_PQ[t, i, j] = float(line_arr[p_id])
                        elif "TV" in protocol:
                            Epidemic_TV[t, i, j] = float(line_arr[p_id])
                        elif "LTE" in protocol:
                            Epidemic_LTE[t, i, j] = float(line_arr[p_id])
                        elif "CBRS" in protocol:
                            Epidemic_CBRS[t, i, j] = float(line_arr[p_id])
                        elif "ISM" in protocol:
                            Epidemic_ISM[t, i, j] = float(line_arr[p_id])

optB_mean = []
optB_sd = []
pesB_mean = []
pesB_sd = []
weiB_mean = []
weiB_sd = []
optBro_mean = []
optBro_sd = []
pesBro_mean = []
pesBro_sd = []
weiBro_mean = []
weiBro_sd = []

TV_mean = []
TV_sd = []
LTE_mean = []
LTE_sd = []
CBRS_mean = []
CBRS_sd = []
ISM_mean = []
ISM_sd = []

optB_temp = []
pesB_temp = []
weiB_temp = []
optBro_temp = []
pesBro_temp = []
weiBro_temp = []

TV_temp = []
LTE_temp = []
CBRS_temp = []
ISM_temp = []

for t in range(len(Epidemic_opt_PQ)):

    t_arr_optB = []
    t_arr_pesB = []
    t_arr_weiB = []
    t_arr_optBro = []
    t_arr_pesBro = []
    t_arr_weiBro = []

    t_arr_tv = []
    t_arr_lte = []
    t_arr_cbrs = []
    t_arr_ism = []
    for i in range(len(Epidemic_opt_PQ[t])):
        for j in range(len(Epidemic_opt_PQ[t][i])):
            t_arr_optB.append(Epidemic_opt_PQ[t, i, j])
            t_arr_pesB.append(Epidemic_pes_PQ[t, i, j])
            t_arr_weiB.append(Epidemic_wei_PQ[t, i, j])
            t_arr_optBro.append(bro_opt_PQ[t, i, j])
            t_arr_pesBro.append(bro_pes_PQ[t, i, j])
            t_arr_weiBro.append(bro_wei_PQ[t, i, j])
            t_arr_tv.append(Epidemic_TV[t, i, j])
            t_arr_lte.append(Epidemic_LTE[t, i, j])
            t_arr_cbrs.append(Epidemic_CBRS[t, i, j])
            t_arr_ism.append(Epidemic_ISM[t, i, j])

    optB_temp.append(t_arr_optB)
    pesB_temp.append(t_arr_pesB)
    weiB_temp.append(t_arr_weiB)
    optBro_temp.append(t_arr_optBro)
    pesBro_temp.append(t_arr_pesBro)
    weiBro_temp.append(t_arr_weiBro)
    TV_temp.append(t_arr_tv)
    LTE_temp.append(t_arr_lte)
    CBRS_temp.append(t_arr_cbrs)
    ISM_temp.append(t_arr_ism)

for i in range(len(optB_temp)):
    optB_mean.append(np.mean(optB_temp[i]))
    pesB_mean.append(np.mean(pesB_temp[i]))
    weiB_mean.append(np.mean(weiB_temp[i]))
    optB_sd.append(np.std(optB_temp[i]))
    pesB_sd.append(np.std(pesB_temp[i]))
    weiB_sd.append(np.std(weiB_temp[i]))
    optBro_mean.append(np.mean(optBro_temp[i]))
    pesBro_mean.append(np.mean(pesBro_temp[i]))
    weiBro_mean.append(np.mean(weiBro_temp[i]))
    optBro_sd.append(np.std(optBro_temp[i]))
    pesBro_sd.append(np.std(pesBro_temp[i]))
    weiBro_sd.append(np.std(weiBro_temp[i]))
    TV_mean.append(np.mean(TV_temp[i]))
    TV_sd.append(np.std(TV_temp[i]))
    LTE_mean.append(np.mean(LTE_temp[i]))
    LTE_sd.append(np.std(LTE_temp[i]))
    CBRS_mean.append(np.mean(CBRS_temp[i]))
    CBRS_sd.append(np.std(CBRS_temp[i]))
    ISM_mean.append(np.mean(ISM_temp[i]))
    ISM_sd.append(np.std(ISM_temp[i]))

print(len(optB_mean))
x = max_memory
# x.append(0)
plt.xticks(fontsize=10)
plt.yticks(fontsize=25)
plt.xticks(max_memory)
# title_str = "Broadcast to everyone in range"
# plt.title(title_str)

# plt.xlim(0,12)
fig_name = "dummy.eps"
plt.xlabel('Max buffer size', fontsize=25)

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.ylim(-0.1,1)

    fig_name = "Plots/pdr_mem_SER.png"

if p_id == 2:
    plt.ylim(0, 150)
    plt.ylabel('Network delay (min)', fontsize=25)
    fig_name = "Plots/latency_mem_SER.png"

if p_id == 3:

    plt.ylabel('Energy per packet (kJ)', fontsize=25)
    fig_name = "Plots/energy_mem_SER.png"

if p_id == 4:
    # plt.ylim(0, 65)

    plt.ylabel('Message overhead', fontsize=25)
    # plt.ylim(-1, 20)
    fig_name = "Plots/overhead_mem_SER.png"


# plt.errorbar(x, optB_mean, optB_sd, marker='o', markersize=5, linestyle='-', linewidth=1, color="red")
# plt.errorbar(x, pesB_mean, pesB_sd, marker='o', markersize=5, linestyle='-', linewidth=1, color="blue")
# plt.errorbar(x, optBro_mean, optBro_sd, marker='x', markersize=5, linestyle='-', linewidth=1, color="pink")
# plt.errorbar(x, pesBro_mean, pesBro_sd, marker='x', markersize=5, linestyle='-', linewidth=1, color="cyan")
# plt.errorbar(x, TV_mean, TV_sd, marker='o', markersize=5, linestyle='--', linewidth=1, color="green")
# plt.errorbar(x, LTE_mean, LTE_sd, marker='o', markersize=5, linestyle='--', linewidth=1, color="black")
# plt.errorbar(x, CBRS_mean, CBRS_sd, marker='o', markersize=5, linestyle='--', linewidth=1, color="brown")
# plt.errorbar(x, ISM_mean, ISM_sd, marker='o', markersize=5, linestyle='--', linewidth=1, color="gray")

if p_id == 3:
    plt.errorbar(x, [y/1000 for y in optB_mean], 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in pesB_mean], 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in weiB_mean], 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in optBro_mean], 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in pesBro_mean], 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in weiBro_mean], 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in TV_mean], 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, [y/1000 for y in LTE_mean], 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, [y/1000 for y in CBRS_mean], 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, [y/1000 for y in ISM_mean], 0, marker='o', markersize=5, linestyle='--', linewidth=1)

else:
    plt.errorbar(x, optB_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, pesB_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, weiB_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, optBro_mean, 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, pesBro_mean, 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, weiBro_mean, 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, TV_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, LTE_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, CBRS_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, ISM_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1)


if p_id == 1:
    plt.legend(["Geo-opt", "Geo-pes", "Geo-wei", "SER-opt", "SER-pes", "SER-wei", "TV", "LTE", "CBRS", "ISM"], loc="lower left", fontsize=10, ncol = 4, frameon=False)

elif p_id == 2:
    plt.legend(["Geo-opt", "Geo-pes", "Geo-wei", "SER-opt", "SER-pes", "SER-wei",  "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 4, frameon=False)
elif p_id ==3:
    plt.legend(["Geo-opt", "Geo-pes", "Geo-wei", "SER-opt", "SER-pes", "SER-wei",  "TV", "LTE", "CBRS", "ISM"], loc="upper right", fontsize=10, ncol = 4, frameon=False)
elif p_id ==4:
    plt.legend(["Geo-opt", "Geo-pes", "Geo-wei", "SER-opt", "SER-pes", "SER-wei", "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 4, frameon=False)

plt.tight_layout()
plt.savefig(fig_name)

plt.show()