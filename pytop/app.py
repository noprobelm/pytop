from textual.app import App
from . import data
from .widgets import ProcessTable
from . import screens


class Pytop(App):
    processes = data.get_processes()
    SCREENS = {"main": screens.Main()}
    CSS_PATH = "styles/styles.tcss"

    def on_mount(self) -> None:
        self.push_screen("main")


if __name__ == "__main__":
    app = App()
    app.run()
