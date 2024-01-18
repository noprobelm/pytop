from textual import on
from textual.app import ComposeResult
from textual.message import Message
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer
from ..widgets import CPUUsage, ProcessTable, Tasks, MeterHeader, Setup
from ..widgets._process_table import Process
from ..widgets._tasks import TaskMetrics
import psutil


class Main(Screen):
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
        def __init__(self, processes: list[Process], task_metrics: TaskMetrics):
            self.processes = processes
            self.task_metrics = task_metrics
            super().__init__()

    class CpuPercentUpdated(Message):
        def __init__(self, cpu_percent: dict[int, float]):
            self.cpu_percent = cpu_percent
            super().__init__()

    def compose(self) -> ComposeResult:
        yield MeterHeader()
        yield ProcessTable(classes="activated")
        yield Setup(classes="deactivated")
        yield Footer()

    def on_mount(self) -> None:
        self.update_processes = self.set_interval(1.5, self._query_system_processes)
        self.update_cpu_percent = self.set_interval(1.5, self._measure_cpu_percent)
        self._measure_cpu_percent()
        self._query_system_processes()

    @on(ProcessesUpdated)
    def update_process_widgets(self, message: ProcessesUpdated):
        top = self.query_one(ProcessTable)
        top.processes = message.processes

        tasks = self.query(Tasks)
        for task in tasks:
            task.num_tasks = message.task_metrics.num_tasks
            task.num_threads = message.task_metrics.num_threads
            task.num_kthreads = message.task_metrics.num_kthreads
            task.num_running = message.task_metrics.num_running

    @on(CpuPercentUpdated)
    def update_cpu_meters(self, message: CpuPercentUpdated):
        cpus = self.query(CPUUsage)
        for cpu in cpus:
            cpu.progress = message.cpu_percent[cpu.core]

    def _query_system_processes(self) -> None:
        processes = []
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

                processes.append(process)

        task_metrics = TaskMetrics(num_tasks, num_threads, num_kthreads, num_running)

        self.post_message(self.ProcessesUpdated(processes, task_metrics))

    def _measure_cpu_percent(self) -> None:
        cpu_percent: dict[int, float] = {
            core: percent
            for core, percent in enumerate(psutil.cpu_percent(percpu=True))  # type: ignore
        }
        self.post_message(self.CpuPercentUpdated(cpu_percent))

    def action_toggle_setup(self):
        top = self.query_one(ProcessTable).toggle_class("activated", "deactivated")
        self.focused = top
        self.query_one(Setup).toggle_class("activated", "deactivated")
