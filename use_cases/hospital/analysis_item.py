import os
import pickle
import re

import pandas as pd

from mitl import load_formula, evaluate_robustness_semantics

with open('./results/dest_time_bounds.pkl', 'rb') as f:
    dest_time_bounds = pickle.load(f)

from collections import defaultdict


def merge_events(data):
    merged = defaultdict(set)

    for time, event in data:
        merged[time].add(event)

    # Sort by time (optional but usually useful)
    return sorted(merged.items())


def generate(df):
    df = df.copy()
    df.loc[:, "traces"] = df.apply(lambda x: (x["simTime"], x["event"]), axis=1)
    traces = df.groupby('itemId')['traces'].agg(list).reset_index()
    traces["times"] = traces.apply(lambda x: x["traces"][-1][0] - x["traces"][0][0], axis=1)
    traces["dest"] = df.groupby('itemId')['destination'].first().reset_index()["destination"]
    traces["traces"] = traces["traces"].apply(lambda x: merge_events(x))
    return traces


formula = load_formula(f'G[0,INF](create --> F[0.0,20] startloading)')
get_formula = lambda x: load_formula(
    f'G[0,INF](startloading --> F[{dest_time_bounds["lb"][x.dest]},{dest_time_bounds["ub"][x.dest]}] deliver)')


def simulate(path):
    df = pd.read_csv(path)
    df['event'] = df['event'].str.lower()

    tr = generate(df)
    tr = tr.drop(index=0)

    dd = df.groupby("itemId")['itemImportance'].max().reset_index()
    dd.reset_index()
    dic_imp = dd["itemImportance"].to_dict()
    tr["imp"] = tr.apply(lambda x: dic_imp[x["itemId"]], axis=1)
    tr["F0"] = tr.apply(lambda x: evaluate_robustness_semantics(x["traces"], formula), axis=1)
    tr["F1"] = tr.apply(lambda x: evaluate_robustness_semantics(x["traces"], get_formula(x)), axis=1)
    return tr["F0"].tolist(), tr["F1"].tolist()


folder_path = "coordinate/results_backup/"
# folder_path = "coordinate/results/" (USE THIS IF YOU WOULD LIKE TO RUN THE SIMULATOR, i.e, COORDINATE)


files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
print(files)

cases = []

for f in files:
    data = f.split("_")
    if len(data) > 4:
        mech = data[0]
        topology = data[1]
        nb = int(re.fullmatch(r"Nb(\d+)", data[2]).group(1))
        nm = int(re.fullmatch(r"Nm(\d+)", data[3]).group(1))
        a = int(re.fullmatch(r"A(\d+)", data[4]).group(1))
        r = int(re.fullmatch(r"R(\d+)m", data[5]).group(1))
        fp = float(re.fullmatch(r"FP([0-9]*\.?[0-9]+)\.csv", data[6]).group(1))
        f0, f1 = simulate(os.path.join(folder_path, f))
        cases.append([mech, topology, nb, nm, a, r, fp, f0, f1])
        print([mech, topology, nb, nm, a, r, fp])
df = pd.DataFrame(cases, columns=["mech", "topology", "nb", "nm", "a", "r", "fp", "f0", "f1"])
df.to_csv("./results/all_item.csv")

print("DONE -- saved in ./results/all_item.csv ")
