import itertools

class lotl:
    def __init__(self,data):
        self.data = data

    def flatten_list(self):
        new_data = self.data
        while True:
            if isinstance(new_data[0],list):
                new_data = list(itertools.chain(*new_data))
            else:
                break
        return new_data

    def flatten_tuple(self):
        new_data = self.data
        while True:
            if isinstance(new_data[0],tuple):
                new_data = tuple(itertools.chain(*new_data))
            else:
                break
        return new_data

    def mean(self):
        return sum(self.data) / len(self.data)
