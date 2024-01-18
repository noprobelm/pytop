from textual.widget import Widget
from textual.message import Message
import psutil
from collections import namedtuple
from psutil._pslinux import pmem
from psutil._common import pcputimes
from typing import Optional, List


class Process:
    def __init__(
        self,
        pid: int,
        ppid: int,
        name: str,
        username: str,
        nice: int,
        memory_info: pmem,
        status: str,
        cpu_percent: float,
        memory_percent: float,
        cpu_times: pcputimes,
        num_threads: int,
        cmdline: Optional[List[str]] = None,
    ):
        self.pid = pid
        self.ppid = ppid
        self.name = name
        self.username = username
        self.nice = nice
        self.pri = nice
        self.virt = memory_info.vms
        self.res = memory_info.rss
        self.shr = memory_info.shared
        self.status = status
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent

        self.cpu_times = cpu_times
        self.num_threads = num_threads
        self.name = name

        if cmdline is None:
            self.cmdline = self.name
        else:
            self.cmdline = "".join(cmdline)


TaskMetrics = namedtuple(
    "TaskMetrics", ["num_tasks", "num_threads", "num_kthreads", "num_running"]
)


class ProcessHandler(Widget):
    class Update(Message):
        def __init__(self, processes: dict[str, Process], task_metrics: TaskMetrics):
            self.processes = processes
            self.task_metrics = task_metrics
            super().__init__()

    def on_mount(self):
        self.set_interval(1.5, self.update_processes)

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

        self.post_message(self.Update(processes, task_metrics))
