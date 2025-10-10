from environment_maps import *

SIM_TIME = 3 * 30 * 24 * 3600

LOGFILE = ''
SIMTIME_LOGFILE = './results/simTime.csv'
LOG_ITEM = True #An item is created
LOG_DELIVERY = True #An item is delivered
LOG_LOAD = False #An item is load on a Robot
LOG_DROP = False #An item is dropped because of a robot failure
LOG_EXPIRE = True #An item expires
LOG_MOVE = False #A robot move to the next room
LOG_FAIL = False #A robot breaks
LOG_RECOVERY = False #A robot is recovered
LOG_HELP = False #A robot send a "help" message in the semi-decentralized architecture
LOG_FAKE = False #A malicious robot fakes its failure
LOG_RESCUE = False #A robot tries to help another robot that said it has failed


ARCHITECTURE = '<arch>' # This can be: 1) decentralized; 2) semi-decentralized; 3) centralized-<strategy> (<strategy> = {proximity, importance, proximp, impprox})


N_ROOMS = int('<Nroom>')
SOURCE = 0
TARGETS = -1 # A list with the ID of rooms where an object can be delivered. If the SOURCE is in this list, it will be removed before starting the simulation. Use -1 for all rooms except the source (same probability). Use the same ID multiple times if a room is more likely to be selected as item destination than others, e.g., [1,2,2,2] means that items are three times more likely to be delivered in room 2 than room 1.
TOPOLOGY_NAME = '<topology>'
TOPOLOGY = ["mesh4"]

ITEM_SPAWNING_TIME = int('<arrival>')
ITEM_SPAWNING_TRACE = '<arrival_trace>'
ITEM_SPAWNING_DISTR = 'exponential'
IMPORTANCE_PROBABILITIES = [0.5, 0.1, 0.4] # Probability of having items with the importance given by the position in the list
EXPIRATION_TIME = [-1, -1, -1]
EXPIRATION_DISTR = ['exponential', 'exponential', 'exponential']

N_ROBOTS = int('<Nbot>')
N_MALICIOUS = int('<Nmal>')
MALICIOUS_FAKE_FAILURES = True
FIND_ROUTE_STRATEGY = 'breadth' # This is 'breadth' (Breadth-First-Search) or 'depth' (Depth-First-Search)
FAIL_PROB = float('<prob>')
COMM_FAIL_PROB = float('<comm_fail_prob>')
LOAD_TIME = float('<load>')
LOAD_TRACE = '<load_trace>'
LOAD_DISTR = 'exponential'
MOVEMENT_TIME = float('<move>')
MOVEMENT_TRACE = '<move_trace>'
MOVEMENT_DISTR = 'exponential'
DROP_TIME = float('<drop>')
DROP_TRACE = '<drop_trace>'
DROP_DISTR = 'exponential'
COMP_TIME = float('<comp>')
COMP_TRACE = '<comp_trace>'
COMP_DISTR = 'exponential'
COMM_TIME = float('<comm>')
COMM_TRACE = '<comm_trace>'
COMM_DISTR = 'exponential'
RECOVERY_TIME = float('<recovery>')
RECOVERY_TRACE = '<recovery_trace>'
RECOVERY_DISTR = 'exponential'
