class Message(object):                                                                          #Message Object
    def __init__(self, ID, src, des, genT, size, prev_bands_used, bands, path, replica):
        self.ID = int(ID)
        self.src = int(src)
        self.des = int(des)
        self.genT = int(genT)
        self.size = int(size)
        self.band_usage = prev_bands_used
        self.bands = bands
        self.path = path
        self.curr = int(src)
        self.last_sent = -1
        self.totalEnergy = 0
        self.replica = replica


    def set(self, lastSent, rep):
        self.last_sent = lastSent
        self.replica = rep

    def band_used(self, s):
        self.band_usage[s] += 1