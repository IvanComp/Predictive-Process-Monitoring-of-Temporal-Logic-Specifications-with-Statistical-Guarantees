# Time Robustness for Point-Based Semantics of Metric Interval Temporal Logic

This package provides the discrete-event simulator <tt>COORDINATE</tt> developed for studying the performance of robots that move items in a physical space.
It includes results presented in the paper *Performance Analysis of Fault-Tolerant Multi-Agent Coordination Mechanisms* accepted for publication on IEEE Transactions in Industrial Informatics.

## Authors
Riccardo Pinciroli (Gran Sasso Science Institute)
Catia Trubiani (Gran Sasso Science Institute)

## Abstract
todo

## Available Files
- *create\_dataframe\_from\_logs.py* is a script that processes simulation logs and creates a dataframe (CSV) for analysis purposes.
- *environment\_maps.py* specifies some topologies that are ready-to-use. This file can be extended to include new topologies.
- *params\_placeholder.py* contains the input parameters that are used to run the simulation. Some parameters in this file have a placeholder that is substituted by *runParallelSim.py* to perform what-if analysis.
- *runParallelSim.py* allows running multiple simulations in parallel. At the beginning of this file, values for parameters that in *params\_placeholder.py* where defined by a placeholder can be specified.
- *simulator.py* is the file that must be called to run the simulation.
- *utils.py* contains all classes and functions used by the discrete-event simulator. The only reason to change this file is the extension of the simulator with new features.
- *images/* is the directory where new figures are stored.
- *Data_Analysis.ipynb* contains scripts and logs used to generate figures in the paper.
- *results/* is the directory where new simulation logs are stored.

## Requirements
- Python 3.8.10
- All required modules can be installed by running <tt>pip3 install -r requirements.txt</tt>

## Reproduce Results in the Paper and Generate New Ones
Here, we describe 1) how to plot the same figures that are included in the paper, 2) how to generate new logs and figures starting from the same system configurations considered in the paper, 3) how to run a simulation with a new system configuration, and 4) how to define a new topology.

### Plot the Same Figures in the Paper
To plot the same figures that are included in the paper (using the same simulation logs generated for the paper), you can follow these steps.
1. From the main directory of this package, open the notebook <tt>replication\_package/figure\_\*/analyzeResults.ipynb</tt>.
2. Execute all cells in the notebook. Figures are stored in <tt>replication\_package/figure\_\*/images/</tt> (a copy of figures included in the paper is already in this folder).

### Generate new Logs from System Configurations used in the Paper
To plot figures using logs from new simulations (with the same input parameters used in the paper), you can follow these steps.
1. From the main directory of this package, go to <tt>replication_package/figure\_\*/</tt>.
2. Open the <tt>runParallelSim.py</tt> file and set the number of simulation to be run in parallel (MAXTHREADS, line 8).
3. Run <tt>python3 runParallelSim.py</tt>.
4. When the simulation is completed, follow the instructions to [Plot the Same Figures in the Paper](plot-the-same-figures-in-the-paper).
  
