from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import Footer, Placeholder
from textual.reactive import Reactive
from ..data import data
from ..widgets import CPUUsage, ProcessTable, Tasks, MeterHeader, Setup
import psutil


class Main(Screen):
    processes: Reactive[data.Processes] = Reactive(data.Processes())
    cpu_percent: Reactive[dict[int, float]] = Reactive(
        {core: percent for core, percent in enumerate(psutil.cpu_percent(percpu=True))}  # type: ignore
    )

    BINDINGS = [
        Binding(key="F3", action="search", description="Search"),
        Binding(key="F4", action="filter", description="Filter"),
        Binding(key="F5", action="tree", description="Tree"),
        Binding(key="F6", action="sortby", description="SortBy"),
        Binding(key="F7", action="nice_down", description="Nice -"),
        Binding(key="F8", action="nice_up", description="Nice +"),
        Binding(key="F9", action="kill", description="Kill"),
        Binding(key="F10", action="quit", description="Quit"),
    ]

    def on_mount(self) -> None:
        self.set_interval(1.5, self.update_processes)
        self.set_interval(1.5, self.update_cpu_percent)
        self.update_processes()

    def update_processes(self) -> None:
        self.processes.query_processes()
        top = self.query_one(ProcessTable)
        top.processes = self.processes.processes

        tasks = self.query_one(Tasks)
        tasks.num_tasks = self.processes.num_tasks
        tasks.num_threads = self.processes.num_threads
        tasks.num_kthreads = self.processes.num_kthreads
        tasks.num_running = self.processes.num_running

    def update_cpu_percent(self) -> None:
        self.cpu_percent = {
            core: percent
            for core, percent in enumerate(psutil.cpu_percent(percpu=True))
        }

    def watch_cpu_percent(self) -> None:
        cpus = self.query(CPUUsage)
        for cpu in cpus:
            cpu.progress = self.cpu_percent[cpu.core]

    def compose(self) -> ComposeResult:
        yield MeterHeader()
        yield ProcessTable()
        yield Footer()
