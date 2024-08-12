from base_elemets import (
    Html,
    Head,
    Script,
    Link,
    Title,
    Body,
    Main,
    Header,
    Footer,
    Nav,
    Ul,
    Li,
    A,
    Strong,
    Style,
    Div,
    Span,
    Meta,
    chain,
)


def navBar():
    return Nav(
        Ul(Li(Strong("RP2040"))),
        Ul(
            Li(A("About", klass="contrart", href="/")),
            Li(A("State", klass="contrart", href="/next")),
            Li(A("GPIO", klass="contrart", href="#")),
        ),
    )


def page_template(*content):
    return chain(
        Header(navBar(), klass="container"),
        Span(hx_ext="ws", ws_connect="/ws_updates"),
        Main(*content, klass="container",hx_ext="ws", ws_connect="/ws_callbacks" ),
    )


def add_head(*content):
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Script(src="public/gz/gz.htmx.min.js"),
            Script(src="public/gz/gz.ws.js"),
            Link(rel="stylesheet", href="public/gz/gz.pico.zinc.min.css"),
        ),
        Body(
            *content,
            klass="container",
        ),
    )
