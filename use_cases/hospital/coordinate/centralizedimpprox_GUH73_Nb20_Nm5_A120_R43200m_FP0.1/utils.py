import numpy as np
import os
import sys
import random
import collections
import queue
import shutil
from params import *

class Clock:
	time = -1.0
	eventDict = {}
	
	def __init__(self):
		self.time = 0.0
		
	def getTime(self):
		return self.time
		
	def updateTime(self, increment):
		self.time += increment
		
	def scheduleEvent(self, event, avgTimes, traceFiles, distributions):
		increment = 0.0
		for avgTime, traceFile, distribution in zip(avgTimes, traceFiles, distributions):
			if distribution == 'exponential':
				increment += np.random.exponential(avgTime)
			elif distribution == 'deterministic':
				increment += avgTime
			elif distribution == 'trace':
				if avgTime >= 0:
					print('[ERROR] You asked for using a trace, but provided an positive average time')
					sys.exit(-1)
				with open(traceFile, 'r') as f:
					lines = f.readlines()
					if len(lines) > 0:
						avgTime = lines.pop(0)
					else:
						print('No more timestamps in ' + traceFile)
						os.remove(traceFile)
						sys.exit(0)
				with open(traceFile, 'w') as f:
					f.writelines(lines)
				increment += float(avgTime)
			else:
				print('[ERROR] Distribution ' + distribution + ' is not supported')
				sys.exit(-1)
		self.eventDict[self.time + increment] = event
			
	def getNextEvent(self):
		timeList = self.eventDict.keys()
		self.time = min(timeList)
		event = self.eventDict.pop(self.time)
		return self.time, event
		
	def getAllNextEvents(self):
		return self.eventDict
		
	def checkClock(self):
		events = self.eventDict.values()
		if len(events) != len(set(events)): # there are duplicate in the list
			duplicates = [item for item, count in collections.Counter(events).items() if count > 1]
			print('[ERROR] The same event has been scheduled more than once. ')
			print(duplicates)
			sys.exit(-1)
			
	def removeEvent(self, eventToRemove):
		times = list(self.eventDict.keys())
		nextEvents = self.eventDict.values()
		keysToRemove = []
		for idx, event in enumerate(nextEvents):
			if event == eventToRemove:
				keysToRemove.append(times[idx])
		for k in keysToRemove:
			del self.eventDict[k]
		
		


class Item:
	idx = -1
	importance = -1 # -1: toInit, 0: low, 1: medium, 2:high
	position = None
	target = None
	uber = None # the robot that is moving this item
	logfile = '' # name (string) of the file containing all the logs of this item
	
	def __init__(self, logfile, idx, space, simTime, imp=-1, target=None):
		self.idx = idx
		self.position = space.getSource()
		if target == None:
			availTargetZones = [room for room in space.getRooms() if room != space.getSource()]
			self.target = random.choice(availTargetZones)
		else:
			self.target = target
		if imp == -1:
			self.importance = self.getRandomImportance(IMPORTANCE_PROBABILITIES)
		else:
			self.importance = imp
		self.logfile = logfile
		if LOG_ITEM:
			self.logEvent(simTime, 'create')
	
	def getIdx(self):
		return self.idx
			
	def getImportance(self):
		return self.importance
		
	def getLocation(self):
		return self.position
		
	def setLocation(self, room):
		self.position = room
		
	def getTarget(self):
		return self.target
		
	def getRandomImportance(self, importanceProbList):
		if sum(importanceProbList) != 1:
			print('[ERROR] This list must sum to 1')
			sys.exit(-1)
		rv = np.random.uniform()
		probSum = 0.0
		for k, prob in enumerate(importanceProbList):
			probSum += prob
			if rv < probSum:
				return k
				
	def getUber(self):
		return self.uber
		
	def setUber(self, robot):
		self.uber = robot
		
	def logEvent(self, simTime, event):
		if not os.path.exists(self.logfile):
			with open(self.logfile, 'w') as f:
				f.write('simTime,robotId,itemId,itemImportance,position,destination,event\n')
		with open(self.logfile, 'a') as f:
			# simulationTime, robotId, itemId, itemImportance, position, event
			f.write(str(simTime)+','+str(-1)+','+str(self.idx)+','+str(self.importance)+','+str(self.position.getIdx())+','+str(self.target.getIdx())+','+str(event)+'\n')


