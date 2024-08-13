from base_elemets import *  # noqa: F403
from common_components import page_template
from microXTMX import app
from lib_src.microdot.websocket import with_websocket, WebSocket
from state import ReactiveComponent, ReactiveProperty


class Counter(ReactiveComponent):
    count = ReactiveProperty(0)

    def __init__(self) -> None:
        super().__init__()

    def increment(self):
        self.count += 1

    def render(self):
        return Div(f"Count: {self.count}")


# Usage
def Co():
    c = Counter()
    return Div(c(), Button("+", callback=lambda x: c.increment()))



@app.page("/")
async def _(request):
    return chunk(
        page_template(
            Co(),
            Co()


        ),
        512,
    )


def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
