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
import gc

class Todo(State):
    def __init__(self, new_todo, done=False) -> None:
        super().__init__()
        self.label = new_todo
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

    def remove(self, todo_id):
        self.todos = list(filter(lambda x:x.id != int(todo_id),self.todos))


todos = Todos()


# @reactive
def Todo_v(todo: Todo):
    text = Span(todo.label)

    if todo.done:
        text = S(text)

    return Div(
        text,
        Button("X", hx_delete=f"/todos/{todo.id}"),
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
        Button("hey",callback=lambda x:print("Hey")),
        Form(
            Input(
                placeholder="Add Todo...",
                name="new_todo",
            ),
            Input( type="checkbox", role="switch",name="done"),
            hx_on__after_request="this.reset()",
            callback=lambda x: todos.add(Todo(**x)),
            role="group",
        ),
        Todos(todos),
    )

@app.delete("/todos/<todo_id>")
async def _(req,todo_id):
    todos.remove(todo_id)



def run():
    print(gc.mem_free())
    app.run(debug=True)


if __name__ == "__main__":
    run()
