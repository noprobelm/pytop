from __future__ import annotations
from textual.app import ComposeResult
from textual.message import Message
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer
from textual.reactive import Reactive
from ..widgets import CPUUsage, ProcessTable, Tasks, MeterHeader, Setup
from ..widgets._process_table import TaskMetrics, Process
import psutil


class Main(Screen):
    cpu_percent: Reactive[dict[int, float]] = Reactive(
        {core: percent for core, percent in enumerate(psutil.cpu_percent(percpu=True))}  # type: ignore
    )

    BINDINGS = [
        Binding(key="f2", action="toggle_setup", description="Search"),
        Binding(key="F3", action="search", description="Search"),
        Binding(key="F4", action="filter", description="Filter"),
        Binding(key="F5", action="tree", description="Tree"),
        Binding(key="F6", action="sortby", description="SortBy"),
        Binding(key="F7", action="nice_down", description="Nice -"),
        Binding(key="F8", action="nice_up", description="Nice +"),
        Binding(key="F9", action="kill", description="Kill"),
        Binding(key="F10", action="quit", description="Quit"),
    ]

    class ProcessesUpdated(Message):
        def __init__(self, processes: dict[str, Process], task_metrics: TaskMetrics):
            self.processes = processes
            self.task_metrics = task_metrics
            super().__init__()

    def compose(self) -> ComposeResult:
        yield MeterHeader()
        yield ProcessTable(classes="activated")
        yield Setup(classes="deactivated")
        yield Footer()

    def on_mount(self) -> None:
        self.process_query = self.set_interval(1.5, self.update_processes)
        self.cpu_query = self.set_interval(1.5, self.update_cpu_percent)
        self.update_processes()

    def on_main_processes_updated(self, message: Main.ProcessesUpdated):
        top = self.query_one(ProcessTable)
        top.processes = message.processes

        tasks = self.query_one(Tasks)
        tasks.num_tasks = message.task_metrics.num_tasks
        tasks.num_threads = message.task_metrics.num_threads
        tasks.num_kthreads = message.task_metrics.num_kthreads
        tasks.num_running = message.task_metrics.num_running

    def update_processes(self) -> None:
        processes = {}
        num_tasks, num_threads, num_kthreads, num_running = 0, 0, 0, 0
        process_query = psutil.process_iter()
        for p in process_query:
            with p.oneshot():
                process = Process(
                    p.pid,
                    p.ppid(),
                    p.name(),
                    p.username(),
                    p.nice(),
                    p.memory_info(),
                    p.status(),
                    p.cpu_percent(),
                    p.memory_percent(),
                    p.cpu_times(),
                    p.num_threads(),
                    p.cmdline(),
                )
                if p.ppid != 2:
                    num_tasks += 1
                if not process.cmdline:
                    num_kthreads += 1
                if process.status == psutil.STATUS_RUNNING:
                    num_running += 1
                num_threads += process.num_threads

                processes[str(process.pid)] = process

        task_metrics = TaskMetrics(num_tasks, num_threads, num_kthreads, num_running)

        processes = processes
        self.post_message(self.ProcessesUpdated(processes, task_metrics))

    def update_cpu_percent(self) -> None:
        self.cpu_percent = {
            core: percent
            for core, percent in enumerate(psutil.cpu_percent(percpu=True))  # type: ignore
        }

    def watch_cpu_percent(self) -> None:
        cpus = self.query(CPUUsage)
        for cpu in cpus:
            cpu.progress = self.cpu_percent[cpu.core]

    def action_toggle_setup(self):
        top = self.query_one(ProcessTable).toggle_class("activated", "deactivated")
        self.focused = top
        self.query_one(Setup).toggle_class("activated", "deactivated")
