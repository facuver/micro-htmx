from lib.microdot.microdot import Microdot, send_file, Response
from base_elemets import Div,Input,Button ,Form,Aside,Nav,Li,Ul,H1 # noqa: F403
from pages import page
from html_builder import callbacks_app

app = Microdot()
Response.default_content_type = "text/html"

def incremetn(x):
    
    return Button(f"Button {x+1}",callback=lambda x,v=x: incremetn(v+1),hx_swap="outerHTML")



@app.get("/")
@page
async def _(request):
    return Div("hey")

@app.get("/next")
@page
async def _(request):
    return Div("Next")

@app.route("/gz/<file>")
async def _(request, file):
    return send_file(f"./public/gz/{file}",compressed=True)

@app.route("/<file>")
async def _(request, file):
    return send_file(f"./public/{file}")


def run():
    app.mount(callbacks_app,"/callbacks")
    app.run(debug=True)


if __name__ == "__main__":
    run()
