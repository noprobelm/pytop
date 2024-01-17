from __future__ import annotations

from typing import List, Optional

import psutil
from psutil._common import pcputimes
from psutil._pslinux import pmem


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


class Processes:
    def __init__(self):
        self.num_tasks, self.num_threads, self.num_kthreads, self.num_running = (
            0,
            0,
            0,
            0,
        )
        self.processes = {}
        self.query_processes()

    def query_processes(self):
        self.processes = {}
        self.num_tasks, self.num_threads, self.num_kthreads, self.num_running = (
            0,
            0,
            0,
            0,
        )
        process_data = psutil.process_iter()
        for data in process_data:
            with data.oneshot():
                process = Process(
                    data.pid,
                    data.ppid(),
                    data.name(),
                    data.username(),
                    data.nice(),
                    data.memory_info(),
                    data.status(),
                    data.cpu_percent(),
                    data.memory_percent(),
                    data.cpu_times(),
                    data.num_threads(),
                    data.cmdline(),
                )
                if process.ppid != 2:
                    self.num_tasks += 1
                if not process.cmdline:
                    self.num_kthreads += 1
                if process.status == psutil.STATUS_RUNNING:
                    self.num_running += 1
                self.num_threads += process.num_threads

                self.processes[str(process.pid)] = process