class Robot:
	idx = -1
	item = None
	healthy = True
	space = None
	position = None # the room where the robot is located
	destination = None # where the robot is going
	optRoute = [] # the route to follow
	failureProb = FAIL_PROB
	memoryItem = None # save the previous item if it was dropped due to an abort_mission message
	malicious = False
	logfile = '' # name (string) of the file containing all the logs of this robot

	def __init__(self, idx, malicious, space, logfile):
		self.idx  = idx
		self.malicious = malicious
		self.space = space
		self.position = space.getSource()
		self.destination = space.getSource()
		self.space.setRobotPosition(self, self.space.getSource())
		self.logfile = logfile
	
	def getIdx(self):
		return self.idx
		
	def isFree(self):
		if self.item == None:
			return True
		else:
			return False
		
	def isHealthy(self):
		return self.healthy
		
	def hasOtherTasks(self):
		if len(self.optRoute) > 0:
			return True
		return False
		
	def getItem(self):
		return self.item
		
	def setItem(self, item):
		self.item = item
		item.setUber(self)
		
	def unsetItem(self):
		self.item.setUber(None)
		self.item = None
		
		
	def getItemImportance(self):
		if self.item == None:
			return -1
		return self.item.getImportance()
		
	def dropItem(self, simTime, itemExpired=False):
		if self.position == self.destination:
			if LOG_DELIVERY:
				self.logEvent(simTime, 'deliver')
			self.space.deliverItem(self.item)
		else:
			if LOG_DROP:
				self.logEvent(simTime, 'drop')
			if itemExpired:
				self.space.getClock().removeEvent('move-' + str(self.getIdx()))
			else:
				self.item.setLocation(self.position)
				self.space.switchItem(self.item)
		self.unsetItem()
		self.destination = self.space.getSource()
		if len(self.space.getItemsByImportance(imp=-1, room=self.position)) == 0 and self.isHealthy(): # If there are not other items to load and the robot is healthy, then find the way back home
			self.optRoute = self.space.findRoute(self.position, self.destination, strategy=FIND_ROUTE_STRATEGY)
			if itemExpired and self.position != self.space.getSource():
				self.space.getClock().scheduleEvent('move-' + str(self.getIdx()), [MOVEMENT_TIME], [MOVEMENT_DISTR])
				
	def loadItem(self, item, simTime):
		if self.item != None:
