import time
import server

class LoggedAgeAccess:

    

    def __get__(self, obj, objtype=None):
        value = obj._age
        print('Accessing %r giving %r', 'age', value)
        return value

    def __set__(self, obj, value):
        print('Updating %r to %r', 'age', value)
        obj._age = value

class Person:

    age = LoggedAgeAccess()             # Descriptor instance

    def __init__(self, name, age):
        self.name = name                # Regular instance attribute
        self.age = age                  # Calls __set__()

    def birthday(self):
        self.age += 1                   # Calls both __get__() and __set__()

# time.sleep(2)



# server.run()

