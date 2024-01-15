from textual.containers import Horizontal, Vertical
import psutil
from ..widgets import *


class MeterRow(Horizontal):
    DEFAULT_CSS = """
    MeterRow {
        height: 1;
        width: 100%;
    }

    MeterRow * {
        height: 1;
        width: 1fr;
        padding-right: 1;
        align-horizontal: right;
    }
    """


class MeterColumn(Vertical):
    DEFAULT_CSS = """
    MeterColumn {
        height: auto;
    }
    """


class Meters(Horizontal):
    DEFAULT_CSS = """

    Meters {
        height: auto;
    }

    Meters .column {
        height: auto;
        padding: 1;
    }

    MeterLayout #c1 {

    }

    MeterLayout #c2 {

    }

    MeterLayout #c3 {

    }

    MeterLayout #c4 {

    }

    """

    def on_mount(self):
        num_cores = psutil.cpu_count()
        cpu_meters = [
            MeterRow(CPUUsage(str(n), n), CPUUsage(str(n + 1), n + 1))
            for n in range(num_cores)[::2]
        ]
        c1_meters = cpu_meters[: len(cpu_meters) // 2]
        c1_meters.extend([MeterRow(RAMUsage("Mem")), MeterRow(SwapUsage("Swp"))])

        c2_meters = cpu_meters[len(cpu_meters) // 2 :]
        c2_meters.extend(
            [MeterRow(Tasks()), MeterRow(LoadAverage()), MeterRow(Uptime())]
        )

        self.query_one("#c1", Vertical).mount_all(c1_meters)
        self.query_one("#c2", Vertical).mount_all(c2_meters)

    def compose(self):
        yield Vertical(classes="column", id="c1")
        yield Vertical(classes="column", id="c2")