#			print('[ERROR] Only one item per robot')
#			sys.exit(-1)
			self.dropItem(simTime)
		if ARCHITECTURE == 'semi-decentralized': # Pay both computation COMP and communication COMM
			self.space.getClock().scheduleEvent('move-' + str(self.getIdx()), [LOAD_TIME, COMP_TIME, MOVEMENT_TIME, COMM_TIME, DROP_TIME], [LOAD_TRACE, COMP_TRACE, MOVEMENT_TRACE, COMM_TRACE, DROP_TRACE], [LOAD_DISTR, COMP_DISTR, MOVEMENT_DISTR, COMM_DISTR, DROP_DISTR]) #Every item that is loaded will be (sooner or later) dropped. The drop time is payed as soon as the item is loaded
		elif 'centralized-' in ARCHITECTURE: # Pay only communication COMM
			self.space.getClock().scheduleEvent('move-' + str(self.getIdx()), [LOAD_TIME, 0, MOVEMENT_TIME, COMM_TIME, DROP_TIME], [LOAD_TRACE, '_', MOVEMENT_TRACE, COMM_TRACE, DROP_TRACE], [LOAD_DISTR, COMP_DISTR, MOVEMENT_DISTR, COMM_DISTR, DROP_DISTR]) #Every item that is loaded will be (sooner or later) dropped. The drop time is payed as soon as the item is loaded
		else: # Pay only computation COMP (if fully-decentralized)
			self.space.getClock().scheduleEvent('move-' + str(self.getIdx()), [LOAD_TIME, COMP_TIME, MOVEMENT_TIME, 0, DROP_TIME], [LOAD_TRACE, COMP_TRACE, MOVEMENT_TRACE, '_', DROP_TRACE], [LOAD_DISTR, COMP_DISTR, MOVEMENT_DISTR, COMM_DISTR, DROP_DISTR]) #Every item that is loaded will be (sooner or later) dropped. The drop time is payed as soon as the item is loaded
		self.memoryItem = None
		self.setItem(item)
		self.destination = item.getTarget()
		self.space.switchItem(item)
		self.optRoute = self.space.findRoute(self.position, self.destination, strategy=FIND_ROUTE_STRATEGY)
		if LOG_LOAD:
			self.logEvent(simTime, 'startLoading')
		
	def logEvent(self, simTime, event):
		if not os.path.exists(self.logfile):
			with open(self.logfile, 'w') as f:
				f.write('simTime,robotId,itemId,itemImportance,position,destination,event\n')
		with open(self.logfile, 'a') as f:
			# simulationTime, robotId, itemId, itemImportance, position, event
			if self.item != None:
				f.write(str(simTime)+','+str(self.idx)+','+str(self.item.getIdx())+','+str(self.item.getImportance())+','+str(self.position.getIdx())+','+str(self.destination.getIdx())+','+str(event)+'\n')
			else:
				f.write(str(simTime)+','+str(self.idx)+','+str(-1)+','+str(-1)+','+str(self.position.getIdx())+','+str(self.destination.getIdx())+','+str(event)+'\n')
		
	def getLocation(self):
		return self.position
		
	def setLocation(self, room):
		self.position = room
		self.space.setRobotPosition(self, room)
		
	def setDestination(self, room):
		self.destination = room
		
	def canLoadItem(self):
		if not self.isHealthy():
			return False
		if len(self.space.getItemsByImportance(imp=-1, room=self.position)) == 0:
			return False
		if self.isFree():
			return True
		if not self.isFree():
			currImp = self.item.getImportance()
			impItems = self.space.getItemsWithMoreImportance(imp=currImp, room=self.position)
			if len(impItems) == 0:
				return False
			else:
				return True
		
	def move(self, simTime):
