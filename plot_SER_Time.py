import numpy as np
import matplotlib.pyplot as plt
from constants import *

time_epochs = 13
runs = 10

msg_files = 33
puser_files = 1

# arrays for broadcast
Epidemic_opt_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_pes_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))

# arrays for geo

Epidemic_opt_PQ1 = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_pes_PQ1 = np.zeros(shape=(time_epochs, msg_files, puser_files))

Epidemic_opt_PQ3 = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_pes_PQ3 = np.zeros(shape=(time_epochs, msg_files, puser_files))

Epidemic_opt_PQ5 = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_pes_PQ5 = np.zeros(shape=(time_epochs, msg_files, puser_files))

num_mules = 50
num_channels = 6
num_Pusers = 100
T = 360
startTime = 1
days = "50"
dataset = "Lexington"
buffer_type = "PQ"
protocols = ["Epidemic_Smart_optimistic", "Epidemic_Smart_pessimistic"]
# protocols = ["Epidemic_Smart_optimistic"]
# fwd_strat = ["geo_3"]
fwd_strat = ["geo_3", "geo_1", "geo_5", "broadcast"]
metrics_file = "metrics.txt"

p_id = 1 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(1, msg_files):
    for j in range(puser_files):
        for strat in fwd_strat:
            for protocol in protocols:
                t = 0
                path = "DataMules/" + dataset + "/" + days + "/1/Link_Exists/LE_" + str(startTime) + \
                       "_" + str(T) + "/" + protocol + "/" + buffer_type + "/" + strat + "/mules_" + \
                       str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                       "/msgfile" + str(i) + "/puserfile" + str(j) + "/"

                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()
                    if int(line_arr[0]) % 5 == 0:
                        if "optimistic" in protocol:
                            if "1" in strat:
                                Epidemic_opt_PQ1[t, i, j] = float(line_arr[p_id])
                            elif "3" in strat:
                                Epidemic_opt_PQ3[t, i, j] = float(line_arr[p_id])
                            elif "5" in strat:
                                Epidemic_opt_PQ5[t, i, j] = float(line_arr[p_id])
                            else:
                                Epidemic_opt_PQ[t, i, j] = float(line_arr[p_id])
                        elif "pessimistic" in protocol:
                            if "1" in strat:
                                Epidemic_pes_PQ1[t, i, j] = float(line_arr[p_id])
                            elif "3" in strat:
                                Epidemic_pes_PQ3[t, i, j] = float(line_arr[p_id])
                            elif "5" in strat:
                                Epidemic_pes_PQ5[t, i, j] = float(line_arr[p_id])
                            else:
                                Epidemic_pes_PQ[t, i, j] = float(line_arr[p_id])

                        t += 1

opt1_mean = []
opt1_sd = []
pes1_mean = []
pes1_sd = []
opt3_mean = []
opt3_sd = []
pes3_mean = []
pes3_sd = []
opt5_mean = []
opt5_sd = []
pes5_mean = []
pes5_sd = []
optB_mean = []
optB_sd = []
pesB_mean = []
pesB_sd = []


opt1_temp = []
pes1_temp = []
opt3_temp = []
pes3_temp = []
opt5_temp = []
pes5_temp = []
optB_temp = []
pesB_temp = []

for t in range(len(Epidemic_opt_PQ3)):
    t_arr_opt1 = []
    t_arr_pes1 = []
    t_arr_opt3 = []
    t_arr_pes3 = []
    t_arr_opt5 = []
    t_arr_pes5 = []
    t_arr_optB = []
    t_arr_pesB = []
    for i in range(len(Epidemic_opt_PQ3[t])):
        for j in range(len(Epidemic_opt_PQ3[t][i])):
            t_arr_opt1.append(Epidemic_opt_PQ1[t,i,j])
            t_arr_pes1.append(Epidemic_pes_PQ1[t,i,j])
            t_arr_opt3.append(Epidemic_opt_PQ3[t,i,j])
            t_arr_pes3.append(Epidemic_pes_PQ3[t,i,j])
            t_arr_opt5.append(Epidemic_opt_PQ5[t,i,j])
            t_arr_pes5.append(Epidemic_pes_PQ5[t,i,j])
            t_arr_optB.append(Epidemic_opt_PQ[t,i,j])
            t_arr_pesB.append(Epidemic_pes_PQ[t,i,j])

    opt1_temp.append(t_arr_opt1)
    pes1_temp.append(t_arr_pes1)
    opt3_temp.append(t_arr_opt3)
    pes3_temp.append(t_arr_pes3)
    opt5_temp.append(t_arr_opt5)
    pes5_temp.append(t_arr_pes5)
    optB_temp.append(t_arr_optB)
    pesB_temp.append(t_arr_pesB)

