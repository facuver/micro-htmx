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
)  # noqa: F403
from common_components import page_template
from microXTMX import app
from lib_src.microdot.websocket import with_websocket, WebSocket
import asyncio
from typing import Any
from state import State,dispatch_to_ws


class Todos(State):
    def __init__(self,todos=[],dispatch_func= None) -> None:
        super().__init__()
        self.todos = todos
        self.callback = dispatch_func
        self.init()
 
    def render(self):
        return Div(
            *[t() for t in self.todos],
        )
    




def delete_todo(todo):
    t.todos =list(filter(lambda x:x.id!=todo.id, t.todos))

class Todo(State):
    def __init__(self,label,done=False,dispatch_func= None) -> None:
        super().__init__()
        self.label = label
        self.done = done
        self.init()

    def render(self):
        return Div(self.label + ( " ✅" if self.done else "") ,Div("X",callback=self.delete) )

    def delete(self,x):
        delete_todo(self)

    def toggle(self,obj):
        self.done = not self.done






t = Todos([Todo(f"Todo {i}", i%2 == 0) for i in range(10)])

@app.page("/")
async def _(request):
    return page_template(
        t()

    )




def run():

    app.run(debug=True)


if __name__ == "__main__":
    run()
