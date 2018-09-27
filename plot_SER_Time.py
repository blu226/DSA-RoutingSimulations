import numpy as np
import matplotlib.pyplot as plt

time_epochs = 7
runs = 1

Epidemic_opt = np.zeros(shape=(time_epochs, runs))
Epidemic_pes = np.zeros(shape=(time_epochs, runs))
Epidemic_rnd = np.zeros(shape=(time_epochs, runs))
Epidemic_opt_PQ = np.zeros(shape=(time_epochs, runs))
Epidemic_pes_PQ = np.zeros(shape=(time_epochs, runs))
Epidemic_rnd_PQ = np.zeros(shape=(time_epochs, runs))

num_mules = 30
num_channels = 10
num_Pusers = 0
T = 180
startTime = 2
num_messages = 15
days = ["30"]
dataset = "Lexington"
folder_nums = [x for x in range(1,11, 1)]
buffer_types = ["PQ", "FIFO"]
protocols = ["Epidemic_Smart_optimistic", "Epidemic_Smart_pessimistic", "Epidemic_Smart_random",]
metrics_file = "metrics.txt"

p_id = 1 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(len(days)):
    for protocol in protocols:
        for buffer_type in buffer_types:
            t = 0

            path = "DataMules/" + dataset + "/" + days[i] + "/1/Link_Exists/LE_" + str(startTime) + "_" + str(T) + "/" + protocol + "/" + buffer_type + "/mules_" + str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + "/" + str(num_messages) + "/"
            with open(path + metrics_file, "r") as f:
                lines = f.readlines()[1:]

            for line in lines:
                line_arr = line.strip().split()
                if int(line_arr[0]) % 10 == 0:
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
            Epidemic_opt_PQ[t][run] = float(Epidemic_opt_PQ[t][run]) / 1000
            Epidemic_pes_PQ[t][run] = float(Epidemic_pes_PQ[t][run]) / 1000
            Epidemic_rnd_PQ[t][run] = float(Epidemic_rnd_PQ[t][run]) / 1000




x = np.array([x for x in range(0, T +1, 30)])
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.xticks(np.arange(0, 181, 30))
# title_str = "Messages: " + str(num_messages) + "    Channels: " + str(num_channels) + "    Primary Users: " + str(num_Pusers)
title_str = "Broadcast to everyone in range"
plt.title(title_str)
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    plt.ylim(-0.05,1.1)
    fig_name = "Plots/pdr_Time_SER.eps"

if p_id == 2:
    plt.ylim(-1, 40)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)

    fig_name = "Plots/latency_time_SER.eps"

if p_id == 3:
    plt.ylabel('Energy expenditure (KJ)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    plt.ylim(-0.01, 0.75)
    fig_name = "Plots/energy_time_SER.eps"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    plt.ylim(-1, 15)
    fig_name = "Plots/overhead_Time_SER.eps"

plt.errorbar(x, Epidemic_opt, 0, marker='h', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_pes, 0, marker='p', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_rnd, 0, marker='v', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_opt_PQ, 0, marker='h', markersize=10, linestyle='-', linewidth=3)
plt.errorbar(x, Epidemic_pes_PQ, 0, marker='p', markersize=10, linestyle='-', linewidth=3)
plt.errorbar(x, Epidemic_rnd_PQ, 0, marker='v', markersize=10, linestyle='-', linewidth=3)

if p_id == 1:
    plt.legend(["Optimistic (FIFO)", "Pessimistic (FIFO)", "Weighted (FIFO)", "Optimistic (PQ)", "Pessimistic (PQ)", "Weighted (PQ)"], loc="upper left", fontsize=15, ncol = 1, frameon=False)
elif p_id == 2:
    plt.legend(["Optimistic (FIFO)", "Pessimistic (FIFO)", "Weighted (FIFO)", "Optimistic (PQ)", "Pessimistic (PQ)", "Weighted (PQ)"], loc="upper left", fontsize=15, ncol = 1, frameon=False)
elif p_id ==3:
    plt.legend(["Optimistic (FIFO)", "Pessimistic (FIFO)", "Weighted (FIFO)", "Optimistic (PQ)", "Pessimistic (PQ)", "Weighted (PQ)"], loc="upper left", fontsize=15, ncol = 1, frameon=False)
elif p_id ==4:
    plt.legend(["Optimistic (FIFO)", "Pessimistic (FIFO)", "Weighted (FIFO)", "Optimistic (PQ)", "Pessimistic (PQ)", "Weighted (PQ)"], loc="upper left", fontsize=15, ncol = 1, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()