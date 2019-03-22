import numpy as np
import matplotlib.pyplot as plt
from constants import *

time_epochs = 5

msg_files = 5
puser_files = 5

# arrays for broadcast
geo_opt = np.zeros(shape=(time_epochs, msg_files, puser_files))
geo_pes = np.zeros(shape=(time_epochs, msg_files, puser_files))
geo_wei = np.zeros(shape=(time_epochs, msg_files, puser_files))

bro_opt_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
bro_pes_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
bro_wei_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))

Epidemic_TV = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_LTE = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_CBRS = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_ISM = np.zeros(shape=(time_epochs, msg_files, puser_files))



#num_mules = [8, 16, 32, 48, 64]
num_mules = [16, 32, 64, 92, 128]
num_channels = 6
num_Pusers = 200
msg_mean = 15
ttl = 180
max_mem = 100
T = 360
startTime = 1
days = "50"
dataset = "Lexington"
buffer_type = ["FIFO", "FIFO"]
protocols = ["optimistic", "pessimistic", "weighted", "TV", "LTE", "CBRS", "ISM"]
# protocols = ["Epidemic_Smart_optimistic"]
# fwd_strat = ["geo_3"]
num_replicas = 5
metrics_file = "metrics.txt"
sim_round = 6

p_id = 1 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(msg_files):
    for j in range(puser_files):
        for mules in num_mules:
            for protocol in ["optimistic", "pessimistic", "weighted"]:
                t = num_mules.index(mules)


                # if fwd_strat > 0:
                path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(startTime) + \
                       "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[0] + "/geo_" + str(num_replicas) + "/mules_" + \
                       str(mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                       "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(ttl) + "/BuffSize_" + str(max_mem) + "/"
                # else:
                #     path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(startTime) + \
                #            "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type + "/broadcast/mules_" + \
                #            str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                #            "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(ttl) + "/BuffSize_" + str(max_mem) + "/"

                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()
                    if int(line_arr[0]) == 360:
                        if "optimistic" in protocol:
                            geo_opt[t, i, j] = float(line_arr[p_id])
                        elif "pessimistic" in protocol:
                             geo_pes[t, i, j] = float(line_arr[p_id])
                        elif "weighted" in protocol:
                             geo_wei[t, i, j] = float(line_arr[p_id])
                        # elif "TV" in protocol:
                        #     Epidemic_TV[t, i, j] = float(line_arr[p_id])
                        # elif "LTE" in protocol:
                        #     Epidemic_LTE[t, i, j] = float(line_arr[p_id])
                        # elif "CBRS" in protocol:
                        #     Epidemic_CBRS[t, i, j] = float(line_arr[p_id])
                        # elif "ISM" in protocol:
                        #     Epidemic_ISM[t, i, j] = float(line_arr[p_id])

for i in range(msg_files):
    for j in range(puser_files):
        for mules in num_mules:
            for protocol in ["optimistic", "pessimistic", "weighted", "TV", "LTE", "CBRS", "ISM"]:
                t = num_mules.index(mules)

                if protocol in ["optimistic", "pessimistic", "weighted"]:
                    path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(startTime) + \
                           "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[0] + "/broadcast/mules_" + \
                           str(mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                           "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(ttl) + "/BuffSize_" + str(max_mem) + "/"

                else:
                    path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(
                        startTime) + \
                           "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[1] + "/broadcast/mules_" + \
                           str(mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                           "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(
                        ttl) + "/BuffSize_" + str(max_mem) + "/"

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


for t in range(len(geo_opt)):
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
    for i in range(len(geo_opt[t])):
        for j in range(len(geo_opt[t][i])):
            t_arr_optB.append(geo_opt[t,i,j])
            t_arr_pesB.append(geo_pes[t,i,j])
            t_arr_weiB.append(geo_wei[t,i,j])
            
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

x = num_mules
# x.append(0)
plt.xticks(fontsize=10)
plt.yticks(fontsize=25)
plt.xticks(num_mules)

fig_name = "dummy.eps"
plt.xlabel('# Datamules', fontsize=25)

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.ylim(-0.1,1)

    fig_name = "Plots/pdr_nodes_SER.eps"

if p_id == 2:
    plt.ylim(0,145)
    plt.ylabel('Network delay (min)', fontsize=25)
    fig_name = "Plots/latency_nodes_SER.eps"

if p_id == 3:
    plt.ylabel('Energy per packet (kJ)', fontsize=25)
    fig_name = "Plots/energy_nodes_SER.eps"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    fig_name = "Plots/overhead_nodes_SER.eps"

if p_id == 3:
    plt.errorbar(x, [y/1000 for y in optB_mean], 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in pesB_mean], 0, marker='x', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, [y/1000 for y in weiB_mean], 0, marker='d', markersize=5, linestyle='-.', linewidth=1)
    plt.errorbar(x, [y/1000 for y in optBro_mean], 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in pesBro_mean], 0, marker='x', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, [y/1000 for y in weiBro_mean], 0, marker='d', markersize=5, linestyle='-.', linewidth=1)
    plt.errorbar(x, [y/1000 for y in TV_mean], 0, marker='*', markersize=5, linestyle=':', linewidth=1)
    plt.errorbar(x, [y/1000 for y in LTE_mean], 0, marker='*', markersize=5, linestyle=':', linewidth=1)
    plt.errorbar(x, [y/1000 for y in CBRS_mean], 0, marker='*', markersize=5, linestyle=':', linewidth=1)
    plt.errorbar(x, [y/1000 for y in ISM_mean], 0, marker='*', markersize=5, linestyle=':', linewidth=1)

else: 
    plt.errorbar(x, optB_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, pesB_mean, 0, marker='x', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, weiB_mean, 0, marker='d', markersize=5, linestyle='-.', linewidth=1)
    plt.errorbar(x, optBro_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, pesBro_mean, 0, marker='x', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, weiBro_mean, 0, marker='d', markersize=5, linestyle='-.', linewidth=1)
    plt.errorbar(x, TV_mean, 0, marker='*', markersize=5, linestyle=':', linewidth=1)
    plt.errorbar(x, LTE_mean, 0, marker='*', markersize=5, linestyle=':', linewidth=1)
    plt.errorbar(x, CBRS_mean, 0, marker='*', markersize=5, linestyle=':', linewidth=1)
    plt.errorbar(x, ISM_mean, 0, marker='*', markersize=5, linestyle=':', linewidth=1)

if p_id == 1:
    plt.legend(["Geo-opt(5)", "Geo-pes(5)", "Geo-wei(5)", "SER-opt", "SER-pes", "SER_wei", "TV", "LTE", "CBRS", "ISM"], loc="lower right", fontsize=10, ncol = 4, frameon=False)
elif p_id == 2:
    plt.legend(["Geo-opt(5)", "Geo-pes(5)", "Geo-wei(5)", "SER-opt", "SER-pes", "SER_wei", "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 4, frameon=False)
elif p_id ==3:
    plt.legend(["Geo-opt(5))", "Geo-pes(5)", "Geo-wei(5)", "SER-opt(5)", "SER-pes", "SER_wei", "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 4, frameon=False)
elif p_id ==4:
    plt.legend(["Geo-opt(5)", "Geo-pes(5)", "Geo-wei(5)", "SER-opt(5)", "SER-pes", "SER_wei", "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 4, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()