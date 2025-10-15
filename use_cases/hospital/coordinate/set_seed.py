# set_seed.py
import os
import random
import numpy as np

SEED = 42

# Make Python’s hashing deterministic (important for dict/set order)
os.environ["PYTHONHASHSEED"] = str(SEED)

# Built-in Python random
random.seed(SEED)

# NumPy
np.random.seed(SEED)

# Try to fix seed for other frameworks if installed
try:
    import torch
    torch.manual_seed(SEED)
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
except ImportError:
    pass

try:
    import tensorflow as tf
    tf.random.set_seed(SEED)
except ImportError:
    pass

print(f"[INFO] Global random seed fixed to {SEED}")
