import pandas as pd

df = pd.read_csv("coordinate/results_backup/centralizedimpprox_GUH73_Nb20_Nm0_A120_R43200m_FP0.0.csv")

dest = df.groupby('itemId')['destination'].first().reset_index()
dest_dict = dest.set_index('itemId')['destination'].to_dict()

times = df.groupby('itemId')['simTime'].agg(['min','max']).reset_index()
times['tot'] = times["max"] - times['min']
times['dest'] = times.apply(lambda x: dest_dict[x["itemId"]],axis=1)
importance = df.groupby('itemId')['itemImportance'].max().reset_index()
times['importance'] = importance["itemImportance"]
# times.groupby(['dest','importance'])['tot'].agg(['mean', 'std']).reset_index()
destination_time = times.groupby('dest')['tot'].agg(['mean','std']).reset_index()
destination_time["lb"] = destination_time["mean"] - 1.5 * destination_time["std"]
destination_time["ub"] = destination_time["mean"] + 1.5 * destination_time["std"]
dest_time_bounds = destination_time[["lb","ub"]].to_dict()

import pickle

with open('./results/dest_time_bounds.pkl', 'wb') as f:
    pickle.dump(dest_time_bounds, f)