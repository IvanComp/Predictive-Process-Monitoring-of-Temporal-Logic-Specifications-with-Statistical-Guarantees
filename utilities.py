import pickle
def load_pickle(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)