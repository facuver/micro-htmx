import asyncio
import asyncio
from lib.microHTMX.base_elemets import *  # noqa: F403
from lib.microHTMX.microHTMX import MicroHTMX, redirect
from lib.microHTMX.state import ReactiveComponent, ReactiveProperty

from common_components import page_template

app = MicroHTMX(reactive=True)


class Todo(ReactiveComponent):
    done: bool = ReactiveProperty(False)

    def __init__(self, label, delete_fn) -> None:
        super().__init__()
        self.label = label
        self.id = id(self)
        self.delete_fn = delete_fn

    def toggle(self, _):
        self.done = not self.done

    def render(self):
        label = H3(self.label+ (" ✅" if self.done else " ⏹️"), callback=self.toggle)
        delete = (
            H3("❌", callback=lambda x, t=self: self.delete_fn(t)) if self.done else ""
        )
        return Div(label, delete, role="group")


class Todos(ReactiveComponent):
    todos: list[Todo] = ReactiveProperty([])

    def __init__(self) -> None:
        super().__init__()

    def add_todo(self, new):
        self.todos = self.todos + [Todo(new, delete_fn=self.remove_todo)]

    def remove_todo(self, todo: Todo):
        self.todos = list(filter(lambda x: x.id != todo.id, self.todos))

    def render(self):
        return Div(*[s() for s in self.todos])


def templated(*args, **kwargs):
    return chunk(page_template(*args, **kwargs), 1024)


todos = Todos()
@app.page("/home")
async def _(request):
    return templated(
        Form(
            Input(name="new_todo", placeholder="Add todo..."),
            Button("Add"),
            callback=lambda x: todos.add_todo(x["new_todo"]),
            hx_on__after_request="this.reset()",
            role="group",
        ),
        todos(),
        path=request.path,
    )


@app.get("/")
def _(r):
    """
    Redirect to /home otherwise the navbar defaluts to /
    """
    return redirect("/home")


@app.page("/about")
async def _(request):
    return templated(H1("Hello"), Div(), path=request.path)


@app.page("/gpio")
async def _(request):
    return templated("SAS", path=request.path)


def run():
    app.run(debug=True, port=80)


if __name__ == "__main__":
    run()
