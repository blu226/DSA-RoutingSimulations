import numpy as np
import matplotlib.pyplot as plt
from constants import *

time_epochs = 5

msg_files = 50
files = 10
puser_files = 1

# arrays for broadcast
Epidemic_opt_PQ = np.zeros(shape=(time_epochs, files, puser_files))
Epidemic_pes_PQ = np.zeros(shape=(time_epochs, files, puser_files))
bro_opt_PQ = np.zeros(shape=(time_epochs, files, puser_files))
bro_pes_PQ = np.zeros(shape=(time_epochs, files, puser_files))
Epidemic_TV = np.zeros(shape=(time_epochs, files, puser_files))
Epidemic_LTE = np.zeros(shape=(time_epochs, files, puser_files))
Epidemic_CBRS = np.zeros(shape=(time_epochs, files, puser_files))
Epidemic_ISM = np.zeros(shape=(time_epochs, files, puser_files))


num_mules = 30
num_channels = 5
num_Pusers = 250
T = 360
startTime = 1
days = "50"
dataset = "Lexington"
buffer_type = "PQ"
protocols = ["optimistic", "pessimistic", "TV", "LTE", "CBRS", "ISM"]
# protocols = ["Epidemic_Smart_optimistic"]
# fwd_strat = ["geo_3"]
fwd_strat = 3
metrics_file = "metrics.txt"

p_id = 4 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(msg_files):
    for j in range(puser_files):
        for protocol in protocols:
            if i < 10:
                t = 2
            elif i < 20:
                t = 0
            elif i < 30:
                t = 1
            elif i < 40:
                t = 3
            elif i < 50:
                t = 4

            path = "DataMules/" + dataset + "/" + days + "/1/Link_Exists/LE_" + str(startTime) + \
                   "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type + "/geo_" + str(fwd_strat) + "/mules_" + \
                   str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                   "/msgfile" + str(i) + "/puserfile" + str(j) + "/"


            with open(path + metrics_file, "r") as f:
                lines = f.readlines()[1:]

            for line in lines:
                line_arr = line.strip().split()
                if int(line_arr[0]) == 360:
                    if "optimistic" in protocol:
                        Epidemic_opt_PQ[t, i % 10, j] = float(line_arr[p_id])
                    elif "pessimistic" in protocol:
                         Epidemic_pes_PQ[t, i % 10, j] = float(line_arr[p_id])
                    elif "TV" in protocol:
                        Epidemic_TV[t, i % 10, j] = float(line_arr[p_id])
                    elif "LTE" in protocol:
                        Epidemic_LTE[t, i % 10, j] = float(line_arr[p_id])
                    elif "CBRS" in protocol:
                        Epidemic_CBRS[t, i % 10, j] = float(line_arr[p_id])
                    elif "ISM" in protocol:
                        Epidemic_ISM[t, i % 10, j] = float(line_arr[p_id])

for i in range(msg_files):
    for j in range(puser_files):
        for protocol in ["optimistic", "pessimistic"]:
            if i < 10:
                t = 2
            elif i < 20:
                t = 0
            elif i < 30:
                t = 1
            elif i < 40:
                t = 3
            elif i < 50:
                t = 4

            path = "DataMules/" + dataset + "/" + days + "/1/Link_Exists/LE_" + str(startTime) + \
                   "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type + "/broadcast/mules_" + \
                   str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                   "/msgfile" + str(i) + "/puserfile" + str(j) + "/"


            with open(path + metrics_file, "r") as f:
                lines = f.readlines()[1:]

            for line in lines:
                line_arr = line.strip().split()
                if int(line_arr[0]) == 360:
                    if "optimistic" in protocol:
                        bro_opt_PQ[t, i % 10, j] = float(line_arr[p_id])
                    elif "pessimistic" in protocol:
                         bro_pes_PQ[t, i % 10, j] = float(line_arr[p_id])


optB_mean = []
optB_sd = []
pesB_mean = []
pesB_sd = []
optBro_mean = []
optBro_sd = []
pesBro_mean = []
pesBro_sd = []

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
optBro_temp = []
pesBro_temp = []

TV_temp = []
LTE_temp = []
CBRS_temp = []
ISM_temp = []

for t in range(len(Epidemic_opt_PQ)):

    t_arr_optB = []
    t_arr_pesB = []
    t_arr_optBro = []
    t_arr_pesBro = []

    t_arr_tv = []
    t_arr_lte = []
    t_arr_cbrs = []
    t_arr_ism = []
    for i in range(len(Epidemic_opt_PQ[t])):
        for j in range(len(Epidemic_opt_PQ[t][i])):
            t_arr_optB.append(Epidemic_opt_PQ[t,i,j])
            t_arr_pesB.append(Epidemic_pes_PQ[t,i,j])
            t_arr_optBro.append(bro_opt_PQ[t, i, j])
            t_arr_pesBro.append(bro_pes_PQ[t, i, j])
            t_arr_tv.append(Epidemic_TV[t, i, j])
            t_arr_lte.append(Epidemic_LTE[t, i, j])
            t_arr_cbrs.append(Epidemic_CBRS[t, i, j])
            t_arr_ism.append(Epidemic_ISM[t, i, j])


    optB_temp.append(t_arr_optB)
    pesB_temp.append(t_arr_pesB)
    optBro_temp.append(t_arr_optBro)
    pesBro_temp.append(t_arr_pesBro)
    TV_temp.append(t_arr_tv)
    LTE_temp.append(t_arr_lte)
    CBRS_temp.append(t_arr_cbrs)
    ISM_temp.append(t_arr_ism)

