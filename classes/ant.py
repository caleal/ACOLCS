# Generating P
import random

class ant:
	def __init__ (self, index, seq, running, stepCount, seqCount):
		# list containing states of the partial solution 
		self.soln = [[0 for i in range(seqCount)]]
		self.extra = []

		# index of the ant's place currently
		self.index = index

		# sequence the ant is assigned to
		self.seq = seq

		# if ant is still live and running
		self.running = running
		self.stepCount = stepCount

##############################################################################################
# Getters                                                                                    #
##############################################################################################

	def getIndex(self):
		return self.index

	def getRunning(self):
		return self.running

	def getSoln(self):
		return self.soln

	def getExtra(self):
		return self.extra

##############################################################################################
# Other methods for functionality                                                            #
##############################################################################################
	# Recalculates heuristic values of next <window> states
	def recalc(self, stateList, window, P):
		start = self.index

		# Checks if next <window> states end up reaching past the end of list
		if self.index + window > len(stateList[self.seq]) - 1:
			window = (len(stateList[self.seq]) - self.index) - 2
			#print(window)

		# Checks if the ant has done a movement, in this case since default index is on 0, 
		if self.stepCount == 0:
			end = start + window
		
		elif self.stepCount > 0:
			# The start of computation would be the next (window) indices
			start = start + 1
			end = start + window

		# Updates heuVals
		# Chooses each character within window
		for i in range(start, end):
			ch = stateList[self.seq][i].getChar()
			gap = 0
			# Gets total gap of characters if this character is chosen
			for j in range(len(stateList)):
				# If checking on same sequence then just add the gap between i and starting pos
				if j == self.seq:
					gap += i - start
				else:
					# If checking on other sequence then have to go find closest matching character
					for k in range(self.soln[-1][j] + 1, len(stateList[j])):
						if(stateList[j][k].getChar() == ch):
							# Increment the gap with the distance between where this character starts and where next match is
							gap += k - self.soln[-1][j]
							break
						if k == len(stateList[j]) and stateList[j][k].getChar() != ch:
							# This state cannot be used as a solution extension
							gap = -1
							stateList[self.seq][i].setheuVal(-1)
							j += 1
							break
			if (gap == 0):
				gap = 1
			stateList[self.seq][i].setheuVal(1/(gap ** P))
		return 1

	def setprobabilities(self, stateList, window):
		start = self.index

		# Total 'p' value (heuristic value * pheromone value)
		p = 0

		# 'p' value of a specific state, scaled to a %tage (p/ptotal)
		p0 = 0

		# Index of highest 'p' value
		maxIndex = 0

		# Temporary list of 'p' values
		tempList = []

		# List of 'p' values for next (window) states, along with index of max value at index 1
		pList = []

		# temp variable for getting max
		tempMax = 0
		tempIndex = 0

		# Sets max to the last index on the list if the window extends to farther than the last index
		if (self.index + window > len(stateList[self.seq]) - 1):
				window = len(stateList[self.seq]) - (self.index + 1)

		# For checking initial values, alternatively check stepcount if it's 0
		if self.stepCount == 0:
			# Consider index [0] as a valid index
			end = start + window
		
		else:
			# The start of computation would be the next (window) indices
			start = start + 1
			end = start + window

		# Getting total values
		for i in range(start, end):
			p += stateList[self.seq][i].getheuVal() * stateList[self.seq][i].getpherVal()

		# Getting total values scaled to a %tage
		for i in range(start, end):
			temp = stateList[self.seq][i].getheuVal() * stateList[self.seq][i].getpherVal() / p
			p0 += temp

			if temp > tempMax:
				tempMax = temp
				tempIndex = i
			tempList.append(p0)

		# Appends tempList to pList
		pList.append(tempList)

		# Appends index of largest 'p' value to pList
		pList.append(tempIndex)

		return pList

	def transition(self, stateList, pList, p0, p1, window):
		# Stops the transition if there aren't any possible movements
		if len(pList[0]) == 0:
			self.running = 1
			return -1

		# Random roll
		p = random.uniform(0.0, 1.0)

		tempSoln = []

		while True:
			if self.running == 1:
				return -1

			# Case 1: Immediately goes to the most promising state
			if p <= p0:
				tempIndex = pList[1]
				
				# Check if movement is valid
				tempSeq = 0

				# print("Character picked is: " + str(stateList[self.seq][tempIndex].getChar() + " at sequence " + str(self.seq) + " and index " + str(tempIndex)))
				
				# Finds the first instance of this character across all sequences relative to current position
				for i in range(len(self.soln[-1])):

					# Iterates over the current index in a given seq, compares with the char picked as its' next char

					for j in range(self.soln[-1][i] + 1, len(stateList[self.seq])):
						# No need to find matching character at assigned sequence
						if i == self.seq:
								tempSoln.append(tempIndex)
								break

						# Find matching character at other sequences
						if stateList[i][j].getChar() == stateList[self.seq][tempIndex].getChar():
							tempSoln.append(j)

							# Last index matches with whatever this index is, terminate early
							if j == len(stateList[self.seq]) - 1:
								self.running = 1
							break

						# Check if j reaches end of its' respective seqeuence
						if j == len(stateList[self.seq]) - 1:
							self.running = 1
							break

				if len(tempSoln) == len(self.soln[0]):
					self.soln.append(tempSoln)
					self.index = tempIndex
					self.stepCount += 1
					return 1
				
				if (self.index > len(stateList[self.seq]) - 1):
					self.index = len(stateList[self.seq]) - 1
					self.running = 1
					return 1
				

			# Case 2: Picks a random state within w, probabilities based off of pList
			elif p0 < p and p < p1:
				# Random number generated
				rand = random.uniform(0.0, 1.0)

				for i in range(len(pList[0])):
					if rand <= pList[0][i]:

						# PYTHON starts at 0 index, increment by 1 to compensate
						tempIndex = self.index + i + 1
						break
						
				# Finds the first instance of this character across all sequences relative to current position
				for i in range(len(self.soln[-1])):

					# Iterates over the current index in a given seq, compares with the char picked as its' next char
					for j in range(self.soln[-1][i] + 1, len(stateList[self.seq])):
						if i == self.seq:
								tempSoln.append(tempIndex)
								break

						if stateList[i][j].getChar() == stateList[self.seq][tempIndex].getChar():
							tempSoln.append(j)

							# Last index matches with whatever this index is, terminate early
							if j == len(stateList[self.seq]) - 1:
								self.running = 1
							break

						# Check if j reaches end of its' respective seqeuence
						if j == len(stateList[self.seq]) - 1:
							self.running = 1
							break

				if len(tempSoln) == len(self.soln[0]):
					self.soln.append(tempSoln)
					self.index = tempIndex
					self.stepCount += 1
					return 2
				
				if (self.index > len(stateList[self.seq]) - 1):
					self.index = len(stateList[self.seq]) - 1
					self.running = 1
					return 2

			# Skip this window
			else:
				self.index += window - 1
				if (self.index >= len(stateList[self.seq]) - 1):
					self.index = len(stateList[self.seq]) - 1
					self.running = 1

				self.stepCount += 1
				return -1

	# Improves the solution greedily, looking for matching characters in between 
	def improve(self, stateList):
			tempSoln = []
			soln = self.soln
			for i in range(len(soln) - 1):
			    
			    # Using the index of the ant assigned to the best solution found as pivot
			    br = 0
			    cont = -1
			    for j in range(soln[i][self.seq] + 1, soln[i + 1][self.seq]):
			        
			        # Chars not picked by the ant that generated the best solution on the sequence it's assigned to
			        temptempSoln = []
			        ch = stateList[self.seq][j].getChar()
			        
			        # Finds common characters that wasn't picked by the algo and inserts them onto the best solution
			        for k in range(len(soln[i])):

			            if br == 1:
			            	start = cont

			            else:
			            	start = soln[i][k] + 1

			            if k != self.seq:
			            	while start < soln[i + 1][k]:
			            		if ch == stateList[k][start].getChar():
			            			temptempSoln.append(start)
			            			cont = start + 1
			            			br = 1
			            			break
			            		else:
			            			start += 1

			            elif k == self.seq:
			                temptempSoln.append(j)

			        if len(temptempSoln) > 1:
			            tempSoln.append(temptempSoln)

			self.extra = tempSoln
			#print("Length: ", len(self.soln), ". Extra Matches: ", len(tempSoln), ". Total Length: ", len(tempSoln) + len(self.soln))

	# Updates the pheromone values, run everytime all ants finish their iterations
	def update(self, stateList, e):

		# Decrements all pheromone values by a factor of (1 - e)
		for i in range(len(stateList)):
			for j in range(len(stateList[i])):
				stateList[i][j].setpherVal((1 - e) * stateList[i][j].getpherVal())

		# Increases all pheromone values found in soln
		for i in range(1, len(self.soln)):
			for j in range(len(self.soln[i])):
				stateList[j][self.soln[i][j]].incpherVal(e)

		# Increases all pheromone values found in extra
		for i in range(len(self.extra)):
			for j in range(len(self.extra[i])):
				stateList[j][self.extra[i][j]].incpherVal(e)


	def output(self):
		print("(" + str(self.soln) + "," + str(self.index) +  "," + str(self.seq) + "," + str(self.stepCount) + "," + str(self.genCount) + ")")