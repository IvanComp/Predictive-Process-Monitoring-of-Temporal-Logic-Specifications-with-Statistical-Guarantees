## Drone Surveillance System

Run ``drone/drone.py`` Please refer to comments contained in it.   

## Smart Hospital Multi-Agent System

``hospital/coordinate/`` contains the tool used for environment simulation. It is not part of our contribution and only minimal modification have been performed.
The original files can also be downloaded [here](https://figshare.com/articles/software/Replication_Package_A_Framework_for_Performance_Analysis_of_Fault-Tolerant_Multi-Agent_Coordination_Mechanisms/16940749?file=38690928) and the reference paper is available [here](https://ieeexplore.ieee.org/document/10013943).
To reproduce results just simply run in order

- ``hospital/time_bounds.py`` to evaluate reasonable bounds for formula ...
- ``hospital/analysis_item.py`` to evaluate robustness of --- on simulated item trajectories
- ``hospital/analysis_robot.py`` to evaluate robustness of --- on simulated robot trajectories  
- ``hospital/generate_statistics.py`` to extract statistical information of time robustness for all the three properties.

> ⚠️ COORDINATE tool does not generate reproducible results (no random seed can be fixed, at least we cannot achieve it).
> To reproduce exactly the paper results we upload the generate trajectories in folder (hospital/coordinate/results_backup/). 
> All the code mentioned above use that trajectories. Refer to comments contained in them.