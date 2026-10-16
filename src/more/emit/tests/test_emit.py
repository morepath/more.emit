from io import StringIO

from webtest import TestApp as Client

from more.emit import EmitApp


def test_emit():
    message = StringIO()

    class App(EmitApp):
        pass

    @App.signal.on("myevent")
    def handler1(arg, request):
        message.write(f"handler1 called with {arg}\n")

    @App.signal.on("myevent")
    def handler2(arg, request):
        message.write(f"handler2 called with {arg}\n")

    @App.path(path="")
    class Root:
        pass

    @App.json(model=Root)
    def root_view(self, request):
        request.app.signal.emit("myevent", "foo", request)
        return {"message": message.getvalue()}

    c = Client(App())

    response = c.get("/")

    assert message.getvalue() == (
        "handler1 called with foo\nhandler2 called with foo\n"
    )

    assert response.json["message"] == (
        "handler1 called with foo\nhandler2 called with foo\n"
    )

    message.close()
