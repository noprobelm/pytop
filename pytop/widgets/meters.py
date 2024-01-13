from textual.reactive import Reactive
from textual.widgets import Static
import psutil
from time import time


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
