import server
import gc
import asyncio

class Signal:
    def __init__(self):
        self._callbacks = []

    def connect(self, callback):
        self._callbacks.append(callback)

    def emit(self, *args):
        for callback in self._callbacks:
            callback(*args)

class ReactiveProperty:
    def __init__(self, initial_value):
        self._value = initial_value
        self.changed = Signal()

    def get(self):
        return self._value

    def set(self, new_value):
        if new_value != self._value:
            self._value = new_value
            self.changed.emit(new_value)

class ReactiveObject:
    def __init__(self):
        self._properties = {}

    def reactive_property(self, name, initial_value):
        prop = ReactiveProperty(initial_value)
        self._properties[name] = prop
        return prop

    def __getattr__(self, name):
        if name in self._properties:
            return self._properties[name].get()
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        elif name in self._properties:
            self._properties[name].set(value)
        else:
            super().__setattr__(name, value)


class LED(ReactiveObject):
    def __init__(self, pin):
        super().__init__()
        self.state = self.reactive_property('state', False)
        self.pin = pin
        # Assuming you have a way to control the LED, e.g., machine.Pin
        # self.led = machine.Pin(pin, machine.Pin.OUT)

    def update_led(self, new_state):
        print("LED state changed to:", new_state)
# async def gc_print():
#     while True:
#         gc.collect()
        
#         await asyncio.sleep(1)

# asyncio.create_task(gc_print())

# server.run()

led = LED(5)  # Assuming the LED is connected to pin 5

# Connect the state change to the LED update method
led.state.changed.connect(led.update_led)

# Change the LED state
led.state = True   # This will print: LED state changed to: True
led.state = False  # This will print: LED state changed to: False