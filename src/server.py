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

class State:
    def __init__(self,callback,data=None) -> None:
        self.data = data
        self.notify = callback

    def set_data(self,value):
        self.data = value
        print("Set")
        self.notify(self.data)

sse_queue = asyncio.Queue(maxsize=20)

def reactive(data):
    d=  Span(
        Div(f"watijg {data}",
            id="test123"), 
        hx_ext="ws", ws_connect="/echo")
    return d

state  = State(reactive,2)



@app.route("/echo")
@with_websocket
async def echo(request, ws:WebSocket):
    while True:
        ws.send(await sse_queue.get())


@app.page("/")
async def _(request):
    return page_template(
        reactive("2"),
        Button("SEND", callback=lambda x:state.set_data(11))
    )


def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
