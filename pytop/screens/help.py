from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Placeholder


class Help(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Help message will go here.")
        yield Footer()
