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

def page_template(*content):
    return Header(navBar(),klass="container"),Main(*content,klass="container")



