import sys
import time

import DP as lcs

from classes import states as states
from classes import ant as ants
# Algo accuracy 85%

##############################################################################################
# ACO Parameters                                                                             #
##############################################################################################

# Minimum number of loops the algo would run
# Everytime a better solution is generated, run for at least L steps
L = 20

# Window Size, max number of states the ants will skip or process
window = 6

# Preference for choosing local optimum, performing weighted exploration, or skipping the window entirely
# Any roll below p0 = exploitation, between p0 and p1 = exploration, above p1 = skip
p0 = 0.92
p1 = 0.98

# Bias/weight of heuristic value over pheromone value, P > 1 makes heuristic value weigh more, P < 1 makes
# pheromone value weigh more
P = 1.25  

# Evaporation Rate
e = .05

##############################################################################################
# Program Proper                                                                             #
##############################################################################################

if (len(sys.argv) != 2):
    sys.exit("Program ran as <program filename> <input filename>")

with open(sys.argv[1]) as f:
    lines = f.readlines()

# Contains the states, where each character is converted to a state that contains the existing char, position, 
# heuVal, and pherVal, refer to states.py
stateList = []

# Contains the search agents, refer to ant.py
antList = []

ACOLCSAve = 0
ACOLCSAveTime = 0
Exact = 0
ExactAveTime = 0

actualsoln = 0
extraavesoln = 0

Z = 1000

# Converting the input
for line in lines:
    if line != '\n':
        print(line.strip())

        # Reset per sequence
        tempList = []
        index = 0

        # Creates a state instance per character, heuVal and pherVal defaulted to 1
        for char in line:
            if(char != '\n'):
                ch = states.state(char, index, 1, 1)
                tempList.append(ch)
            index += 1
        stateList.append(tempList)


for z in range(Z):
    print(z)
    # Stores the length of the best found LCS
    lcsLen = -1

    # Stores the best solution
    soln = []

    # Counter for L
    count = 0

    # Timestamp 1: Start of Algo
    start_time = time.time()

    ##############################################################################################
    # ACO Proper                                                                                 #
    ##############################################################################################
    while count < L:
        antList = []
        
        # Used to find gen-best solutions
        genBest = -1
        antgenBest = -1
        
        # Generating Ants
        for i in range(len(stateList)):
            ant = ants.ant(0, i, 0, 0, len(stateList))
            antList.append(ant)

        # Control variable for ACO loop
        fin = 0

        while fin != 1:

            # Recalcing heuVals based on position, refer to recalc method on ant.py
            for i in range(len(antList)):
                if antList[i].getRunning() == 0:
                    antList[i].recalc(stateList, window, P)

            # Generating pList based on heuVals of next (window) states, refer to setprobabilities and transition on ant.py
            for i in range(len(antList)):
                if antList[i].getRunning() == 0:
                    pList = antList[i].setprobabilities(stateList, window)
                    # Ant transitions, as per the algorithm
                    antList[i].transition(stateList, pList, p0, p1, window)

            # Checks if the ants have stopped running
            for i in range(len(antList)):
                if antList[i].getRunning() == 0:
                    fin = 0
                    break
                else:
                    fin = 1

        # Compares results with existing best solution, also compares ants to find which has the generation-best solution
        for i in range(len(antList)):
            antSoln = antList[i].getSoln()

            # Finds extra matches greedily, saves them at each ant's 'extra' property, see ant.py for details
            antList[i].improve(stateList)
            
            # Finds gen-best solution
            if(len(antList[i].getSoln()) + len(antList[i].getExtra()) > genBest):
                genBest = len(antList[i].getSoln()) + len(antList[i].getExtra()) 
                antgenBest = i

            # Finds all time found best solution
            if(len(antList[i].getSoln()) + len(antList[i].getExtra()) > lcsLen):
                lcsLen = len(antList[i].getSoln()) + len(antList[i].getExtra()) 
                soln = antList[i].getSoln()
                extraSoln = antList[i].getExtra()
                count = 0
            #print("Length: ", len(antList[i].getSoln()), " ", ". Extra Matches: ", len(antList[i].getExtra()    ))

        antList[antgenBest].update(stateList, e)
        count += 1

    # Timestamp 2: End of Algo
    algo_time = time.time()

    ##############################################################################################
    # Printing Results                                                                           #
    ##############################################################################################

    #print("LCS length determined by algo is " + str(int(lcsLen) -  len(extraSoln) - 1))
    #print("Extra matches found with len: ", len(extraSoln))
    #print("=========")
    #print("Total Length of Solution is: ", (lcsLen - 1))
    #print("Time spent by algorithm is " + str(algo_time - start_time) + " seconds")

    ACOLCSAve += int(lcsLen - 1)
    ACOLCSAveTime += algo_time - start_time

    actualsoln += lcsLen - 1
    extraavesoln += len(extraSoln)

    ##############################################################################################
    # Obtaining the exact LCS using DP                                                           #
    ##############################################################################################

    #X = lines[0]
    #Y = lines[2]
    #length = lcs.lcs(X, Y)

    # Timestamp 3: End of DP Algo
    base_time = time.time()
    #print("Length of LCS using DP method is ", length)
    #print("Exact solution found in " + str(base_time - algo_time) + " seconds using DP method")

    #ExactAveTime += base_time - algo_time
    #Exact = length

    for i in range(len(stateList)):
        for j in range(len(stateList[i])):
            stateList[i][j].setpherVal(1)

print("Average time of ACO-LCS: ", ACOLCSAveTime / Z)
print("Average length of ACO-LCS: ", ACOLCSAve / Z)
print("Average length of ACO-LCS w/o Improve: ", actualsoln / Z)
print("Average length of ACO-LCS w/ Improve: ", extraavesoln / Z)

#print("Average time of Exact solution: ", ExactAveTime / 50)
#print("Exact Solution length: ", Exact)
