import re
import random
import pickle
from shutil import copyfile

from STB_help import *

def readTrajectoryFile(DMTrajectories):
    filepath = "../Lexington/primaryRoads.osm.wkt"
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


def getSourceDesCoordinates(src_start, src_end, des_end):
    bus_routes = pickle.load(open(lex_data_directory + "bus_route_ids.pkl", "rb"))
    village_coors = [0 for x in range(des_end + 1)]
    bus_routes = list(set(bus_routes))

    print(bus_routes)
    print(src_start, src_end, des_end)
    for srcID in range(src_start, src_end, 1):
        #Choose src and des from bus routes
        route_id = random.choice(bus_routes)
        #bus_routes.remove(route_id)
        src = random.choice(DMTrajectories[route_id])

        if srcID + src_end >= des_end:
            village_coors[srcID] = src
            print("SRC Route ID", route_id, srcID, src)

        else:
            des = random.choice(DMTrajectories[route_id])
            dist = euclideanDistance(float(str(src).split()[0]), float(str(src).split()[1]), float(str(des).split()[0]), float(str(des).split()[1]))
            count = 0
            adequate_dist = random.randint(1000, 2500)
            while dist < adequate_dist:
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
            village_coors[srcID] = src
            village_coors[srcID + src_end] = des


    # for desID in range(0, des_end - src_end, 1):
    #     rand_location = random.choice(DMTrajectories[chosen_bus_route[desID]])
    #     village_coors.append(rand_location)
    #     # print(village_coors[desID].split()[0], village_coors[desID + src_end].split()[0])
    #     count = 0
    #     while count< len(DMTrajectories[chosen_bus_route[desID]]) and euclideanDistance(float(village_coors[desID].split()[0]), float(village_coors[desID].split()[1]), float(village_coors[desID + src_end].split()[0]), float(village_coors[desID + src_end].split()[1])) < 2000:
    #         count = count + 1
    #         rand_location = random.choice(DMTrajectories[chosen_bus_route[desID]])
    #         village_coors[src_end + desID] = rand_location

            # print("DES Route ID", chosen_bus_route[desID - src_end], rand_location, euclideanDistance(float(village_coors[desID].split()[0]), float(village_coors[desID].split()[1]), float(village_coors[desID + src_end].split()[0]), float(village_coors[desID + src_end].split()[1])))


    f = open(lex_data_directory + "village_coor.pkl", 'wb')
    pickle.dump(village_coors, f)
    f.close()

def getBusRoutes(bus_start, bus_end):
    bus_routes = []
    for srcID in range(bus_start, bus_end, 1):
        bus_routes.append(random.randint(0, len(DMTrajectories)-1))

    f = open(lex_data_directory +  "bus_route_ids.pkl", 'wb')
    pickle.dump(bus_routes, f)
    f.close()
    print(bus_routes)

def getLocationsOfSourcesAndDataCenters(startIndex, endIndex):
    # create file for Sources. Though the source location are fixed, the spectrum bandwidth changes over time
    # Hence, it is important to save it as a file

    villageCoor = pickle.load(open(lex_data_directory + "village_coor.pkl", "rb"))
    for srcID in range(startIndex, endIndex, 1):

        # villageCoor = random.choice(DMTrajectories[srcID%len(DMTrajectories)])
        srcLocationX = villageCoor[srcID].strip().split(" ")[0]
        srcLocationY = villageCoor[srcID].strip().split(" ")[1]
        # print("Location: " + villageCoor[srcID] + " " + srcLocationX + " " + srcLocationY)

        with open(lex_data_directory_day + str(srcID) + ".txt", "w") as srcP:
            srcP.write("T X Y ")
            for s in S:
                srcP.write("S" + str(s) + " ")
            srcP.write("\n")

            for t in range(0, T, dt):
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
    bus_route_ids = pickle.load(open(lex_data_directory + "bus_route_ids.pkl", "rb"))

    for ind in range(startIndex, endIndex, 1):
        dmID = dmID + 1
        currTime = random.randint(route_start_time1, route_start_time2)
        currCoorID = 0
        nextCoorID = 1
        dmSpeed = random.randint(VMIN, VMAX)

        # chosen_trajectory_id = random.randint(0, len(DMTrajectories)-1)

        chosen_trajectory_id  = bus_route_ids[ind]
        eachDM = DMTrajectories[chosen_trajectory_id]

        villageCoor = pickle.load(open(lex_data_directory + "village_coor.pkl", "rb"))

        # print("Village coors", villageCoor)
        # print("Bus route ", bus_route_ids[ind], DMTrajectories[bus_route_ids[ind]], "\n")

        # print("Trajectory " +  str(len(eachDM)) + " : " + str(eachDM))

        with open(lex_data_directory_day + "/"+ str(dmID)+".txt", "w") as dmP:
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


def copy_files():
    # for run in range(1, 11, 1):
    for i in range(V):
        run = lex_data_directory_day.split("/")[2]
        day = lex_data_directory_day.split("/")[3]
        # print("Current run is: ", run)
        src = "../Lexington" + str(max_nodes) + "/" + str(run) + "/" + day  + "/" + str(i) + ".txt"
        dst = lex_data_directory_day + str(i) + ".txt"
        copyfile(src, dst)

# Main starts here

#change the directory to the parent one
#We want same source, destination, and bus routes irrespective of number of runs and days
lex_data_directory = lex_data_directory.split("/")[0] +"/" + lex_data_directory.split("/")[1] + "/"

# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V, V, numSpec, int(T/dt), int(T/dt)))
LINK_EXISTS.fill(math.inf)

T = T + 30

if not os.path.exists(lex_data_directory_day):
    os.makedirs(lex_data_directory_day)

DMTrajectories = []         #stores the coordinates for each data mule

# Read trajectory for each data mule
readTrajectoryFile(DMTrajectories)
# selectedDMTrajectories = DMTrajectories[:3]

print("Length of DM trajectories: ", len(DMTrajectories))

#Just copy files, we don't have to generate the trajectories
if V - NoOfDataCenters - NoOfSources < max_nodes:
    copy_files()

else:
    #TODO: Run it only for Day1
    if "Day1" in lex_data_directory_day and lex_data_directory_day.split("/")[2] == str(run_start_time):
        print("New locations generated\n")
        getBusRoutes(0, NoOfDMs)
        getSourceDesCoordinates(0, NoOfSources, (NoOfSources + NoOfDataCenters))

    # Randomly place sources and destination nodes (index from 0 to S -1)
    getLocationsOfSourcesAndDataCenters(0, NoOfSources + NoOfDataCenters)

    # Place DMs on selected Routes (index from (S - DM)
    getLocationsOfDMs(DMTrajectories, 0, NoOfDMs)

