from constants import *
import random

message_file = open(DataMule_path + "Link_Exists/generated_messages.txt", "w")
message_file.write("ID\ts\td\tTTL\tsize\tgenT\n")

min_burst = 5
max_burst = 20

min_wait = 5
max_wait = 20

t = 0
msg_count = 0

while t < T:
    num_msg_to_gen = random.randint(min_burst, max_burst)
    time_to_next_burst = random.randint(min_wait, max_wait)

    for i in range(num_msg_to_gen):

        src = random.randint(0, NoOfSources - 1)
        dst = random.randint(NoOfSources, NoOfSources + NoOfDataCenters - 1)
        size = random.choice(M)
        TTL = 60

        line = str(msg_count) + "\t" + str(src) + "\t" + str(dst) + "\t" + str(TTL) + "\t" \
        + str(size) + "\t" + str(t) + "\n"

        message_file.write(line)

        msg_count += 1

    t += time_to_next_burst

