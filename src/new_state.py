class Signal:
    def __init__(self):
        self._callbacks = []

    def connect(self, callback):
        self._callbacks.append(callback)

    def emit(self, *args):
        for callback in self._callbacks:
            callback(*args)

class Component:
    def __init__(self):
        self._state = {}
        self.html_changed = Signal()

    def set_state(self, key, value):
        if self._state.get(key) != value:
            self._state[key] = value
            self.html_changed.emit(self.render())

    def get_state(self, key):
        return self._state.get(key)

    def render(self):
        # This method should be overridden in subclasses
        return "<div>Base Component</div>"

# Example usage
class Counter(Component):
    def __init__(self, initial_count=0):
        super().__init__()
        self.set_state('count', initial_count)

    def increment(self):
        self.set_state('count', self.get_state('count') + 1)

    def decrement(self):
        self.set_state('count', self.get_state('count') - 1)

    def render(self):
        return "<div>Count: %d</div>" % self.get_state('count')

class TodoList(Component):
    def __init__(self):
        super().__init__()
        self.set_state('todos', [])

    def add_todo(self, todo):
        todos = self.get_state('todos') + [todo]
        self.set_state('todos', todos)

    def render(self):
        todo_items = "".join(["<li>%s</li>" % todo for todo in self.get_state('todos')])
        return "<ul>%s</ul>" % todo_items
    

def update_html(new_html):
    print("HTML updated:")
    print(new_html)

# Counter example
counter = Counter(0)
counter.html_changed.connect(update_html)

print(counter.render())  # Initial render
counter.increment()  # This will trigger a re-render