#		print(str(self.getIdx()) + ' --> ' + str([r.getIdx() for r in self.optRoute]) + ' at ' + str(simTime))
		if len(self.optRoute) == 0:
			print('[ERROR] Robot ' + str(self.getIdx()) + ' cannot go anywhere and it is stuck in Room ' + str(self.position.getIdx()))
			sys.exit(-1)
		nextRoom = self.optRoute[0]
		self.optRoute.remove(nextRoom)
		self.setLocation(nextRoom)
		if LOG_MOVE:
			self.logEvent(simTime, 'move')
		if self.destination == nextRoom and not self.isFree():
			self.dropItem(simTime)
			self.memoryItem = None
		if self.fail(simTime): # If the robot fails
			self.space.getClock().scheduleEvent('recovery-' + str(self.getIdx()), [RECOVERY_TIME], [RECOVERY_TRACE], [RECOVERY_DISTR])
			self.memoryItem = None
		elif self.memoryItem != None: # Else if the robot came to help
			if self.memoryItem[0].getImportance() > self.space.getMaxImportance(room=nextRoom): # if there is not an item more important than the old one
				self.optRoute =  self.space.findRoute(self.position, self.memoryItem[1], strategy=FIND_ROUTE_STRATEGY)
				self.space.getClock().scheduleEvent('move-' + str(self.getIdx()), [MOVEMENT_TIME], [MOVEMENT_TRACE], [MOVEMENT_DISTR])
			else: # if there is an item more important than the old one
				self.loadItem(self.space.getMoreImportantItem(room=nextRoom), simTime)	
			self.memoryItem = None
		elif self.canLoadItem(): # Else if there is a new item that can be load by the robot
			self.loadItem(self.space.getMoreImportantItem(room=nextRoom), simTime)
		elif len(self.optRoute) == 0 and self.isFree() and self.position != self.space.getSource(): # Else if the robot is in a room with no further information
			self.destination = self.space.getSource()
			self.optRoute = self.space.findRoute(self.position, self.destination, strategy=FIND_ROUTE_STRATEGY)
			self.space.getClock().scheduleEvent('move-' + str(self.getIdx()), [MOVEMENT_TIME], [MOVEMENT_TRACE], [MOVEMENT_DISTR])
		elif not (self.isFree() and self.position == self.space.getSource()): # Else if the robot is neither empty nor in the source room
			self.space.getClock().scheduleEvent('move-' + str(self.getIdx()), [MOVEMENT_TIME], [MOVEMENT_TRACE], [MOVEMENT_DISTR])
		if self.isHealthy() and self.malicious and MALICIOUS_FAKE_FAILURES and not np.random.uniform() < COMM_FAIL_PROB: #If the robot is healthy AND it is malicious AND malicious behavior is enabled AND communication has not failed 
			self.fakeFailure(nextRoom, simTime)
			
			
	def fail(self, simTime):
		if np.random.uniform() < self.failureProb:
			self.healthy = False
			if LOG_FAIL:
				self.logEvent(simTime, 'fail')
			if self.item != None:
				itemToDrop = self.item
				self.dropItem(simTime)
				if not np.random.uniform() < COMM_FAIL_PROB: #Look for help only if communication has not failed
					if ARCHITECTURE == 'semi-decentralized':
						if not self.malicious:
							self.sendMessageToPeers(itemToDrop.getImportance(), self.position, simTime)
						else: # If the robot is malicious send a message containing the max importance independently of the actual importance of the carried item
							maxImportance = len(IMPORTANCE_PROBABILITIES) + 1
							self.sendMessageToPeers(maxImportance, self.position, simTime)
					elif 'centralized-' in ARCHITECTURE:
						controller_strategy = ARCHITECTURE.split('-')[1]
						if not self.malicious:
							self.sendMessageToMaster(itemToDrop.getImportance(), self.position, simTime, controller_strategy)
						else:
							maxImportance = len(IMPORTANCE_PROBABILITIES) + 1
							self.sendMessageToMaster(maxImportance, self.position, simTime, controller_strategy)
			return True
		return False
		
	def recovery(self, simTime):
		self.healthy = True
		self.position = self.space.getSource()
		self.space.setRobotPosition(self, self.position)
		self.destination = self.space.getSource()
		self.optRoute = []
		if LOG_RECOVERY:
			self.logEvent(simTime, 'recover')
		if self.canLoadItem():
			self.loadItem(self.space.getMoreImportantItem(room=self.position), simTime)
			
	
	def sendMessageToPeers(self, itemImportance, position, simTime, fake=False):
		nearRobots = self.space.getNearRobots(self)
		if LOG_HELP and not fake:
			self.logEvent(simTime, 'help')
#		print('--> ' + str(self.getIdx()) + ' from Room ' + str(self.position.getIdx()) + ' asks to ' + str([bot.getIdx() for bot in nearRobots]) + ' at ' + str(simTime))
		### Ask for help to all near robots ###
#		for robot in nearRobots:
#			robot.abortMission(itemImportance, position, simTime)
		#######################################
		### Ask for help to only one close robot with the smallest importance ###
		nearRobotsMinImp = self.space.getRobotsByImportance(self, nearRobots, itemImportance)
		if len(nearRobotsMinImp) == 0:
			return None
		helper = random.choice(nearRobotsMinImp)
		helper.abortMission(itemImportance, position, simTime)
		##################################################################
			
			
	def sendMessageToMaster(self, itemImportance, position, simTime, strategy, fake=False):
		if LOG_HELP and not fake:
			self.logEvent(simTime, 'help')
		if strategy == 'proximity':
			robotsStepOne = self.space.getRobotsByProximity(self, self.space.getAllRobots(), position)
			if len(robotsStepOne) > 0:
				robotsStepTwo = robotsStepOne
			else:
				return None
		elif strategy == 'importance':
			robotsStepOne = self.space.getRobotsByImportance(self, self.space.getAllRobots(), itemImportance)
			if len(robotsStepOne) > 0:
				robotsStepTwo = robotsStepOne
			else:
				return None	
		elif strategy == 'proximp':
			robotsStepOne = self.space.getRobotsByProximity(self, self.space.getAllRobots(), position)
			if len(robotsStepOne) > 0:
				robotsStepTwo = self.space.getRobotsByImportance(self, robotsStepOne, itemImportance)
			else:
				return None		
		elif strategy == 'impprox':
			robotsStepOne = self.space.getRobotsByImportance(self, self.space.getAllRobots(), itemImportance)
			if len(robotsStepOne) > 0:
				robotsStepTwo = self.space.getRobotsByProximity(self, robotsStepOne, position)
			else:
				return None	
		else:
			print('The Coordinator does not support this strategy')
			sys.exit(-1)
