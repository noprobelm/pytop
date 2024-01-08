from textual.app import App
from . import screens


class App(App):
    SCREENS = {"main": screens.Main()}

    def on_mount(self) -> None:
        self.push_screen("main")


if __name__ == "__main__":
    app = App()
    app.run()
