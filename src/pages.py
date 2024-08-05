from base_elemets import Html,Head,Script,Link,Title,Body,Main,Header,Footer,Nav,Ul,Li,A,Strong,Style,Div


def navBar():
    return  Nav(
        Ul(
            Li(Strong("RP2040"))
        ),
        Ul(
            Li(A("About", klass="contrart",href="/")),
            Li(A("State", klass="contrart",href="/next")),
            Li(A("GPIO", klass="contrart",href="#"))
        )
    )
def template(content):
    return Html(
        Head(
            Script(src="gz/gz.htmx.min.js"),
            Link(rel="stylesheet", href="gz/gz.pico.zinc.min.css"),
        ),
        Body(
            Header(navBar(),klass="container"),
            Main(
                content,

            ),
            klass="container"
        ),
        color_mode="user"
    )

def page(func):
    """decorator to apply main template, wiht htmx, css and layout"""
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        return template(response)
    return wrapper