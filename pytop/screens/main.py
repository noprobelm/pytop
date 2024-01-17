from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import Footer, Placeholder
from textual.reactive import Reactive
from ..widgets import CPUUsage, ProcessTable, Tasks, MeterHeader, Setup
from ..widgets._process_table import TaskMetrics, Process
import psutil


class Main(Screen):
    processes: Reactive[dict[str, Process]] = Reactive({})
    task_metrics: Reactive[TaskMetrics] = Reactive(TaskMetrics(0, 0, 0, 0))
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

    def compose(self) -> ComposeResult:
        yield MeterHeader()
        yield ProcessTable()
        yield Footer()

    def on_mount(self) -> None:
        self.process_query = self.set_interval(1.5, self.update_processes)
        self.cpu_query = self.set_interval(1.5, self.update_cpu_percent)
        self.update_processes()

    def start_process_query(self) -> None:
        self.process_query.resume()

    def stop_process_query(self) -> None:
        self.process_query.pause()

    def start_cpu_query(self) -> None:
        self.cpu_query.resume()

    def stop_cpu_query(self) -> None:
        self.cpu_query.pause()

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

        self.task_metrics = TaskMetrics(
            num_tasks, num_threads, num_kthreads, num_running
        )

        self.processes = processes

    def watch_processes(self) -> None:
        top = self.query_one(ProcessTable)
        top.processes = self.processes

        tasks = self.query_one(Tasks)
        tasks.num_tasks = self.task_metrics.num_tasks
        tasks.num_threads = self.task_metrics.num_threads
        tasks.num_kthreads = self.task_metrics.num_kthreads
        tasks.num_running = self.task_metrics.num_running

    def update_cpu_percent(self) -> None:
        self.cpu_percent = {
            core: percent
            for core, percent in enumerate(psutil.cpu_percent(percpu=True))  # type: ignore
        }

    def watch_cpu_percent(self) -> None:
        cpus = self.query(CPUUsage)
        for cpu in cpus:
            cpu.progress = self.cpu_percent[cpu.core]
