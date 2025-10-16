# params.py — Single Source of Truth (COMPLETO)

from environment_maps import *  # importa ghent73 e topologyName_dict

# ---------- SPAZIO / TOPOLOGIA ----------
TOPOLOGY_NAME = "GUH73"   # chiave nel dizionario
try:
    TOPOLOGY = topologyName_dict[TOPOLOGY_NAME]
except Exception:
    TOPOLOGY = ghent73  # fallback

# numero stanze robusto a dict/list
try:
    N_ROOMS = len(TOPOLOGY.keys())
except Exception:
    try:
        N_ROOMS = len(TOPOLOGY)
    except Exception:
        N_ROOMS = 4  # fallback coerente con Ghent

SOURCE  = 0      # pharmacy
TARGETS = -1     # -1 = tutte tranne SOURCE (uniforme)

# ---------- FINESTRA DI OSSERVAZIONE ----------
SIM_TIME = 1 * 30 * 24 * 3600  # ~3 mesi (in secondi)

# ---------- WORKLOAD (ARRIVI & PRIORITÀ) ----------
ITEM_SPAWNING_DISTR = 'exponential'  # 'exponential' | 'deterministic' | 'trace'
ITEM_SPAWNING_TIME  = 120.0          # media inter-arrivo (s) — scegli 90/120/300
ITEM_SPAWNING_TRACE = ''             # file traccia se usi 'trace' (stringa vuota = off)

# mix importanza L/M/H
IMPORTANCE_PROBABILITIES = [0.5, 0.1, 0.4]

# scadenze (disabilitate come da tua tabella)
EXPIRATION_DISTR = 'none'            # oppure 'exponential' se abiliti
EXPIRATION_TIME  = [-1, -1, -1]      # -1 = no-expire per L/M/H
EXPIRATION_TRACE = ''                # se 'trace'

# ---------- AGENTI ----------
N_ROBOTS      = 20
N_MALICIOUS   = 0
MALICIOUS_FAKE_FAILURES = True   # i malevoli fingono failure (relevante in SD/CE)
FIND_ROUTE_STRATEGY     = 'breadth'  # 'breadth' (BFS) | 'depth' (DFS)

# affidabilità
FAIL_PROB      =0.10
#FAIL_PROB      =0.0
RECOVERY_TIME  = 1800.0
RECOVERY_DISTR = 'exponential'
RECOVERY_TRACE = ''

# ---------- TEMPI DI AZIONE ----------
# LOAD
LOAD_TIME   = 1.0
LOAD_DISTR  = 'exponential'
LOAD_TRACE  = ''

# MOVEMENT
MOVE_TIME      = 5.0    # per hop se il modello è ad hop
MOVEMENT_TIME  = MOVE_TIME      # alias
MOVEMENT_DISTR = 'exponential'
MOVEMENT_TRACE = ''

# DROP (rilascio/consegna)
DROP_TIME   = 1.0
DROP_DISTR  = 'exponential'
DROP_TRACE  = ''

# ---------- OVERHEAD (decisione/comunicazione) ----------
COMP_TIME   = 2.0
COMP_DISTR  = 'exponential'
COMP_TRACE  = ''

COMM_TIME   = 0.5
COMM_DISTR  = 'exponential'
COMM_TRACE  = ''
#COMM_FAIL_PROB = 0.0
COMM_FAIL_PROB = 0.10

# ---------- LOGGING ----------
# directory results/ deve esistere
LOGFILE         = './results/test.csv'     # log eventi (item, move, ecc.)
SIMTIME_LOGFILE = './results/simTime.csv'  # tempo di simulazione (se usato dal codice)

LOG_ITEM     = True  # An item is created
LOG_DELIVERY = True  # An item is delivered
LOG_LOAD     = True  # Item loaded
LOG_DROP     = True  # Item dropped due to failure
LOG_EXPIRE   = True  # Item expires
LOG_MOVE     = True  # Robot moves
LOG_FAIL     = True  # Robot breaks
LOG_RECOVERY = True  # Robot recovered
LOG_HELP     = True  # Help message (SD)
LOG_FAKE     = True  # Fake failure (malicious)
LOG_RESCUE   = True  # Rescue attempt

# ---------- MECCANISMO DI COORDINAMENTO ----------
# Valori ammessi dal simulatore (in base ai tuoi nomi cartella/log):
#  'decentralized'           → FD
#  'semi-decentralized'      → SD
#  'centralized-impprox'     → CE (importance→proximity)
#  'centralized-proximp'     → CE (proximity→importance)
ARCHITECTURE = 'centralized-impprox'    # il runner lo sovrascriverà a runtime
CE_STRATEGY  = 'imp-prox'         # se il codice lo usa direttamente

# ---------- ALIAS (compat per nomi alternativi che ho visto nei tuoi log/codice) ----------
# counts
N_BOTS       = N_ROBOTS
N_MAL_BOTS   = N_MALICIOUS
N_agent      = N_ROBOTS
N_malicious  = N_MALICIOUS

# tempi (alias “T_*” se qualche punto del codice li usa)
T_load   = LOAD_TIME
T_move   = MOVE_TIME
T_drop   = DROP_TIME
T_comp   = COMP_TIME
T_comm   = COMM_TIME
T_repair = RECOVERY_TIME

# failure (alias “F_*”)
F_agent  = FAIL_PROB
F_msg    = COMM_FAIL_PROB

# meccanismo alias (se da qualche parte cercano COORD_MECH)
COORD_MECH = {
    'decentralized':        'FD',
    'semi-decentralized':   'SD',
    'centralized-impprox':  'CE',
    'centralized-proximp':  'CE'
}.get(ARCHITECTURE, 'FD')
