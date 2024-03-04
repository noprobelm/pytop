from textual.containers import Vertical, Horizontal
import psutil
from ..widgets import *
from collections import namedtuple


class Meters(Horizontal):
    def compose(self):
        num_cores = psutil.cpu_count()

        with Vertical(id="c1"):
            for i in range(num_cores // 2)[::2]:
                with Horizontal(classes="meter-row"):
                    yield CPUUsage(i, classes="meter")
                    yield CPUUsage(i + 1, classes="meter")

            yield Horizontal(RAMUsage("Mem", classes="meter"), classes="meter-row")
            yield Horizontal(SwapUsage("Swp", classes="meter"), classes="meter-row")

        with Vertical(id="c2"):
            for i in range(num_cores // 2, num_cores)[::2]:
                with Horizontal(classes="meter-row"):
                    yield CPUUsage(i, classes="meter")
                    yield CPUUsage(i + 1, classes="meter")

            yield Horizontal(Tasks(classes="meter"), classes="meter-row")
            yield Horizontal(LoadAverage(classes="meter"), classes="meter-row")
            yield Horizontal(Uptime(classes="meter"), classes="meter-row")