### Run the Discrete-Event Simulator
To run one or more simulations with new input parameters, you can follow these steps.
1. From the main directory of this package, open <tt>params_placeholder.py</tt> and set your own input parameters. [Table 1](#table-1) describes the parameters that can be changed in this file.
2. From the main directory of this package, open <tt>runParallelSim.py</tt> and set your own input parameters (from line 5 to line 31). Parameters from line 15 must be provided as a list. If the length of the list is longer than 1 and <tt>MAXTHREADS</tt> is greater than 1, the simulator run multiple simulations in parallel. [Table 2](#table-2) describes the parameters that can be changed in this file.
3. Once you specified all the input parameters, run <tt>python3 runParallelSim.py</tt>
4. Use the <tt>create\_dataframe\_from\_logs.py</tt> script to create a dataframe from the logs that you have just generated.
5. Use the dataframe to plot the desired figures (you can use scripts in the <tt>replication\_package</tt> directory or work with your own scripts).

#### Table 1

| Parameter | Description |
| --- | --- |
| SIM\_TIME | Time that must be simulated. |
| LOGFILE | The name of the file where logs are stored. Leave it empty to make the simulator generate the name based on the provided parameters. |
| SIMTIME\_LOGFILE | The name of the file where simulation times are stored. |
| LOG\_\<EVENT\> | Choose if \<EVENT\> must be logged (*True*) or not (*False*). A description of each \<EVENT\> is provided as a comment in the file.|
| SOURCE | ID of the room where items are created. |
| TARGETS | List of room IDs where items are delivered. The source cannot be in this list. Use *-1* for all rooms except the source (same probability). Use the same ID multiple times if a room is more likely to be selected as item destination than others, e.g., *\[1,2,2,2\]* means that items are three times more likely to be delivered in room 2 than room 1. |
| ITEM\_SPAWNING\_DISTR | Distribution of the inter-arrival time (only Exponential, Deterministic, and Trace are currently supported values). |
| IMPORTANCE\_PROBABILITIES | Probability that a new item will have the importance specified by the list index. The sum of all items in this list must be 1. |
| EXPIRATION\_TIME | Average time to deliver an item with the importance specified by the list index. Use *-1* if items do not expire. |
| EXPIRATION\_DISTR | Distribution of the expiration time (only Exponential and Deterministic are currently supported values). |
| MALICIOUS\_FAKE\_FAILURES | Choose if malicious robots should fake failures (*True*) or only communicate higher item importance when they fail for real (*False*). |
| FIND\_ROUTE\_STRATEGY | Choose which strategy should be used to find the shortest path: breadth-first (*breadth*) or depth-first (*depth*) search. |
| LOAD\_DISTR | Distribution of the time to load an object (only Exponential, Deterministic, and Trace are currently supported values). |
| MOVE\_DISTR | Distribution of the time to reach a new room (only Exponential, Deterministic, and Trace are currently supported values). |
| DROP\_DISTR | Distribution of the time to drop an object (only Exponential, Deterministic, and Trace are currently supported values). |
| COMP\_TIMES | Distribution of the computation time (only Exponential, Deterministic, and Trace are currently supported values). |
| COMM\_TIMES | Distribution of the communication time (only Exponential, Deterministic, and Trace are currently supported values). |
| RECOVERY\_DISTR | Distribution of the recovery time (only Exponential, Deterministic, and Trace are currently supported values). |

#### Table 2

| Parameter | Description |
| --- | --- |
| MAXTHREADS| Number of parallel simulations.|
| RESULTS\_DIRECTORY | Folder where all results are stored. |
| SIMULATOR\_DIRECTORY | Folder where files used by the simulator are located. |
| REPETITIONS | Number of repetitions of each simulation. |
| SAVE\_LOGS | Choose if system logs should be stored (*True*) or not (*False*). If <tt>REPETITIONS>1</tt> and you are only interested in scalability observations (i.e., how long the simulation takes to complete), we suggest to set this parameter to *False*.
| ARCHITECTURES | A list of architectures to simulate. Possible values are: *decentralized*, *semi-decentralized*, *centralized-impprox*, *centralized-proximp*, *centralized-importance*, and *centralized-proximity*. |
| TOPOLOGY\_NAMES | A list of topologies to simulate. Possible values are: *mesh*, *ring*, and *tree*. Other values can be used if users extend the <tt>envirnment\_maps.py</tt> file with their own topology. |
| NUM\_ROOMS | A list of number of rooms to simulate. |
| FAIL\_PROB | A list of agent failure probabilities to simulate. |
| COMM\_FAIL\_PROB | A list of communication failure probabilities to simulate. |
| NUM\_BOTS | A list of number of robots to simulate. |
| NUM\_MALICIOUS\_PERC | A list of percentage of malicious robots to simulate. |
| ITEM\_SPAWNING\_TIME | A list of item inter-arrival times to simulate (set to a negative number to use the trace specified in ITEM\_SPAWNING\_TRACE). |
| ITEM\_SAPWNING\_TRACE | The path to the trace to use for inter-arrivals. |
| LOAD\_TIMES | A list of load times to simulate (set to a negative number to use the trace specified in LOAD\_TRACE). |
| LOAD\_TRACE | The path to the trace to use for load times. |
| MOVE\_TIMES | A list of movement times to simulate (set to a negative number to use the trace specified in MOVE\_TRACE). |
| MOVE\_TRACE | The path to the trace to use for movements. |
| DROP\_TIMES | A list of drop times to simulate (set to a negative number to use the trace specified in DROP\_TRACE). |
| DROP\_TRACE | The path to the trace to use for drop times. |
| COMP\_TIMES | A list of computation times to simulate (set to a negative number to use the trace specified in COMP\_TRACE). |
| COMP\_TRACE | The path to the trace to use for computation times. |
| COMM\_TIMES | A list of communication times to simulate (set to a negative number to use the trace specified in COMM\_TRACE). |
| COMM\_TRACE | The path to the trace to use for communication times. |
| RECOVERY\_TIMES | A list of recovery times to simulate (set to a negative number to use the trace specified in RECOVERY\_TRACE). |
| RECOVERY\_TRACE | The path to the trace to use for recoveries. |


### Define a New Topology
To define a new space topology, you can follow these steps.
1. From the main directory of this package, open <tt>environment\_maps.py</tt>
2. Add a new dictionary to that file. Please, be sure that the name of the new dictionary is something like \<TOPOLOGY\>\<NUM\_ROOMS\>. The dictionary must have as many *Key*:*Value* pairs as the number of rooms in the new topology. *Key* is the ID of a room (i.e., from 0 to \<NUM\_ROOMS\> - 1). *Value* is a list containing the ID of rooms adjacent to the room specified by *Key*.
3. Finally, go to the end of the file and add a new *Key*:*Value* pair to the <tt>topologyName\_dict</tt>. *Key* is the name of the new topology. *Value* is the name of the dictionary which defines the new topology.
