import numpy as np
import pandas as pd


def to_list(v):
    v = v[1:-1]
    return [float(a) for a in v.split(",")]


def filter(v):
    return [a for a in v if np.isfinite(a)]


df = pd.read_csv("./results/all_item.csv")
df = df[df.fp!=0]
df["f0"] = df.apply(lambda x: to_list(x["f0"]), axis=1)
df["f0_mean"] = df["f0"].apply(lambda x: np.mean(filter(x)))
df["f0_median"] = df["f0"] .apply(lambda x: np.median(filter(x)))
df["f0_q1"] = df["f0"] .apply(lambda x: np.percentile(filter(x),25))
df["f0_q2"] = df["f0"] .apply(lambda x: np.percentile(filter(x),75))
df["f1"] = df.apply(lambda x: to_list(x["f1"]), axis=1)
df["f1_mean"] = df["f1"].apply(lambda x: np.mean(filter(x)))
df["f1_median"] = df["f1"].apply(lambda x: np.median(filter(x)))
df["f1_q1"] = df["f1"].apply(lambda x: np.percentile(filter(x),25))
df["f1_q2"] = df["f1"].apply(lambda x: np.percentile(filter(x),75))
df = df.drop('f0', axis=1)
df = df.drop('f1', axis=1)
df.to_csv("./results/all_item_stat.csv", index=False)


dd = pd.read_csv("./results/all_robot.csv")
dd = dd[dd.fp!=0]
dd["f0"] = dd.apply(lambda x: to_list(x["f0"]), axis=1)
dd["f0_mean"] = dd["f0"].apply(lambda x: np.mean(filter(x)))
dd["f0_median"] = dd["f0"] .apply(lambda x: np.median(filter(x)))
dd["f0_q1"] = dd["f0"].apply(lambda x: np.percentile(filter(x),25))
dd["f0_q2"] = dd["f0"].apply(lambda x: np.percentile(filter(x),75))
dd = dd.drop('f0', axis=1)
dd.to_csv("./results/all_robot_stat.csv", index=False)