for i in range(len(opt1_temp)):
    opt1_mean.append(np.mean(opt1_temp[i]))
    pes1_mean.append(np.mean(pes1_temp[i]))
    opt1_sd.append(np.std(opt1_temp[i]))
    pes1_sd.append(np.std(pes1_temp[i]))
    opt3_mean.append(np.mean(opt3_temp[i]))
    pes3_mean.append(np.mean(pes3_temp[i]))
    opt3_sd.append(np.std(opt3_temp[i]))
    pes3_sd.append(np.std(pes3_temp[i]))
    opt5_mean.append(np.mean(opt5_temp[i]))
    pes5_mean.append(np.mean(pes5_temp[i]))
    opt5_sd.append(np.std(opt5_temp[i]))
    pes5_sd.append(np.std(pes5_temp[i]))
    optB_mean.append(np.mean(optB_temp[i]))
    pesB_mean.append(np.mean(pesB_temp[i]))
    optB_sd.append(np.std(optB_temp[i]))
    pesB_sd.append(np.std(pesB_temp[i]))


x = np.array([x for x in range(0, T +1, metric_interval)])
plt.xticks(fontsize=10)
plt.yticks(fontsize=25)
plt.xticks(np.arange(0, T+1, 30))
title_str = "Channels: " + str(num_channels) + "    Primary Users: " + str(num_Pusers)
# title_str = "Broadcast to everyone in range"
plt.title(title_str)
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    plt.ylim(-0.1,1)
    fig_name = "Plots/pdr_Time_SER.png"

if p_id == 2:
    # plt.ylim(-1, 13)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)

    fig_name = "Plots/latency_time_SER.png"

if p_id == 3:
    plt.ylabel('Energy per packet (KJ)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    fig_name = "Plots/energy_time_SER.png"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    # plt.ylim(-1, 20)
    fig_name = "Plots/overhead_Time_SER.png"


plt.errorbar(x, optB_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1, color="red")
plt.errorbar(x, opt1_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1, color ="blue")
plt.errorbar(x, opt3_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1, color="green")
plt.errorbar(x, opt5_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1, color = "black")
plt.errorbar(x, pesB_mean, 0, marker='x', markersize=5, linestyle='--', linewidth=1, color="red")
plt.errorbar(x, pes1_mean, 0, marker='x', markersize=5, linestyle='--', linewidth=1, color ="blue")
plt.errorbar(x, pes3_mean, 0, marker='x', markersize=5, linestyle='--', linewidth=1, color="green")
plt.errorbar(x, pes5_mean, 0, marker='x', markersize=5, linestyle='--', linewidth=1, color = "black")



if p_id == 1:
    plt.legend(["Opt-B","Opt-1","Opt-3","Opt-5", "Pes-B", "Pes-1", "Pes-3", "Pes-5"], loc="lower right", fontsize=12, ncol = 2, frameon=False)
elif p_id == 2:
    plt.legend(["Opt-B","Opt-1","Opt-3","Opt-5", "Pes-B", "Pes-1", "Pes-3", "Pes-5"], loc="lower right", fontsize=12, ncol = 2, frameon=False)
elif p_id ==3:
    plt.legend(["Opt-B","Opt-1","Opt-3","Opt-5", "Pes-B", "Pes-1", "Pes-3", "Pes-5"], loc="lower right", fontsize=12, ncol = 4, frameon=False)
elif p_id ==4:
    plt.legend(["Opt-B","Opt-1","Opt-3","Opt-5", "Pes-B", "Pes-1", "Pes-3", "Pes-5"], loc="lower right", fontsize=15, ncol = 2, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()