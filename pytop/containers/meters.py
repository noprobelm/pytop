from textual.containers import Vertical, Container, Horizontal
import psutil
from ..widgets import *
from textual.widget import Widget
from textual.widgets import Static, Label

class MeterColumn(Vertical):
    DEFAULT_CSS = """
    MeterColumn {
        height: auto;
    }
    """


class Meters(Widget):
    DEFAULT_CSS = """

    Meters {
        layout: horizontal;
        height: auto;
        width: auto;
    }

    Meters Horizontal {
        height: auto;
        align-horizontal: right;
        width: auto;
        padding: 0 1 0 1;
    }

    Meters Vertical {
        height: auto;
        padding: 1
    }


    """

    def compose(self):
        num_cores = psutil.cpu_count()

        with Vertical():
            for i in range(num_cores // 2)[::2]:
                with Horizontal():
                    yield CPUUsage(str(i), i)
                    yield CPUUsage(str(i + 1), i + 1)

            yield Horizontal(RAMUsage("Mem", classes="meter"))
            yield Horizontal(SwapUsage("Swp", classes="meter"))

        with Vertical():
            for i in range(num_cores // 2, num_cores)[::2]:
                with Horizontal():
                    yield CPUUsage(str(i), i)
                    yield CPUUsage(str(i + 1), i + 1)

            yield Horizontal(Tasks())
            yield Horizontal(LoadAverage())
            yield Horizontal(Uptime())
