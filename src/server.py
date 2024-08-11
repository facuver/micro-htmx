from base_elemets import (
    Div,
    Label,
    Input,
    Button,
    Form,
    Aside,
    Nav,
    Li,
    Ul,
    H1,
    Span,
    H4,
    S,
)  # noqa: F401
from common_components import page_template
from microXTMX import app
from state import State, reactive


class Todo(State):
    def __init__(self, label, done=False) -> None:
        super().__init__()
        self.label = label
        self.done = done
        self.id = id(self)

    def toggle(self):
        self.done = not self.done


class Todos(State):
    def __init__(self) -> None:
        super().__init__()
        self.todos = []

    def add(self, todo):
        print(todo, " Added")
        self.todos += [todo]

    def remove(self, todo):
        self.todos = [t for t in self.todos if t is not todo]


todos = Todos()


@reactive
def Todo_v(todo: Todo):
    text = Span(todo.label, callback=lambda x: todo.toggle())

    if todo.done:
        text = S(text)

    return Div(
        text,
        Button("X", klass="btn-danger", callback=lambda x, v=todo: todos.remove(todo)),
        rolw="group",
    )


@reactive
def Todos(todos: Todos):
    return Div(
        *[Todo_v(t) for t in todos.todos],
    )


@app.page("/")
async def _(request):
    return page_template(
        Span(hx_ext="ws", ws_connect="/ws"),
        Form(
            Input(
                placeholder="Add Todo...",
                name="new_todo",
            ),
            Input( type="checkbox", role="switch",name="done"),

            hx_on__after_request="this.reset()",
            callback=lambda x: todos.add(Todo(x["new_todo"], x["done"])),
            role="group",
        ),
        Todos(todos),
    )


def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
