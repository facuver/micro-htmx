from base_elemets import *  # noqa: F403
from common_components import page_template
from microXTMX import app
from lib_src.microdot.websocket import with_websocket, WebSocket
from state import ReactiveComponent, ReactiveProperty


class Counter(ReactiveComponent):
    count:int= ReactiveProperty(0)
    double:int = ReactiveProperty(0)
    def __init__(self) -> None:
        self.double_count = self.count * 2

        super().__init__()

    def increment(self):
        self.count += 1

    def render(self):
        return H1(Span(f"{self.count}  :: {self.double_count}"))



c= Counter()
# Usage
def Co():
    global c
    return Div(c(), Div("+",klass="button", callback=lambda x: c.increment() , value="Ok"))


@app.page("/")
@app.page("/home")
async def _(request):
    return chunk(
        page_template(
            Co(),
            Co(),


        path=request.path),
        512,
    )


@app.page("/about")
async def _(request):
    return chunk(page_template(H1("Hello") ,path=request.path))

@app.page("/gpio")
async def _(request):
    return chunk(page_template('<sl-button size="small">Click me</sl-button>',H1("Hello") ,path=request.path))

def run():
    app.run(debug=True,port=5000)


if __name__ == "__main__":
    run()
