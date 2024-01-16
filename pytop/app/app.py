from textual.app import App
from textual.binding import Binding

from ..screens import Main, Setup


class Pytop(App):
    BINDINGS = [
        Binding(key="escape", action="switch_mode('main')", show=False),
        Binding(key="f1", action="switch_mode('help')", description="Help"),
        Binding(key="f2", action="switch_mode('setup')", description="Setup"),
    ]
    MODES = {"main": Main, "setup": Setup}

    def on_mount(self) -> None:
        self.switch_mode("main")
