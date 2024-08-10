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
from lib.microdot.websocket import with_websocket, WebSocket
import asyncio

from typing import Any
from typing_extensions import Unpack


from base_elemets import KWARGS


class State():

    def __init__(self) -> None:
        self.callback = None
        self.id = "id-" + str(id(self))

    def render(self):
        raise NotImplementedError

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.render().replace(">",f" id={self.id}>",1)
    

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name]= value
        if self.callback:
            self.callback(self())


class Todos(State):
    def __init__(self,todos=[],dispatch_func= None) -> None:
        super().__init__()
        self.todos = todos
        self.callback = dispatch_func
 
    def render(self):
        return Div(
            *[t() for t in self.todos],
        )


    


ws_send_queue = asyncio.Queue(maxsize=10)
def dispatch(obj):
    try:
        ws_send_queue.put_nowait(obj)
    except:
        print("queue full")

@app.route("/echo")
@with_websocket
async def echo(request, ws:WebSocket):
    while True:
        await ws.send(await ws_send_queue.get())



def delete(todo):
    t.todos =list(filter(lambda x:x.id!=todo.id, t.todos))

class Todo(State):
    def __init__(self,label,done=False,dispatch_func= None) -> None:
        super().__init__()
        self.label = label
        self.done = done
        self.callback = dispatch_func

    def render(self):
        return Div(self.label + ( " ✅" if self.done else "") , callback=lambda x:delete(self)  )


    def toggle(self,obj):
        self.done = not self.done






t = Todos([Todo(f"Todo {i}", i%2 == 0, dispatch_func=dispatch) for i in range(20)],dispatch_func=dispatch)

@app.page("/")
async def _(request):

    return page_template(
        Span(hx_ext="ws", ws_connect="/echo"),
        t()

    )


def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
