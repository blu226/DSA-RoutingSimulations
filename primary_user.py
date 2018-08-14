from STB_help import *

class PrimaryUser(object):

    def __init__(self):
        self.band = random.randint(0, len(S))
        self.channel = random.randint(0, num_channels)
        self.x = -1
        self.y = -1
        self.active = False

    def place(self):
        files = findfiles(DataMule_path)
        chosen_file = random.choice(files)

        with open(DataMule_path + chosen_file, 'r') as f:
            lines = f.readlines()[1:]

        rand_index = random.randint(0, len(lines) - 1)

        line_arr = lines[rand_index].strip().split()

        self.x = float(line_arr[2])
        self.y = float(line_arr[3])