for i in range(len(optB_temp)):
    optB_mean.append(np.mean(optB_temp[i]))
    pesB_mean.append(np.mean(pesB_temp[i]))
    optB_sd.append(np.std(optB_temp[i]))
    pesB_sd.append(np.std(pesB_temp[i]))
    optBro_mean.append(np.mean(optBro_temp[i]))
    pesBro_mean.append(np.mean(pesBro_temp[i]))
    optBro_sd.append(np.std(optBro_temp[i]))
    pesBro_sd.append(np.std(pesBro_temp[i]))
    TV_mean.append(np.mean(TV_temp[i]))
    TV_sd.append(np.std(TV_temp[i]))
    LTE_mean.append(np.mean(LTE_temp[i]))
    LTE_sd.append(np.std(LTE_temp[i]))
    CBRS_mean.append(np.mean(CBRS_temp[i]))
    CBRS_sd.append(np.std(CBRS_temp[i]))
    ISM_mean.append(np.mean(ISM_temp[i]))
    ISM_sd.append(np.std(ISM_temp[i]))

print(len(optB_mean))
x = [5, 8, 10, 12, 15]
# x.append(0)
plt.xticks(fontsize=10)
plt.yticks(fontsize=25)
plt.xticks([5, 8, 10, 12, 15])
title_str = "Channels: " + str(num_channels) + "    Primary Users: " + str(num_Pusers)
# title_str = "Broadcast to everyone in range"
# plt.title(title_str)
# plt.xlim(3, 10)

plt.xlim(5,15)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Mean message burst inter-arrival time', fontsize=18)
    plt.ylim(-0.1,1)

    fig_name = "Plots/pdr_msg_SER.png"

if p_id == 2:
    plt.ylim(13, 47)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Mean message burst inter-arrival time', fontsize=18)

    fig_name = "Plots/latency_msg_SER.png"

if p_id == 3:
    plt.ylabel('Energy per packet (J)', fontsize=25)
    plt.xlabel('Mean message burst inter-arrival time', fontsize=18)
    fig_name = "Plots/energy_msg_SER.png"

if p_id == 4:
    # plt.ylim(0, 65)

    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Mean message burst inter-arrival time', fontsize=18)
    # plt.ylim(-1, 20)
    fig_name = "Plots/overhead_msg_SER.png"


# plt.errorbar(x, optB_mean, optB_sd, marker='o', markersize=5, linestyle='-', linewidth=1, color="red")
# plt.errorbar(x, pesB_mean, pesB_sd, marker='o', markersize=5, linestyle='-', linewidth=1, color="blue")
# plt.errorbar(x, optBro_mean, optBro_sd, marker='x', markersize=5, linestyle='-', linewidth=1, color="pink")
# plt.errorbar(x, pesBro_mean, pesBro_sd, marker='x', markersize=5, linestyle='-', linewidth=1, color="cyan")
# plt.errorbar(x, TV_mean, TV_sd, marker='o', markersize=5, linestyle='--', linewidth=1, color="green")
# plt.errorbar(x, LTE_mean, LTE_sd, marker='o', markersize=5, linestyle='--', linewidth=1, color="black")
# plt.errorbar(x, CBRS_mean, CBRS_sd, marker='o', markersize=5, linestyle='--', linewidth=1, color="brown")
# plt.errorbar(x, ISM_mean, ISM_sd, marker='o', markersize=5, linestyle='--', linewidth=1, color="gray")

plt.errorbar(x, optB_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1, color="red")
plt.errorbar(x, pesB_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1, color="blue")
plt.errorbar(x, optBro_mean, 0, marker='x', markersize=5, linestyle='-', linewidth=1, color="pink")
plt.errorbar(x, pesBro_mean, 0, marker='x', markersize=5, linestyle='-', linewidth=1, color="cyan")
plt.errorbar(x, TV_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1, color="green")
plt.errorbar(x, LTE_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1, color="black")
plt.errorbar(x, CBRS_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1, color="brown")
plt.errorbar(x, ISM_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1, color="gray")




if p_id == 1:
    plt.legend(["Geo-opt [3]", "Geo-pes [3]", "SER-opt", "SER-pes", "TV", "LTE", "CBRS", "ISM"], loc="lower right", fontsize=12, ncol = 3, frameon=False)
elif p_id == 2:
    plt.legend(["Geo-opt [3]", "Geo-pes [3]", "SER-opt", "SER-pes", "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=12, ncol = 3, frameon=False)
elif p_id ==3:
    plt.legend(["Geo-opt [3]", "Geo-pes [3]", "SER-opt", "SER-pes", "TV", "LTE", "CBRS", "ISM"], loc="center left", fontsize=12, ncol = 2, frameon=False)
elif p_id ==4:
    plt.legend(["Geo-opt [3]", "Geo-pes [3]", "SER-opt", "SER-pes", "TV", "LTE", "CBRS", "ISM"], loc="upper right", fontsize=12, ncol = 2, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()