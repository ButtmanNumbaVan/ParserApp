import pickle


def dump_main_list(file_name, data):
    with open('dumps/{}'.format(file_name), 'wb') as f:
        pickle.dump(data, f)
        f.close()


def load_main_list(file_name):
    with open('dumps/{}'.format(file_name), 'rb') as f:
        data = pickle.load(f)
        f.close()
        return data