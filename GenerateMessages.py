from constants import *
import random

def get_possible_msgs(t, path_lines):
    small_msg = []
    large_msg = []
    for line in path_lines:
        line_arr = line.strip().split()

        if int(line_arr[2]) < t + 5 and int(line_arr[2]) > t - 5 and int(line_arr[0]) < NoOfSources \
                and int(line_arr[1]) < NoOfSources + NoOfDataCenters and int(line_arr[1]) >= NoOfSources \
                and len(line_arr) > 8:


            if int(line_arr[3]) > 600:
                large_msg.append(line)
            else:
                small_msg.append(line)

            path_lines.remove(line)
    return small_msg, large_msg






num_gen = 5


for i in range(num_gen):
    print(i)

    message_file = open("Generated_Messages/generated_messages" + str(i) + ".txt", "w")
    message_file.write("ID\ts\td\tTTL\tsize\tgenT\n")

    with open(path_to_LLC + "LLC_PATH.txt", "r") as fp:
        path_lines = fp.readlines()[1:]
    fp.close()

    min_burst = 5
    max_burst = 15

    min_wait = 2
    max_wait = 13

    t = 0
    msg_count = 0

    while t < 240:
        # print(t)
        num_msg_to_gen = random.randint(min_burst, max_burst)
        time_to_next_burst = random.randint(min_wait, max_wait)

        small, large = get_possible_msgs(t, path_lines)


        for i in range(num_msg_to_gen):

            p = random.randint(0,100)
            generate = False

            if p < 80:
                if len(small) > 0:
                    msg_line = random.choice(small)
                    small.remove(msg_line)
                    generate = True
            else:
                if len(large) > 0:
                    msg_line = random.choice(large)
                    large.remove(msg_line)
                    generate = True

            if generate:
                msg_line_arr = msg_line.strip().split()

                src = int(msg_line_arr[0])
                dst = int(msg_line_arr[1])
                genT = int(msg_line_arr[2])
                size = int(msg_line_arr[3])
                desired_TTL = random.randint(minTTL, TTL)


                line = str(msg_count) + "\t" + str(src) + "\t" + str(dst) + "\t" + str(TTL) + "\t" \
                + str(size) + "\t" + str(t) + "\n"

                message_file.write(line)

                msg_count += 1

        t += time_to_next_burst

    message_file.close()


