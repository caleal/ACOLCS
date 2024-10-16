# For example, sequence S1 has characters "abcde", these are placed on a statelist S1 such that S1[0] contains 
# the character 'a' at index 0, 'b' at index 1, and so on

# Heuristic value is calced by the distance between state m to state n; larger gaps between states give lower heuristic values

# Pheromone default set to 1 so it doesn't affect initial set of movement; ants move depending on heuristic value alone. Update pheromone value 
# after first generation
# reduce all states pheromone by some value, increase pheromone of states picked by some value.

# Check ant.py for specifics on how heuVals and pherVals are calculated

class state:
	def __init__(self, char, pos, pherVal, heuVal):
		self.char = char
		self.pos = pos
		self.pherVal = pherVal
		self.heuVal = heuVal

	def output(self):
		print("(" + str(self.char) + "," + str(self.pos) +  "," + str(self.pherVal) + "," + str(self.heuVal) + ")")

	def getChar(self):
		return self.char

	def getPos(self):
		return self.pos

	def getpherVal(self):
		return self.pherVal

	def getheuVal(self):
		return self.heuVal

	def setpherVal(self, pherVal):
		self.pherVal = pherVal

	def incpherVal(self, pherVal):
		self.pherVal += pherVal

	def decpherVal(self, pherVal):
		self.pherVal -= pherVal

	def setheuVal(self, heuVal):
		self.heuVal = heuVal

	def update(self):
		pass