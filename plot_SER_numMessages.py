import numpy as np
import matplotlib.pyplot as plt

time_epochs = 6
runs = 1

Epidemic_opt = np.zeros(shape=(time_epochs, runs))
Epidemic_pes = np.zeros(shape=(time_epochs, runs))
Epidemic_rnd = np.zeros(shape=(time_epochs, runs))
Epidemic_opt_PQ = np.zeros(shape=(time_epochs, runs))
Epidemic_pes_PQ = np.zeros(shape=(time_epochs, runs))
Epidemic_rnd_PQ = np.zeros(shape=(time_epochs, runs))

num_mules = 10
num_channels = 6
num_Pusers = 50
T = 180
startTime = 840
num_messages = [x for x in range(25, 151, 25)]
days = ["2007-11-06"]
folder_nums = [x for x in range(1,11, 1)]
buffer_types = ["PQ", "FIFO"]
protocols = ["Epidemic_Smart_optimistic", "Epidemic_Smart_pessimistic", "Epidemic_Smart_random",]
metrics_file = "metrics.txt"

p_id = 1 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(len(days)):
    for protocol in protocols:
        for buffer_type in buffer_types:
            t = 0
            for num_msg in num_messages:

                path = "DataMules/UMass/" + days[i] + "/1/Link_Exists/LE_" + str(startTime) + "_" + str(T) + "/" + protocol + "/" + buffer_type + "/mules_" + str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + "/" + str(num_msg) + "/"
                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()

                    if "180" in line_arr:
                        if "optimistic" in protocol:
                            if buffer_type == "FIFO":
                                Epidemic_opt[t][i] = float(line_arr[p_id])
                            else:
                                Epidemic_opt_PQ[t][i] = float(line_arr[p_id])

                        elif "pessimistic" in protocol:
                            if buffer_type == "FIFO":
                                Epidemic_pes[t][i] = float(line_arr[p_id])
                            else:
                                Epidemic_pes_PQ[t][i] = float(line_arr[p_id])

                        elif "random" in protocol:
                            if buffer_type == "FIFO":
                                Epidemic_rnd[t][i] = float(line_arr[p_id])
                            else:
                                Epidemic_rnd_PQ[t][i] = float(line_arr[p_id])



                t += 1

if p_id == 3:
    for t in range(len(Epidemic_opt)):
        for run in range(runs):
            Epidemic_opt[t][run] = float(Epidemic_opt[t][run]) / 1000
            Epidemic_pes[t][run] = float(Epidemic_pes[t][run]) / 1000
            Epidemic_rnd[t][run] = float(Epidemic_rnd[t][run]) / 1000
            Epidemic_opt_PQ[t][run] = float(Epidemic_opt[t][run]) / 1000
            Epidemic_pes_PQ[t][run] = float(Epidemic_pes[t][run]) / 1000
            Epidemic_rnd_PQ[t][run] = float(Epidemic_rnd[t][run]) / 1000




x = np.array([x for x in range(25, 151, 25)])
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.xticks(np.arange(25, 151, 25))
title_str = "Time: " + str(T) + "    Channels: " + str(num_channels) + "    Primary Users: " + str(num_Pusers)
plt.title(title_str)
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Number of Messages', fontsize=25)
    plt.ylim(-0.05,1.25)
    fig_name = "Plots/pdr_MSGS_SER.eps"

if p_id == 2:
    plt.ylim(-1, 110)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Number of Messages', fontsize=25)

    fig_name = "Plots/latency_MSGS_SER.eps"

if p_id == 3:
    plt.ylabel('Energy expenditure (KJ)', fontsize=25)
    plt.xlabel('Number of Messages', fontsize=25)
    plt.ylim(-0.1, 8)
    fig_name = "Plots/energy_MSGS_SER.eps"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Number of Messages', fontsize=25)
    plt.ylim(-1, 70)
    fig_name = "Plots/overhead_MSGS_SER.eps"

plt.errorbar(x, Epidemic_opt, 0, marker='h', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_pes, 0, marker='p', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_rnd, 0, marker='v', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_opt_PQ, 0, marker='h', markersize=10, linestyle='-', linewidth=3)
plt.errorbar(x, Epidemic_pes_PQ, 0, marker='p', markersize=10, linestyle='-', linewidth=3)
plt.errorbar(x, Epidemic_rnd_PQ, 0, marker='v', markersize=10, linestyle='-', linewidth=3)




if p_id == 1:
    plt.legend(["Optimistic (FIFO)", "Pessimistic (FIFO)", "Random (FIFO)", "Optimistic (PQ)", "Pessimistic (PQ)", "Random (PQ)"], loc="upper right", fontsize=15, ncol = 2, frameon=False)
elif p_id == 2:
    plt.legend(["Optimistic (FIFO)", "Pessimistic (FIFO)", "Random (FIFO)", "Optimistic (PQ)", "Pessimistic (PQ)", "Random (PQ)"], loc="lower right", fontsize=15, ncol = 2, frameon=False)
elif p_id ==3:
    plt.legend(["Optimistic (FIFO)", "Pessimistic (FIFO)", "Random (FIFO)", "Optimistic (PQ)", "Pessimistic (PQ)", "Random (PQ)"], loc="center", fontsize=15, ncol = 2, frameon=False)
elif p_id ==4:
    plt.legend(["Optimistic (FIFO)", "Pessimistic (FIFO)", "Random (FIFO)", "Optimistic (PQ)", "Pessimistic (PQ)", "Random (PQ)"], loc="upper right", fontsize=15, ncol = 2, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()