from textual.reactive import Reactive
from textual.widgets import Static
import psutil
from time import time


class LoadAverage(Static):
    one: Reactive[float] = Reactive(0.0)
    five: Reactive[float] = Reactive(0.0)
    fifteen: Reactive[float] = Reactive(0.0)

    def on_mount(self):
        self.set_interval(1.5, self.update_averages)

    def update_averages(self):
        load_avg = psutil.getloadavg()
        self.one, self.five, self.fifteen = load_avg[0], load_avg[1], load_avg[2]

    def render(self):
        return f"Load average: {round(self.one, 2)} {round(self.five, 2)} {round(self.fifteen, 2)}"


class Uptime(Static):
    boot_time = psutil.boot_time()
    current_time: Reactive[float] = Reactive(time)

    def on_mount(self):
        self.set_interval(1.5, self.update_time)

    def update_time(self):
        self.current_time = time()

    def watch_current_time(self):
        self.update()

    def render(self):
        uptime_seconds = self.current_time - self.boot_time
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)
        return f"Uptime: {int(h):02d}:{int(m):02d}:{int(s):02d}"
