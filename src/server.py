from microHTMX.base_elemets import *  # noqa: F403
from microHTMX.microXTMX import app , redirect ,
from microHTMX.state import ReactiveComponent, ReactiveProperty

from common_components import page_template
from components.temperature import TemperatureDisplay


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


def templated(*args, **kwargs):
    return chunk(page_template(*args, **kwargs), 1024)

@app.get("/")
def _(r):
    """
    Redirect to /home otherwise the navbar defaluts to /
    """
    return redirect("/home")

@app.page("/home")
async def _(request):
    return templated(Div("Heelo"), path=request.path)


@app.page("/about")
async def _(request):
    return templated(H1("Hello") ,path=request.path)

temp = TemperatureDisplay()
@app.page("/gpio")
async def _(request):
    return templated(temp() ,path=request.path)

def run():
    app.run(debug=True,port=80)


if __name__ == "__main__":
    run()
