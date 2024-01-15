from textual.app import App
from textual.reactive import Reactive
import psutil

from .screens import Main, Setup
from .widgets import CPUUsage


class Pytop(App):
    SCREENS = {"main": Main(), "setup": Setup()}
    CSS_PATH = "styles/styles.tcss"

    cpu_percent: Reactive[dict[int, float]] = Reactive(
        {cpu: percent for cpu, percent in enumerate(psutil.cpu_percent(percpu=True))}  # type: ignore
    )

    def on_mount(self) -> None:
        self.push_screen("setup")
        self.push_screen("main")
        self.set_interval(1.5, self.calculate_cpus)

    def calculate_cpus(self):
        self.cpu_percent = {
            cpu: percent for cpu, percent in enumerate(psutil.cpu_percent(percpu=True))  # type: ignore
        }

    def watch_cpu_percent(self):
        cpus = self.query(CPUUsage)
        for cpu in self.cpu_percent:
            cpus[cpu].progress = self.cpu_percent[cpu]


def main():
    pytop = Pytop()
    pytop.run()


if __name__ == "__main__":
    main()