#		print(simTime, self.getIdx(), '-->', [bot.getIdx() for bot in robotsStepOne], [bot.getIdx() for bot in robotsStepTwo])
		if len(robotsStepTwo) > 0:
				helper = random.choice(robotsStepTwo)
				helper.abortMission(itemImportance, position, simTime)
			
			
	def fakeFailure(self, position, simTime):
		if LOG_FAKE:
			self.logEvent(simTime, 'fakeFailure')
		if ARCHITECTURE == 'semi-decentralized':
			maxImportance = len(IMPORTANCE_PROBABILITIES) + 1
			self.sendMessageToPeers(maxImportance, self.position, simTime, fake=True)
		if 'centralized-' in ARCHITECTURE:
			controller_strategy = ARCHITECTURE.split('-')[1]
			maxImportance = len(IMPORTANCE_PROBABILITIES) + 1
			self.sendMessageToMaster(maxImportance, self.position, simTime, controller_strategy, fake=True)
			
			
	def abortMission(self, newItemImportance, helpRoom, simTime):
		if LOG_RESCUE:
			self.logEvent(simTime, 'rescue')
		if helpRoom == self.position:
			if self.canLoadItem():
#				print('same room ==> ' + str(self.getIdx()) + ' aborts at ' + str(simTime) + ' [move-' + str(self.getIdx()) + ']')
				self.space.getClock().removeEvent('move-' + str(self.getIdx()))
				self.loadItem(self.space.getMoreImportantItem(room=self.position), simTime)
		elif self.getItemImportance() < newItemImportance and self.isHealthy():
			if len(self.optRoute) == 0 or helpRoom != self.optRoute[0]:
				if not self.isFree():
					self.memoryItem = [self.item, self.position]
					self.dropItem(simTime)
#				print('different room ==> ' + str(self.getIdx()) + ' aborts at ' + str(simTime) + ' [move-' + str(self.getIdx()) + ']')
				self.space.getClock().removeEvent('move-' + str(self.getIdx()))
				self.destination = helpRoom
				self.optRoute = self.space.findRoute(self.position, self.destination, strategy=FIND_ROUTE_STRATEGY)
				self.space.getClock().scheduleEvent('move-' + str(self.getIdx()), [MOVEMENT_TIME], [MOVEMENT_TRACE], [MOVEMENT_DISTR])
			
			
		
	

			
			
class Room:
	idx = -1
	source = False
	adjacents = [] # Adjacent rooms are other rooms that are connected to the current one
	
	def __init__(self, idx):
		self.idx = idx
		
	def setSource(self):
		self.source = True
		
	def isSource(self):
		return self.source
		
	def setAdjacentRooms(self, adjRooms):
		self.adjacents = adjRooms			
		
	def getAdjacentRooms(self):
		return self.adjacents
		
	def getRandomAdjacent(self):
		return random.choice(self.adjacents)
		
	def isAdjacent(self, room):
		if room in self.adjacents:
			return True
		else:
			return False
			
	def getIdx(self):
		return self.idx
		
	def getProximity(self):
		proximityDict = {}
		q = queue.Queue()
		q.put([self, 0]) #[Room, Distance]
		while not q.empty():
			next = q.get()
			room = next[0]
			dist = next[1]
			if room not in proximityDict.keys():
				proximityDict[room] = dist
				for r in room.adjacents:
					q.put([r, dist+1])
		return proximityDict
			
			
