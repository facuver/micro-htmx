from base_elemets import *# noqa: F403
from common_components import page_template
from microXTMX import app , add_head
from lib_src.microdot.websocket import with_websocket, WebSocket
import asyncio
from typing import Any
from state import State,dispatch_to_ws




class Todos(State):
    def __init__(self,todos=[],dispatch_func= None) -> None:
        super().__init__()
        self.todos = todos
        self.callback = dispatch_func
        # self.init()
 
    def render(self):
        return Div(
            *[t() for t in self.todos],
        )
    

    def add(self, tod):
        self.todos += [tod]


@app.get("/todo")
def _(request):
    return Span("")

def delete_todo(todo):
    t.todos =list(filter(lambda x:x.id!=todo.id, t.todos))

class Todo(State):
    def __init__(self,label,done=False,dispatch_func= None) -> None:
        super().__init__()
        self.label = label
        self.done = done

    def render(self):
        return Div(Div(self.label + ( " ✅" if self.done else " ⏹️") ,hx_get="/todo") , role="group")

    def delete(self,x):
        delete_todo(self)
        return Span()

    def toggle(self,obj):
        self.done = not self.done
        

import time



    
t = Todos([Todo(f"Todo {i}", i%2 == 0) for i in range(10)])


# @app.page("/")
# async def _(request):
#     return page_template(
#         Input(placeholder="Add Todo..." , callback=lambda x: t.add(Todo(x.items()[0]))),
#         t()

#     )


@app.page("/")
async def _(request):
    return chunk(page_template(t(),request= request) , 200)




def run():

    app.run(debug=True)


if __name__ == "__main__":
    run()
