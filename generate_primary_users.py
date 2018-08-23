from STB_help import *



files = findfiles(DataMule_path)

for x in range(num_primary_users):
    chosen_file = random.choice(files)

    with open(DataMule_path + chosen_file, 'r') as f:
        lines = f.readlines()[1:]


    rand_index = random.randint(0, len(lines) - 1)
    line_arr = lines[rand_index].strip().split()

    x = float(line_arr[2])
    y = float(line_arr[3])

    while int(x) == 0:
        rand_index = random.randint(0, len(lines) - 1)
        line_arr = lines[rand_index].strip().split()

        x = float(line_arr[2])
        y = float(line_arr[3])

    band = random.randint(0,len(S) - 1)
    channel = random.randint(0, default_num_channels - 1)

    p_line = str(x) + "\t" + str(y) + "\t" + str(channel) + "\t" + str(band) + "\n"

    f = open("Primary_Users/primary_users.txt", "a")
    f.write(p_line)
    f.close()

for x in range(default_num_channels, 0, -1):
    with open("Primary_Users/primary_users.txt", "r") as f:
        lines = f.readlines()

        f2 = open("Primary_Users/primary_users_" + str(x) + ".txt", "w")

        for line in lines:
            line_arr = line.strip().split()

            if int(line_arr[2]) >= x:
                line_arr[2] = random.randint(0, x - 1)

            new_line = str(line_arr[0]) + "\t" + str(line_arr[1]) + "\t" + str(line_arr[2]) + "\t" + str(line_arr[3]) + "\n"
            f2.write(new_line)

        f2.close()




