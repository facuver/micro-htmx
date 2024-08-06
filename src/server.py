from base_elemets import Div,Input,Button ,Form,Aside,Nav,Li,Ul,H1 # noqa: F403
from common_components import page_template
from microXTMX import app


@app.page("/")
async def _(request):
    return page_template(Button("test",hx_get="/test"))

@app.page("/next")
async def _(request):
    return page_template(Div("next"),Div("sa"))


@app.get("/test")
async def _(request):
    return 

def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
