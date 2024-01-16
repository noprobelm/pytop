from textual.app import App
from textual.reactive import Reactive
import psutil

from .screens import Main, Setup
from .widgets import CPUUsage
from .app import Pytop


def main():
    pytop = Pytop()
    pytop.run()


if __name__ == "__main__":
    main()
