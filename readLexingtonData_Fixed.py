import re
import random
import pickle
import shutil
import numpy

from STB_help import *

def readTrajectoryFile(DMTrajectories):
    filepath = "primaryRoads.osm.wkt"
    with open(filepath) as fp:
        lines = fp.readlines()

        for index in range(0, len(lines)):
            patternMatch = re.match(r'^LINESTRING \((.*)\)', lines[index], re.M | re.I)

            if patternMatch:
                # print ("Pattern 1: ", patternMatch.group(1))
                trajectoryCoord = patternMatch.group(1)
                if len(trajectoryCoord.strip().split(',')) > 30:
                    DMTrajectories.append(trajectoryCoord.strip().split(','))

            else:
                print ("No Match !!!")
    fp.close()

def check_dist_between_all_src_des(vil_src, vil_des, new_src, new_des):
    add_new_src_des = True
    adequate_dist = 2000

    # if len(vil_src) == 0:
    #     return True

    for des in vil_des:
        dist = euclideanDistance(float(str(new_src).split()[0]), float(str(new_src).split()[1]), float(str(des).split()[0]),
                                 float(str(des).split()[1]))
        if dist < adequate_dist:
            add_new_src_des = False

    for src in vil_src:
        dist = euclideanDistance(float(str(src).split()[0]), float(str(src).split()[1]), float(str(new_des).split()[0]),
                                 float(str(new_des).split()[1]))
        if dist < adequate_dist:
            add_new_src_des = False

    dist = euclideanDistance(float(str(new_src).split()[0]), float(str(new_src).split()[1]), float(str(new_des).split()[0]),
                             float(str(new_des).split()[1]))

    if dist < adequate_dist:
        add_new_src_des = False

    return add_new_src_des

def getSourceDesCoordinates(src_start, src_end, des_end):

    if day_num == 1:

        bus_routes = pickle.load(open(DataMule_path + "bus_route_ids.pkl", "rb"))
        village_coors = []
        village_src = []
        village_des = []

        bus_routes = list(set(bus_routes))

        print("bus_routes", bus_routes)
        print(src_start, src_end, des_end)
        for srcID in range(src_start, src_end, 1):
            #Choose src and des from bus routes
            route_id = random.choice(bus_routes)
            #bus_routes.remove(route_id)
            print("routeID:", route_id)
            src = random.choice(DMTrajectories[route_id])

            if srcID + src_end >= des_end:
                village_coors[srcID] = src
                print("SRC Route ID", route_id, srcID, src)

            else:
                des = random.choice(DMTrajectories[route_id])
                dist = euclideanDistance(float(str(src).split()[0]), float(str(src).split()[1]), float(str(des).split()[0]), float(str(des).split()[1]))
                count = 0
                adequate_dist = random.randint(2000, 2500)
                while dist < adequate_dist and check_dist_between_all_src_des(village_src, village_des, src, des) == False:
                    count = count + 1
                    if count > len(DMTrajectories[route_id]):
                        route_id = random.choice(bus_routes)
                        # print(route_id)
                        count = 0

                    src = random.choice(DMTrajectories[route_id])
                    des = random.choice(DMTrajectories[route_id])
                    dist = euclideanDistance(float(str(src).split()[0]), float(str(src).split()[1]), float(str(des).split()[0]),
                                             float(str(des).split()[1]))
                    # print(route_id, dist)

                print("SRC Route ID", route_id, srcID, src)
                print("DES Route ID", route_id, srcID + src_end, des, "dist: ", dist, "\n")
                village_src.append(src)
                village_des.append(des)
                # village_coors[srcID] = src
                # village_coors[srcID + src_end] = des

        for x in range(len(village_src)):
            village_coors.append(village_src[x])

        for x in range(len(village_des)):
            village_coors.append(village_des[x])



        f = open(DataMule_path + "village_coor.pkl", 'wb')
        pickle.dump(village_coors, f)
        f.close()

    # else:
    #     dir1 = DataMule_path + "Day1/"
    #     dir2 = DataMule_path + "Day2/"
    #     if not os.path.exists(dir1):
    #         os.makedirs(dir1)
    #     if not os.path.exists(dir2):
    #         os.makedirs(dir2)
    #     for i in range(des_end):
    #         curr_dir = DataMule_path + "Day1/" + str(i) + ".txt"
    #         new_dir = DataMule_path + "Day2/" + str(i) + ".txt"
    #         shutil.copyfile(curr_dir, new_dir)

