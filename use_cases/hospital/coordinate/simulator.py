from utils import *
from params import *
import time
import random
		

startSim = time.time()

# Check that the architecture is admitted
if ARCHITECTURE != 'decentralized' and ARCHITECTURE != 'semi-decentralized' and ARCHITECTURE != 'centralized-proximity' and ARCHITECTURE != 'centralized-importance' and ARCHITECTURE != 'centralized-proximp' and ARCHITECTURE != 'centralized-impprox':
	print('This architecture is not supported')
	sys.exit(-1)
	
if N_ROOMS != len(TOPOLOGY.keys()):
	print('The number of rooms defined in TOPOLOGY does not match the one given in N_ROOMS')
	sys.exit(-1)

if LOGFILE == '':
	LOGFILE = getLogfileName()

# Initialize the clock
clock = Clock()


# Create the rooms
rooms = []
for i in range(N_ROOMS):
	rooms.append(Room(i))
	
itemIdx = 0

# Create a Space
space = Space(rooms, TOPOLOGY, clock, source=rooms[SOURCE])


# Create robots
robotIdx = 0
bots = []
for i in range(N_ROBOTS):
	if robotIdx < N_MALICIOUS:
		bots.append(Robot(robotIdx, True, space, LOGFILE))
	else:
		bots.append(Robot(robotIdx, False, space, LOGFILE))
	robotIdx += 1
botsRandomOrder = bots.copy()


# Initialize the simulation
clock.scheduleEvent('item', [ITEM_SPAWNING_TIME], [ITEM_SPAWNING_TRACE],  [ITEM_SPAWNING_DISTR])


while clock.getTime() < SIM_TIME:
	clock.checkClock()
	ts, event = clock.getNextEvent()
	if event == 'item':
		space.newItem(Item(LOGFILE, itemIdx, space, ts, imp=-1, target=getTargetRoom(rooms)))
		itemIdx += 1
		random.shuffle(botsRandomOrder) 
		for bot in botsRandomOrder:
			if bot.getLocation() == space.getSource() and bot.isFree() and bot.isHealthy() and not bot.hasOtherTasks():
				item = space.getMoreImportantItem(room=space.getSource())
				bot.loadItem(item, clock.getTime())
				break
	elif 'move' in event:
		idx = int(event.split('-')[1])
		bot = bots[idx]
		bot.move(ts)
	elif 'recovery' in event:
		idx = int(event.split('-')[1])
		bot = bots[idx]
		bot.recovery(ts)
	elif 'expire' in event:
		idx = int(event.split('-')[1])
		item = space.getItembyId(idx)
		space.expireItem(item, ts)
		
endSim = time.time()
simTime = endSim - startSim
logSimulationTime(simTime)
print(LOGFILE.split('/')[-1] + ' --> Simulation time: ' + str(simTime))

