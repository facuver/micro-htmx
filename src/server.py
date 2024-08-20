import asyncio
import asyncio
from lib.microHTMX.base_elemets import *  # noqa: F403
from lib.microHTMX.microHTMX import MicroHTMX, redirect 
from lib.microHTMX.state import ReactiveComponent, ReactiveProperty

from common_components import page_template

app = MicroHTMX(reactive=True)

class Todo(ReactiveComponent):
    done:bool= ReactiveProperty(False)

    def __init__(self,label) -> None:
        super().__init__()
        self.label = label
        self.todo_id  = id(self)

    def toggle(self,_):
        self.done = not self.done

    def render(self):

        return Div(H3(self.label  + (" ✅" if self.done else " ⏹️"), callback= self.toggle) ,  H3("❌" , callback=lambda x,t=self:c.remove_todo(t)) if self.done else "" , role="group")

class Todos(ReactiveComponent):
    todos:list[Todo] = ReactiveProperty([Todo("Gee")])

    def __init__(self) -> None:
        super().__init__()
    
    def add_todo(self,new):
        print(new)
        self.todos = self.todos + [Todo(new)]


    def remove_todo(self,todo):
        self.todos = list(filter(lambda x:x._id!=todo.id, self.todos ))

    def render(self):
        return Div(*[s() for s in self.todos ])

c= Todos()


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
    global c
    return templated(Form(Input(name="new_todo", placeholder = "Add todo..."),Button("Add"),callback=lambda x:c.add_todo(x["new_todo"]),hx_on__after_request='this.reset()',role="group" ),c(), path=request.path)


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
