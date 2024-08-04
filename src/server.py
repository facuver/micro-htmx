from microdot.microdot import Microdot, send_file
from base_elemets import Div,Input,Button ,Form,Aside,Nav,Li,Ul # noqa: F403
from pages import template
from html_builder import callbacks_app

app = Microdot()

def menu():
    return Nav(
        Ul(
            Li(
                Ul(
                    Li("manu1"),
                    Li("manu2"),
                    Li("manu3"),
                )
            )
        )

    )

@app.get("/")
async def _(request):
    til=Div("HEYYYYY",callback=lambda x:Div("HEy!!@!!"),id="result")
    print(til)
    return template(Div( 
                        "Hello", 
                        til,
                        til,
                        Input(name="ho",klass="input" ,placehoder="as",callback=lambda x:x,hx_target="#result",hx_trigger="keyup changed delay:0.1s"),
                        Button("click",callback=lambda x:print("hello"),hx_swap="innerHTML"),
                        )) 


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
