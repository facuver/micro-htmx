import asyncio
from lib.microHTMX.base_elemets import *  # noqa: F403
from lib.microHTMX.microXTMX import app , redirect 
from lib.microHTMX.state import ReactiveComponent, ReactiveProperty

from common_components import page_template


class Counter(ReactiveComponent):
    count:int= ReactiveProperty(0)
    
    def __init__(self) -> None:
        super().__init__()
        self.count = 0
        asyncio.create_task(self._update())

    async def _update(self):
        while True:
            self.increment()
            await asyncio.sleep(1)


    def increment(self):
        self.count += 1

    def render(self):
        return H1(Span(f"{self.count}"))


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
    c= Counter()
    return templated(c(), path=request.path)


@app.page("/about")
async def _(request):
    return templated(H1("Hello"),Div() ,path=request.path)

@app.page("/gpio")
async def _(request):
    return templated("SAS" ,path=request.path)

def run():
    app.run(debug=True,port=80)


if __name__ == "__main__":
    run()
