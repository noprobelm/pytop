from textual.reactive import Reactive
from textual.widgets import Static
from .text_progress_bar import TextProgressBar
import psutil
from time import time


class CPUUsage(TextProgressBar):
    def __init__(
        self,
        label: str,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(label, 100.0, "percent", name=name, id=id, classes=classes)


class MemoryUsage(TextProgressBar):
    def __init__(
        self,
        label: str,
        total: float,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self._total_readout = self._convert_units(total)
        super().__init__(label, total, "proportion", name=name, id=id, classes=classes)

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

    def compute__readout(self) -> str:
        if self.progress is None or self.total is None:
            return f"-/-"
        used = self._convert_units(self.progress)
        total = self._convert_units(self.total)
        return f"{used}/{total}"


class LoadAverage(Static):
    """A meter for displaying 1, 5, and 15 minute CPU load averages"""

    load_avg: Reactive[tuple] = Reactive(psutil.getloadavg)

    def on_mount(self) -> None:
        self.set_interval(1.5, self.update_load_avg)

    def update_load_avg(self) -> None:
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


class Uptime(Static):
    """A meter for displaying time elapsed since system boot"""

    boot_time = psutil.boot_time()
    current_time: Reactive[float] = Reactive(time)

    def on_mount(self) -> None:
        self.set_interval(1.5, self.update_time)

    def update_time(self) -> None:
        self.current_time = time()

    def watch_current_time(self) -> None:
        self.update()

    def render(self) -> str:
        uptime_seconds = self.current_time - self.boot_time
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)
        return f"Uptime: {int(h):02d}:{int(m):02d}:{int(s):02d}"


class Tasks(Static):
    """A meter for displaying number of tasks running"""

    num_tasks: Reactive[int] = Reactive(0)
    num_threads: Reactive[int] = Reactive(0)
    num_kthreads: Reactive[int] = Reactive(0)
    num_running: Reactive[int] = Reactive(0)

    def render(self) -> str:
        return f"Tasks: {self.num_tasks}, {self.num_threads} thr, {self.num_kthreads} kthr; {self.num_running} running"
