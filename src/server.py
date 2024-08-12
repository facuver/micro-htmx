from base_elemets import (
    Div,
    Input,
    Button,
    Form,
    Aside,
    Nav,
    Li,
    Ul,
    H1,
    Span,
    render_html,
)  # noqa: F403
from common_components import page_template
from microXTMX import app, add_head
import asyncio
from state import Reactive


class Todos(Reactive):
    def __init__(self, todos=[]) -> None:
        super().__init__()
        self.todos = todos

    def render(self):
        return Div(
            *[t() for t in self.todos],
        )

    def add(self, tod):
        self.todos += [tod]


def delete_todo(todo):
    t0.todos = list(filter(lambda x: x.id != todo.id, t0.todos))


class Todo(Reactive):
    def __init__(self, label, done=False) -> None:
        super().__init__()
        self.label = label
        self.done = done

    def render(self):
        return Div(
            Div(
                self.label + (" ✅" if self.done else " ⏹️"),
                Span("❌", callback=self.delete) if self.done else "",
                callback=self.toggle,
            ),
            role="group",
        )

    def delete(self, x):
        delete_todo(self)

    def toggle(self, obj):
        self.done = not self.done


t0 = Todos([Todo(f"Todo {i}", i % 2 == 0) for i in range(5)])




def AddTodo():
    def add(x):
        t0.add(Todo(x["new_todo"]))
        return AddTodo()

    return Input(
        placeholder="Add Todo...",
        value="",
        id="new_todo",
        name="new_todo",
        hx_on__before_request='alert("Making a request!")',
        callback=add,
    )


@app.get("/")
async def _(request):
    return add_head(page_template(t0()))





def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
