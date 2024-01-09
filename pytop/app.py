from textual.app import App
from . import screens


class Pytop(App):
    SCREENS = {"main": screens.Main()}
    CSS_PATH = "styles/styles.tcss"

    def on_mount(self) -> None:
        self.push_screen("main")


if __name__ == "__main__":
    app = App()
    app.run()