class Space:
	source = None
	rooms = []
	connections_dict = []
	availItems = []
	movingItems = []
	robotPositionDict = {}
	clock = None
	
	def __init__(self, rooms, connection_dict, clock, source=None):
		self.rooms = rooms
		self.connections_dict = connection_dict
		self.clock = clock
		
		if source == None:
			print('[ERROR] You must provide a source')
			sys.exit(-1)
			
		self.source = source
		self.source.setSource()
		
		for	i in connection_dict.keys():
			adjList = [rooms[j] for j in connection_dict[i]]
			rooms[i].setAdjacentRooms(adjList)
				
#		for room, connection in zip(rooms, connections):
#			room.setAdjacentRooms(connection)
			
		#TODO: Check that Source is someway connected to all other rooms, otherwise exit(-1)
			
	def getSource(self):
		return self.source
		
	def getRooms(self):
		return self.rooms
		
	def getClock(self):
		return self.clock
		
	def getAllRobots(self):
		return list(self.robotPositionDict.keys())
		
	def newItem(self, item):
		self.availItems.append(item)
		impIdx = item.getImportance()
		expireTime = EXPIRATION_TIME[impIdx]
		if expireTime != -1:
			expireDistr = EXPIRATION_DISTR[impIdx]
			self.clock.scheduleEvent('expire-' + str(item.getIdx()), [expireTime], [expireDistr])
		self.clock.scheduleEvent('item', [ITEM_SPAWNING_TIME], [ITEM_SPAWNING_TRACE], [ITEM_SPAWNING_DISTR])

#	def getItem(self, idx):
#		return self.availItems[idx]

	def getItembyId(self, idx):
		allItems = self.availItems + self.movingItems
		for item in allItems:
			if item.getIdx() == idx:
				return item
		print('[ERROR] There is not an item with ID ' + str(idx))
		sys.exit(-1)
		
	def getItemsByImportance(self, imp=-1, room=None):
		if room == None:
			if imp == -1:
				return self.availItems
			else:
				return [item for item in self.availItems if item.getImportance() == imp]
		else:
			if imp == -1:
				return [item for item in self.availItems if item.getLocation() == room]
			else:
				return [item for item in self.availItems if item.getImportance() == imp and item.getLocation() == room]
			
	def getItemsWithMoreImportance(self, imp=-1, room=None):
		if room == None:
			if imp == -1:
				return self.availItems
			else:
				return [item for item in self.availItems if item.getImportance() > imp]
		else:
			if imp == -1:
				return [item for item in self.availItems if item.getLocation() == room]
			else:
				return [item for item in self.availItems if item.getImportance() > imp and item.getLocation() == room]
				
	def getMoreImportantItem(self, room=None):
		maxImp = -1
		output = None
		if room == None:
			allAvailItems = self.availItems
		else:
			allAvailItems = [item for item in self.availItems if item.getLocation() == room]
		for item in allAvailItems:
			currImp = item.getImportance()
			if currImp > maxImp:
				maxImp = currImp
				output = item
		return output
		
	def getMaxImportance(self, room=None):
		moreImportantItem = self.getMoreImportantItem(room)
		if moreImportantItem == None:
			return -1
		else:
			return moreImportantItem.getImportance()
			
