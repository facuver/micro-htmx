import json


class PersistentDict(dict):
    def __init__(self, path) -> None:
        self.path = path
        self.values = {}

        try:
            with open(self.path, "r") as file:
                for key, value in json.loads(file.read()).items():
                    self.values[key] = value
        except Exception as e:
            print("File not found creating empy dict: ", e)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value
        with open(self.path, "w") as file:
            file.write(json.dumps(self.values))

    def __getattr__(self, key):
        return getattr(self.values, key)

