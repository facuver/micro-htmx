from lib.microHTMX.base_elemets import *  # noqa: F403
from common_components import page_template
from lib.microHTMX.microXTMX import app , redirect
from lib.microHTMX.state import ReactiveComponent, ReactiveProperty


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


@app.get("/")
def _(r):
    return redirect("/home")

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
    return chunk(page_template(H1("Hello") ,path=request.path))

def run():
    app.run(debug=True,port=80)


if __name__ == "__main__":
    run()