#	def getItemsByLocation(self, room):
#		return [item for item in self.availItems if item.getLocation() == room]
			
	def deliverItem(self, item):
		self.clock.removeEvent('expire-' + str(item.getIdx()) + '-'  + str(item.getImportance()))
		self.movingItems.remove(item)
		
	def expireItem(self, item, simTime):
		if LOG_EXPIRE:
			item.logEvent(simTime, 'expire')
		if item in self.availItems:
			self.availItems.remove(item)
		elif item in self.movingItems:
			self.movingItems.remove(item)
			bot = item.getUber()
			bot.dropItem(simTime, itemExpired=True)
		else:
			print('[ERROR] The expired item does not exist')
			sys.exit(-1)
		
	def switchItem(self, item):
		if item in self.availItems:
			self.availItems.remove(item)
			self.movingItems.append(item)
		elif item in self.movingItems:
			self.movingItems.remove(item)
			self.availItems.append(item)
		else:
			print('[ERROR] The switched item does not exist')
			sys.exit(-1)

	def findAllRoutesDFS(self, start, target, visited=[], routes={}):
		visited = [*visited, start]
		if start == target:
			routes[str([room.getIdx() for room in visited])] = len(visited) - 1
		else:
			adjs = start.getAdjacentRooms()
			for room in adjs:
				if room not in visited:
					routes = self.findAllRoutesDFS(room, target, visited=visited, routes=routes)
		return routes
    
    
	def findAllRoutesBFS(self, start, target):
		q = queue.Queue()
		q.put([start])
		routes = {}
		while not q.empty():
			roomList = q.get()
			if target in roomList:
				cost = len(roomList) - 1
				if len(routes.keys()) == 0:
					routes[str([room.getIdx() for room in roomList])] = cost
				elif cost == min(routes.values()):
					routes[str([room.getIdx() for room in roomList])] = cost
				elif cost < min(routes.values()):
					routes = {}
					routes[str([room.getIdx() for room in roomList])] = cost
			elif len(routes.keys()) == 0:
				for adj in roomList[-1].getAdjacentRooms():
					if adj not in roomList:
						q.put(roomList + [adj])
		return routes


	def findRoute(self, start, target, strategy='breadth'):
		if strategy == 'breadth':
			routes = self.findAllRoutesBFS(start, target)
			possibleRoutes = list(routes.keys())
		elif strategy == 'depth':
			routes = self.findAllRoutesDFS(start, target, visited=[], routes={})
			possibleRoutes = []
			minCost = min(routes.values())
			for route, cost in routes.items():
				if cost == minCost:
					possibleRoutes.append(route)
		else:
			print('[ERROR] This strategy for finding routes is not supported')
			sys.exit(-1)
		if len(possibleRoutes) == 0:
			print('[ERROR] No route between ' + str(start.getIdx()) + ' and ' + str(target.getIdx()))
			sys.exit(-1)
		chosenRoute = random.choice(possibleRoutes)
		chosenRoute = chosenRoute[1:-1] #Remove parenthesis from the string
		chosenRoute = chosenRoute.split(', ')[1:] #Create a list of room IDs and pass all rooms but the first one (i.e., the current one)
		return [self.rooms[int(idx)] for idx in chosenRoute] #Return the rooms
		
	def setRobotPosition(self, robot, robotPosition):
		self.robotPositionDict[robot] = robotPosition
		
	def getRobotPosition(self, robot):
		return self.robotPositionDict[robot]
		
	def getNearRobots(self, askingRobot):
		targetRoom = askingRobot.getLocation()
		robots = list(self.robotPositionDict.keys())
		nearRobots = []
		for idx, room in enumerate(self.robotPositionDict.values()):
			bot = robots[idx]
			if bot != askingRobot:
				if room.isAdjacent(targetRoom) or room == targetRoom:
					nearRobots.append(robots[idx])
#		print('--> Room: ' + str(targetRoom.getIdx()) + ' - Receiver: ' + str([bot.getIdx() for bot in nearRobots]))
		return nearRobots
		
	def getRobotsByImportance(self, askingRobot, bots, itemImportance):
		if askingRobot in bots:
			bots.remove(askingRobot)
		minImp = itemImportance
		for bot in bots:
			if bot.isHealthy():
				currImp = bot.getItemImportance()
				if currImp == -1:
					minImp = currImp
					break
				elif currImp < minImp:
					minImp = currImp
		output = []
		if minImp >= itemImportance:
			return []
		for bot in bots:
			if bot.getItemImportance() == minImp and bot.isHealthy():
				output.append(bot)
#		print('importance ==>', [bot.getIdx() for bot in output], minImp)
		return output

#	def getRobotsByLocation(self, room):
#		outputRobots = []
#		for bot in self.robotPositionDict.keys():
#			if robotPositionDict[bot] == room:
#				outputRobots.append(bots)
#		return outputRobots
				
