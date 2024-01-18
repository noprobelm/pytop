from textual.containers import Vertical, Horizontal
import psutil
from ..widgets import *


class MeterHeader(Horizontal):
    def compose(self):
        num_cores = psutil.cpu_count()

        with Vertical(classes="meter-col", id="c1"):
            for i in range(num_cores // 2)[::2]:
                with Horizontal(classes="meter-row"):
                    yield CPUUsage(str(i), i, classes="meter")
                    yield CPUUsage(str(i + 1), i + 1, classes="meter")

            yield Horizontal(RAMUsage("Mem"), classes="meter-row")
            yield Horizontal(SwapUsage("Swp"), classes="meter-row")

        with Vertical(classes="meter-col", id="c2"):
            for i in range(num_cores // 2, num_cores)[::2]:
                with Horizontal(classes="meter-row"):
                    yield CPUUsage(str(i), i, classes="meter")
                    yield CPUUsage(str(i + 1), i + 1, classes="meter")

            yield Horizontal(Tasks(), classes="meter-row")
            yield Horizontal(LoadAverage(), classes="meter-row")
            yield Horizontal(Uptime(), classes="meter-row")
