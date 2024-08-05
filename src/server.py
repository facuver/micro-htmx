from base_elemets import Div,Input,Button ,Form,Aside,Nav,Li,Ul,H1 # noqa: F403

from html_builder import page, app


@page("/")
async def _(request):
    return Button("test",hx_get="/test")

@page("/next")
async def _(request):
    return Div("next"),Div("ds"),Div("Sd")


@app.get("/test")
async def _(request):
    print("Hey")
    return 

def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
