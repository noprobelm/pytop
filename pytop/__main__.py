from textual.app import App
from .screens.main import Main


class Pytop(App):
    SCREENS = {"main": Main()}
    CSS_PATH = "styles/styles.tcss"

    def on_mount(self) -> None:
        self.push_screen("main")


def main():
    pytop = Pytop()
    pytop.run()


if __name__ == "__main__":
    main()