#	def getRobotsByProximity(self, askingRobot, targetRoom, bots):
#		proximityMap = targetRoom.getProximity()
#		maxHops = max(proximityMaps.values())
#		for hop in range(maxHops+1):
#			bots = []
#			for room in rooms:
#				if proximityMap[room] == hop:
#					bots += self.getRobotsByLocation(room)
#					if askingRobot in bots:
#						bots.remove(askingRobot)
#			if len(bots) > 0:
#				break
#		return bots
		
	def getRobotsByProximity(self, askingRobot, bots, targetRoom):
		if askingRobot in bots:
			bots.remove(askingRobot)
		proximityMap = targetRoom.getProximity()
		minHops = N_ROOMS
		for bot in bots:
			if bot.isHealthy():
				currHops = proximityMap[bot.getLocation()]
				if currHops == 0:
					minHops = 0
					break
				elif currHops < minHops:
					minHops = currHops
		output = []
		for bot in bots:
			if proximityMap[bot.getLocation()] == minHops and bot.isHealthy():
				output.append(bot)
#		print('proximity ==>', [bot.getIdx() for bot in output], minHops)
		return output
		
		







def logSimulationTime(simTime):
	path = SIMTIME_LOGFILE.split('/')
	filename = path[-1]
	dirname = ''
	for p in path[:-1]:
		dirname += p + '/'
	if not filename in os.listdir(dirname):
		with open(SIMTIME_LOGFILE, 'w') as f:
			f.write('arch,space,Nrooms,Nbot,Nmal,failProb,commFailProb,arrival,loadItem,moveItem,dropItem,comp,comm,recovery,simTime\n')
	with open(SIMTIME_LOGFILE, 'a') as f:
		f.write(str(ARCHITECTURE) + ',' + str(TOPOLOGY_NAME) + ',' + str(N_ROOMS) + ',' + str(N_ROBOTS) + ',' + str(N_MALICIOUS) + ',' + str(FAIL_PROB*100) + ',' + str(COMM_FAIL_PROB*100) + ',' + str(ITEM_SPAWNING_TIME) + ',' + str(LOAD_TIME) + ',' + str(MOVEMENT_TIME) + ',' + str(DROP_TIME) +  ',' + str(COMP_TIME) +  ',' + str(COMM_TIME) + ',' + str(RECOVERY_TIME) + ',' + str(simTime) + '\n')

def getLogfileName():
	filename = os.path.dirname(os.path.realpath(__file__)) + '/results/'
	if ARCHITECTURE == 'decentralized':
		filename += 'fully_'
	elif ARCHITECTURE == 'semi-decentralized':
		filename += 'semi_'
	elif ARCHITECTURE == 'centralized-importance':
		filename += 'centralizedImp_'
	elif ARCHITECTURE == 'centralized-proximity':
		filename += 'centralizedProx_'
	elif ARCHITECTURE == 'centralized-proximp':
		filename += 'centralizedProxImp_'
	else:
		filename += 'centralizedImpProx_'
	filename += TOPOLOGY_NAME + '_Nbot'
	filename += str(N_ROBOTS) + '_Nmal'
	filename += str(N_MALICIOUS) + '_p'
	filename += str(int(FAIL_PROB*100)) + 'pc_cmF'
	filename += str(int(COMM_FAIL_PROB*1000)) + 'pm_A'
	filename += str(int(ITEM_SPAWNING_TIME)) + '_L'
	filename += str(int(LOAD_TIME)) + '_M'
	filename += str(int(MOVEMENT_TIME)) + '_D'
	filename += str(int(DROP_TIME)) + '_cp'
	filename += str(int(COMP_TIME)) + '_cm'
	filename += str(int(COMM_TIME)) + '_R'
	filename += str(int(RECOVERY_TIME))
	return filename + '.csv'
	
def getTargetRoom(rooms):
	if TARGETS == -1:
		return None
	if max(TARGETS) >= len(rooms):
		print('[ERROR] There are more Target rooms than rooms')
		sys.exit(-1)
	while SOURCE in TARGETS:
		TARGETS.remove(SOURCE)
	roomIdx = random.choice(TARGETS)
	return rooms[roomIdx]
