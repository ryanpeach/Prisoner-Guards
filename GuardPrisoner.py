class State:
	def __init__(self, boatOnLeft=True, boatSize = 2, prisoners=(4,0), guards=(4,0)):
		self.B = boatOnLeft
		self.Z = boatSize
		self.P = prisoners
		self.G = guards
		
	def move(self, prisoners, guards):
		if prisoners + guards <= self.Z:
			if self.B:
				newP = (self.P[0] - prisoners, self.P[1] + prisoners)
				newG = (self.G[0] - guards,self.G[1] + guards)
			else:
				newP = (self.P[0] + prisoners, self.P[1] - prisoners)
				newG = (self.G[0] + guards, self.G[1] - guards)

		return ((not self.B,prisoners,guards),State(not self.B,self.Z,newP,newG),self)
			
	def locNum(self,loc):
		i = 1
		if loc:
			i = 0
		return i
	
	def test(self):
		output = True;
		for x in [0,1]:
			if (self.P[x] > self.G[x] and self.G[x] != 0) or self.P[x] < 0 or self.G[x] < 0:
				output = False;
		return output
	
	def copy(self):
		return State(self.B,self.Z,self.P,self.G)
		
	def __eq__(self, newState):
		return newState.B == self.B and newState.G == self.G and newState.P == self.P and newState.Z == self.Z

	def __hash__(self):
		Z=sum(self.P)+sum(self.G)
		return self.locNum(self.B)*Z^4+self.P[0]*Z^3+self.P[1]*Z^2+self.G[0]*Z^1+self.G[1]

	def __str__(self):
		return repr((self.B,self.P,self.G))
                

class Generator:
	def __init__(self, initState, tester):
		self.S = initState
		self.T = tester
	
	def generate(self):
		for z in range(1,self.S.Z+1):
			for x in range(0,z+1):
				y = z - x
				newMove = self.S.move(x,y)
				if self.T.add(newMove):
					#print newMove[1]
					pass
				if self.T.Victory:
					return
					
class SemanticNet:
	def __init__(self, initialState):
		self.Graph = {initialState:[]}
		self.WorkingMemory = [initialState]
		
	def addNode(self, newMove):
		self.addLink(newMove)
		self.Graph[newMove[1]] = []
		self.WorkingMemory.append(newMove[1])
		
	def addLink(self, newMove):
		self.Graph[newMove[2]].append(newMove[0:1])
	
	def search(self, newNode):
		for node in self.Graph:
			if node == newNode:
				return (len(self.Graph[node]) == 0,True)
		return (False,False)
		
	def pop(self):
		return self.WorkingMemory
		
class Tester:
	def __init__(self, net, goal):
		self.G = net
		self.W = goal
		self.Victory = net.search(goal)[1]
		
	def add(self, newMove):
		move = newMove[0]
		state = newMove[1]
		org = newMove[2]
		
		if self.goal(state):
			self.Victory = True
		
		if state.test():
			#print True
			value, duplicate = self.G.search(state)
			if not duplicate:
				self.G.addNode(newMove)
				return True
			elif value:
				self.G.addLink(newMove)
				return True
			else:
				return False
		else:
			return False
			
	def goal(self, newNode):
		if self.W == newNode:
			self.Victory = True
			return True
		return False

for U in range(2,50):			
	Start = State(True, 3, (U,0), (U,0))
	Finish = State(False, 3, (0,U), (0,U))
	Net = SemanticNet(Start)
	Test = Tester(Net, Finish)

	CurrentNodes = [Start]
	num = 0
	try:
		print "------ Gen " + str(U) + " -----------"
		while not Test.Victory:
			num += 1
			source = Net.WorkingMemory.pop(0);
			#print "------ Gen " + str(num) + " -----------"
			#print "-- " + str(source) + " --"
			Generator(source, Test).generate()
		print "------ Itt. " + str(num) + " -----------"
		print "--------------- Victory! ---------------"

	except IndexError:
		print "---------- Failure... --------"
