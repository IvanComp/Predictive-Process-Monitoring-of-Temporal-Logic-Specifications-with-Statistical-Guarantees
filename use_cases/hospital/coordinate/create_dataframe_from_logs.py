import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats

########################
### Global Variables ###
########################

NUM_WEEKS_INIT = 0
MIN_SIM_TIME = NUM_WEEKS_INIT*7*24*3600 #Start observing the system after NUM_WEEKS_INIT weeks
CONF_INT = 0.95

ARCHITECTURES = ['decentralized', 'semi-decentralized', 'centralized-impprox'] #Coordination mechanisms that have been simulated
SPACES = ['GUH73'] #Topologies that have been simulated
PROBS = [5] #Failure probabilities that have been simulated
COMM_FAIL_PROBS = [3] #Probability (permille) that a message is lost
NUM_BOTS = [20] #Number of robots that have been simulated
PERC_MALS = [0.9] #Percentages of malicious robots that have been simulated
ARRIVALS = [30*i for i in range(3,11,1)] #Inter-arrival times that have been simulated
LOADS = [1] #Load times that have been simulated
MOVES = [5] #Move times that have been simulated
DROPS = [1] #Drop times that have been simulated
COMPS = [100] #Computation time in msec
COMMS = [30] #Communication time in msec
RECOVERIES = [1800] #Recovery times that have been simulated
IMPS = [-1, 0, 1, 2] #Importances that have been simulated (-1 is for all importances aggregated)

DF_NAME = 'LatVsArrival'
LOGS_DIR = './GUH_interArr/'





# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd='\r'):
    """
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()






total = len(SPACES) * len(ARCHITECTURES) * len(PROBS) * len(COMM_FAIL_PROBS) * len(NUM_BOTS) * len(PERC_MALS) * len(ARRIVALS) * len(LOADS) * len(MOVES) * len(DROPS) * len(COMPS) * len(COMMS) * len(RECOVERIES) * len(IMPS)

df = pd.DataFrame(columns=['space', 'arch', 'failProb_%', 'commFailProb_‰', 'Nbot', 'Nmal', 'load', 'comp', 'comm', 'itemImp', 'latency', 'latency_low', 'latency_up', 'items_created', 'items_delivered', 'items_expired', 'throughput'])
idx = 0

for arch in ARCHITECTURES:
    for space in SPACES:
        for Nbot in NUM_BOTS:
            for perc_mal in PERC_MALS:
                Nmal = int(Nbot * perc_mal)
                for prob in PROBS:
                    for commProb in COMM_FAIL_PROBS:
                        for arrival in ARRIVALS:
                            for load in LOADS:
                                for move in MOVES:
                                    for drop in DROPS:
                                        for comp in COMPS:
                                            for comm in COMMS:
                                                for recovery in RECOVERIES:
                                                    dfTmp = pd.read_csv('./results/' + arch + '_' + space + '_Nb' + str(Nbot)
                                                                        + '_Nm' + str(Nmal) + '_p' + str(int(prob))
                                                                        + 'pc_cmF' + str(commProb) + 'pm_A' + str(arrival) + '_L' + str(load)
                                                                        + '_M' + str(int(move)) + '_D' + str(drop) 
                                                                        + '_cp' + str(comp) + 'ms_cm' + str(comm)
                                                                        + 'ms_R' + str(recovery) + '_r0.csv')
                                        dfTmp = dfTmp[dfTmp['simTime']>=MIN_SIM_TIME]
                                        obsTime = dfTmp['simTime'].max() - MIN_SIM_TIME
                        
                                        for imp in IMPS:

                                            if imp >= 0:
                                                dfCreate = dfTmp[(dfTmp['event']=='create') & (dfTmp['itemImportance']==imp)][['itemId', 'simTime']]
                                                dfDeliver = dfTmp[(dfTmp['event']=='deliver') & (dfTmp['itemImportance']==imp)][['itemId', 'simTime']]
                                                numCreated = dfCreate.shape[0]
                                                numExpired = dfTmp[(dfTmp['event']=='expire') & (dfTmp['itemImportance']==imp)].shape[0]
                                                numDelivered = dfDeliver.shape[0]
                                            else:
                                                dfCreate = dfTmp[(dfTmp['event']=='create')][['itemId', 'simTime']]
                                                dfDeliver = dfTmp[(dfTmp['event']=='deliver')][['itemId', 'simTime']]
                                                numCreated = dfCreate.shape[0]
                                                numExpired = dfTmp[(dfTmp['event']=='expire')].shape[0]
                                                numDelivered = dfDeliver.shape[0]

                                            dfLat = dfCreate.merge(dfDeliver, how='inner', left_on='itemId', right_on='itemId', suffixes=('_start', '_end'))
                                            dfLat['latency'] = dfLat['simTime_end'] - dfLat['simTime_start']

                                            avg = np.mean(dfLat['latency'].values)
                                            std = np.std(dfLat['latency'].values)
                                            z = stats.norm.ppf(CONF_INT+(1-CONF_INT)/2)
                                            ci = z * (std/np.sqrt(dfLat.shape[0]))
                                            ci_low = avg - ci
                                            ci_up = avg + ci        

                                            df.loc[idx] = [space, arch, prob, Nbot, Nmal, arrival, imp, avg, ci_low, ci_up, numCreated, numDelivered, numExpired, numDelivered/obsTime]

                                            idx += 1

                                            printProgressBar(idx, total, prefix='Generating', suffix='Completed', decimals=2, length=50)
                            
df[['failProb_%', 'commFailProb_‰', 'Nbot', 'Nmal', 'load', 'comp', 'comm', 'itemImp', 'items_created', 'items_delivered', 'items_expired']] = df[['failProb_%', 'commFailProb_‰', 'Nbot', 'Nmal', 'load', 'comp', 'comm', 'itemImp', 'items_created', 'items_delivered', 'items_expired']].astype('int')
df.to_csv('./results/' + DF_NAME + '.csv', index=False)
