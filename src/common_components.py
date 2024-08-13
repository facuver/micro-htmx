from base_elemets import Html,Head,Script,Link,Title,Body,Main,Header,Footer,Nav,Ul,Li,A,Strong,Style,Div,Span

def navBar(path):
    print(path)
    return  Nav(
        Ul(
            Li(Strong("RP2040" + " > " + path))
        ),
        Ul(
            Li(A("About", klass="contrart " , href="/")),
            Li(A("State", klass="contrart" , href="/next")),
            Li(A("GPIO", klass="contrart" ,  href="#"))
        )
    )

def page_template(*content , request):
    yield from Header(navBar(request.path),klass="container")
    yield from Span( hx_ext="ws", ws_connect="/ws_updates")
    yield from Main(*content,klass="container", hx_ext="ws", ws_connect="/ws_callbacks")




