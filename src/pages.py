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
            Script(src="public/gz/gz.htmx.min.js"),
            Link(rel="stylesheet", href="public/gz/gz.pico.zinc.min.css"),
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