def getBusRoutes(bus_end):
    bus_routes = []
    num_buses = 0
    srcID = 0

    while num_buses < bus_end:
        bus_routes.append(srcID)
        num_buses += 1
        if srcID == len(DMTrajectories)-1:
            srcID = 0
        else:
            srcID += 1

    f = open(DataMule_path +  "bus_route_ids.pkl", 'wb')
    print("bus route IDs:", bus_routes)
    pickle.dump(bus_routes, f)
    f.close()

def getLocationsOfSourcesAndDataCenters(startIndex, endIndex):
    # create file for Sources. Though the source location are fixed, the spectrum bandwidth changes over time
    # Hence, it is important to save it as a file
    if not os.path.exists(DataMule_path + "Day" + str(day_num)):
        os.makedirs(DataMule_path + "Day" + str(day_num))

    villageCoor = pickle.load(open(DataMule_path + "village_coor.pkl", "rb"))
    for srcID in range(startIndex, endIndex, 1):

        # villageCoor = random.choice(DMTrajectories[srcID%len(DMTrajectories)])
        srcLocationX = villageCoor[srcID].strip().split(" ")[0]
        srcLocationY = villageCoor[srcID].strip().split(" ")[1]
        # print("Location: " + villageCoor[srcID] + " " + srcLocationX + " " + srcLocationY)

        with open(DataMule_path + "Day" + str(day_num) + "/" + str(srcID) + ".txt", "w") as srcP:
            srcP.write("T X Y ")
            for s in S:
                srcP.write("S" + str(s) + " ")
            srcP.write("\n")

            for t in range(0, 2*T, dt):
                srcP.write(str(t) + " " + str(srcLocationX) + " " + str(srcLocationY) + " ")

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [minBW[s] for s in S]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    srcP.write(str(sBW) + " ")
                srcP.write("\n")
        srcP.close()


