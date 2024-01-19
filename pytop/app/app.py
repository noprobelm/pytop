from textual.app import App
from textual.binding import Binding

from ..screens import Main, Help


class Pytop(App):
    CSS_PATH = """../styles/styles.tcss"""
    BINDINGS = [
        Binding(key="escape", action="switch_mode('main')", show=False),
        Binding(key="f1", action="switch_mode('help')", description="Help"),
    ]
    MODES = {"main": Main, "help": Help}

    def on_mount(self) -> None:
        self.switch_mode("main")
