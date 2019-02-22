from constants import *
import random
import os

def get_possible_msgs(t, path_lines):
    msgs = []
    for line in path_lines:
        line_arr = line.strip().split()

        if int(line_arr[2]) < t + 5 and int(line_arr[2]) > t - 5 and int(line_arr[0]) < NoOfSources \
                and int(line_arr[1]) < NoOfSources + NoOfDataCenters and int(line_arr[1]) >= NoOfSources \
                and len(line_arr) > 8:

                msgs.append(line)


            # path_lines.remove(line)
    return msgs


num_gen = 5

for i in range(num_gen):
    print(i)


    with open(path_to_LLC + "LLC_PATH.txt", "r") as fp:
        path_lines = fp.readlines()[1:]
    fp.close()

    min_burst = 5
    max_burst = 15

    min_wait = 20
    max_wait = 30

    msg_file_path = "Generated_Messages/mean" + str(int((min_wait + max_wait)/ 2))
    if not os.path.exists(msg_file_path):
        os.makedirs(msg_file_path)
    message_file = open(msg_file_path + "/generated_messages" + str(i) + ".txt", "w")
    message_file.write("ID\ts\td\tTTL\tsize\tgenT\n")

    t = 0
    msg_count = 0

    small_sizes = [60, 600]
    large_sizes = [2400, 3000]

    while t < 240:
        # print(t)
        num_msg_to_gen = random.randint(min_burst, max_burst)
        time_to_next_burst = random.randint(min_wait, max_wait)

        msgs = get_possible_msgs(t, path_lines)


        for i in range(num_msg_to_gen):

            if len(msgs) > 0:
                msg_line = random.choice(msgs)
                msgs.remove(msg_line)
                p = random.randint(0, 100)

                msg_line_arr = msg_line.strip().split()

                src = int(msg_line_arr[0])
                dst = int(msg_line_arr[1])
                genT = int(msg_line_arr[2])
                desired_TTL = random.randint(minTTL, TTL)

                if p < 80:
                    size = random.choice(small_sizes)
                else:
                    size = random.choice(large_sizes)



                line = str(msg_count) + "\t" + str(src) + "\t" + str(dst) + "\t" + str(TTL) + "\t" \
                + str(size) + "\t" + str(t) + "\n"

                message_file.write(line)

                msg_count += 1

        t += time_to_next_burst

    message_file.close()