def getLocationsOfDMs(DMTrajectories, startIndex, endIndex):
    dmID = startIndex + NoOfSources + NoOfDataCenters - 1
    wait_time_dict = {}
    wait_interval = 20
    bus_route_ids = pickle.load(open(DataMule_path+ "bus_route_ids.pkl", "rb"))

    for ind in range(startIndex, endIndex, 1):
        dmID = dmID + 1
        currCoorID = 0
        nextCoorID = 1
        dmSpeed = random.randint(VMIN, VMAX)

        # chosen_trajectory_id = random.randint(0, len(DMTrajectories)-1)

        chosen_trajectory_id  = bus_route_ids[ind]
        eachDM = DMTrajectories[chosen_trajectory_id]

        # update wait time dictionary to keep track of buses on same trajectory
        if chosen_trajectory_id in wait_time_dict:
            wait_time_dict[chosen_trajectory_id] += 1
        else:
            wait_time_dict[chosen_trajectory_id] = 0

        currTime = wait_interval * wait_time_dict[chosen_trajectory_id]

        villageCoor = pickle.load(open(DataMule_path + "village_coor.pkl", "rb"))

        # print("Village coors", villageCoor)
        # print("Bus route ", bus_route_ids[ind], DMTrajectories[bus_route_ids[ind]], "\n")

        # print("Trajectory " +  str(len(eachDM)) + " : " + str(eachDM))

        with open(DataMule_path + "Day" + str(day_num) +"/"+ str(dmID + NoOfSources + NoOfDataCenters)+".txt", "w") as dmP:
            # print ("For DM: " + str(dmID) + " Speed: " + str(dmSpeed))
            dmP.write("T X Y ");
            for s in S:
                dmP.write("S"+ str(s) + " ")
            dmP.write("\n")

            # By default, move in the forward direction
            isDirectionForward = True

            chosen_wait_time = random.choice(wait_time)

            for t in range(currTime, T, dt):
                prevCoors = eachDM[currCoorID].strip().split(' ')
                currCoors = eachDM[nextCoorID].strip().split(' ')

                consumedTime = euclideanDistance(prevCoors[0], prevCoors[1], currCoors[0], currCoors[1])/dmSpeed
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))


                # if prevCoors in villageCoor:
                if eachDM[currCoorID] in villageCoor and chosen_wait_time > 0:
                    chosen_wait_time -= 1
                    dmP.write(str(t) + " " + eachDM[currCoorID].strip() + " ")
                    # if chosen_wait_time == 1:
                    #     print("Bus ", chosen_trajectory_id, " Time: " , t, " Coor: ", prevCoors, " Cons Time: ", consumedTime)

                elif consumedTime > t or t == T- dt:
                    # Stay in the same location
                    # print (str(t) + " " + str(eachDM[currCoorID]))
                    dmP.write(str(t) + " " + eachDM[currCoorID].strip() + " ")

                else:
                    # Move to the next location
                    dmP.write(str(t) + " " + eachDM[nextCoorID].strip() + " ")

                    #Set the current ID and next ID appropriately
                    currCoorID = nextCoorID

                    #repeat from start of the trajectory (if currently at the end of the trajectory)
                    # Each trajectory is periodic
                    if currCoorID == len(eachDM) - 1:
                        isDirectionForward = False

                    if currCoorID == 0:
                        isDirectionForward = True

                    if isDirectionForward:
                        nextCoorID = currCoorID + 1

                    else:
                        nextCoorID = currCoorID - 1

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [minBW[s] for s in S]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    dmP.write(str(sBW) + " ")
                dmP.write("\n")
        dmP.close()

#
# def copy_files():
#     # for run in range(1, 11, 1):
#     for i in range(V):
#         run = lex_data_directory_day.split("/")[2]
#         day = lex_data_directory_day.split("/")[3]
#         # print("Current run is: ", run)
#         src = "../Lexington" + str(max_nodes) + "/" + str(run) + "/" + day  + "/" + str(i) + ".txt"
#         dst = lex_data_directory_day + str(i) + ".txt"
#         copyfile(src, dst)

# Main starts here

#change the directory to the parent one
#We want same source, destination, and bus routes irrespective of number of runs and days

# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V + NoOfSources + NoOfDataCenters, V + NoOfSources + NoOfDataCenters, numSpec, int(T/dt)))
LINK_EXISTS.fill(math.inf)

T = T + 30

if not os.path.exists(DataMule_path):
    os.makedirs(DataMule_path)

DMTrajectories = []         #stores the coordinates for each data mule

# Read trajectory for each data mule
readTrajectoryFile(DMTrajectories)
# selectedDMTrajectories = DMTrajectories[:3]

print("Length of DM trajectories: ", len(DMTrajectories))

if V + NoOfDataCenters + NoOfSources == max_nodes:

    #TODO: Run it only for Day1

    if generate_link_exists == True:
        print("New locations generated\n")
        getBusRoutes(V)
        getSourceDesCoordinates(0, NoOfSources, (NoOfSources + NoOfDataCenters))

    # Randomly place sources and destination nodes (index from 0 to S -1)
    getLocationsOfSourcesAndDataCenters(0, NoOfSources + NoOfDataCenters)

    # Place DMs on selected Routes (index from (S - DM)
    getLocationsOfDMs(DMTrajectories, 0, V)

