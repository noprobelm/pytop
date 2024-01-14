from textual.app import ComposeResult
from textual.reactive import Reactive
from textual.widgets import Static, Label
from textual.containers import Container, Horizontal, Vertical, Grid
from .text_progress_bar import TextProgressBar
import psutil
from psutil._pslinux import svmem
from psutil._common import sswap
from time import time


class Meter(Static):
    DEFAULT_CSS = """
    Meter {
        height: 1;
        width: 1fr;
        padding-right: 1;
    }
    """

    def on_mount(self):
        self.update_meter = self.set_interval(1.5, self.update_data)

    def update_data(self):
        pass


class CPUUsage(TextProgressBar):
    """A meter for displaying CPU usage (per core) as a text progress meter"""

    DEFAULT_CSS = """
    CPUUsage {
        height: 1;
        width: 1fr;
    }
    """

    def __init__(
        self,
        label: str,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self.label = label
        super().__init__(label, "percent", name=name, id=id, classes=classes)


class MemoryUsage(TextProgressBar):
    """A meter for displaying memory usage as a text progress meter"""

    DEFAULT_CSS = """
    MemoryUsage {
        height: 1;
        width: 1fr;
    }
    """

    def __init__(
        self,
        label: str,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self.label = label
        super().__init__(label, "proportion", name=name, id=id, classes=classes)

    def watch_total(self, total):
        self.total_readout = self._convert_units(total)

    def compute__readout(self) -> str:
        if self.progress is None or self.total is None:
            return f"-/-"
        used = self._convert_units(self.progress)
        total = self._convert_units(self.total)
        return f"{used}/{total}"

    def _convert_units(self, data: int | float):
        units = {0: "K", 1: "K", 2: "M", 3: "G", 4: "T"}
        unit_key = 0
        while data > 1024:
            data = data / 1024
            unit_key += 1

        if unit_key == 0:
            return "0K"
        elif unit_key == 4:
            return f">{str(round(data, 2))}{units[unit_key]}"
        else:
            return f"{str(round(data, 1))}{units[unit_key]}"


class RAMUsage(MemoryUsage):
    """A meter for displaying Random Access Memory (RAM) usage"""

    virtual_memory: Reactive[svmem] = Reactive(psutil.virtual_memory)

    def on_mount(self):
        self.progress = self.virtual_memory.used
        self.total = self.virtual_memory.total
        self.update_data = self.set_interval(1.5, self.update_virtual_memory)

    def start(self):
        self.update_data.pause()

    def stop(self):
        self.update_data.resume()

    def update_virtual_memory(self):
        self.virtual_memory = psutil.virtual_memory()

    def watch_virtual_memory(self):
        self.progress = self.virtual_memory.used
        self.update()


class SwapUsage(MemoryUsage):
    """A meter for displaying swap memory usage"""

    swap_memory: Reactive[sswap] = Reactive(psutil.swap_memory)

    def on_mount(self):
        self.progress = self.swap_memory.used
        self.total = self.swap_memory.total
        self.update_data = self.set_interval(1.5, self.update_swap_memory)

    def start(self):
        self.update_data.pause()

    def stop(self):
        self.update_data.resume()

    def update_swap_memory(self):
        self.swap_memory = psutil.swap_memory()

    def watch_swap_memory(self):
        self.progress = self.swap_memory.used
        self.update()


class LoadAverage(Meter):
    """A meter for displaying 1, 5, and 15 minute CPU load averages"""

    load_avg: Reactive[tuple] = Reactive(psutil.getloadavg)

    def update_data(self) -> None:
        self.load_avg = psutil.getloadavg()

    def watch_loadavg(self) -> None:
        self.update()

    def render(self) -> str:
        self.one, self.five, self.fifteen = (
            self.load_avg[0],
            self.load_avg[1],
            self.load_avg[2],
        )
        return f"Load average: {round(self.one, 2)} {round(self.five, 2)} {round(self.fifteen, 2)}"


class Uptime(Meter):
    """A meter for displaying time elapsed since system boot"""

    boot_time = psutil.boot_time()
    current_time: Reactive[float] = Reactive(time)

    def update_data(self) -> None:
        self.current_time = time()

    def watch_current_time(self) -> None:
        self.update()

    def render(self) -> str:
        uptime_seconds = self.current_time - self.boot_time
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)
        return f"Uptime: {int(h):02d}:{int(m):02d}:{int(s):02d}"


class Tasks(Meter):
    """A meter for displaying number of tasks running"""

    num_tasks: Reactive[int] = Reactive(0)
    num_threads: Reactive[int] = Reactive(0)
    num_kthreads: Reactive[int] = Reactive(0)
    num_running: Reactive[int] = Reactive(0)

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Tasks: ")
            yield Static(f"{self.num_tasks}")

    # def render(self) -> str:
    #     return f"Tasks: {self.num_tasks}, {self.num_threads} thr, {self.num_kthreads} kthr; {self.num_running} running"
