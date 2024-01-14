from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

import psutil
from psutil._common import pcputimes
from psutil._pslinux import pmem
from rich.text import Text

STATUS = {
    psutil.STATUS_RUNNING: "R",
    psutil.STATUS_SLEEPING: "S",
    psutil.STATUS_DISK_SLEEP: "D",
    psutil.STATUS_STOPPED: "T",
    psutil.STATUS_TRACING_STOP: "t",
    psutil.STATUS_ZOMBIE: "Z",
    psutil.STATUS_DEAD: "X",
    psutil.STATUS_WAKING: "W",
    psutil.STATUS_PARKED: "P",
    psutil.STATUS_IDLE: "I",
}

USERNAME = os.getlogin()


@dataclass(order=True, eq=True)
class PID:
    pid: int

    def __rich__(self) -> Text:
        return Text(str(self.pid), justify="right")


@dataclass(order=True, eq=True)
class Username:
    username: str

    def __rich__(self) -> Text:
        if self.username != USERNAME:
            return Text(self.username, style="bold bright_black")
        else:
            return Text(self.username)


@dataclass(order=True, eq=True)
class Nice:
    nice: int

    def __rich__(self) -> Text:
        return Text(str(self.nice), justify="right")


@dataclass(order=True, eq=True)
class Priority:
    priority: int

    def __rich__(self) -> Text:
        return Text(str(self.priority), justify="right")


@dataclass(order=True, eq=True)
class Memory:
    size: int

    def __rich__(self) -> Text:
        units = {0: "K", 1: "K", 2: "M", 3: "G", 4: "T"}
        unit_styles = {
            0: "",
            1: "",
            2: "bright_cyan",
            3: "bright_green",
            4: "bright_red",
        }
        unit_key = 0
        data = self.size
        while data > 1024:
            data = data // 1024
            unit_key += 1

        if unit_key == 0:
            return Text("0K")
        elif unit_key == 4:
            return Text(
                f">{str(round(data, 2))}{units[unit_key]}", style=unit_styles[unit_key]
            )
        else:
            return Text(
                f"{str(round(data, 2))}{units[unit_key]}", style=unit_styles[unit_key]
            )


@dataclass(order=True, eq=True)
class Status:
    status: str

    def __rich__(self) -> Text:
        status = STATUS[self.status]
        if status == "R":
            return Text(status, style="bright_green")
        else:
            return Text(status)


@dataclass(order=True, eq=True)
class Percent:
    percent: float

    def __rich__(self) -> Text:
        percent = round(self.percent, 1)
        if self.percent == 0:
            return Text(str(percent), style="bold bright_black")
        else:
            return Text(str(percent))


@dataclass(order=True, eq=True)
class CPUTimes:
    user: float
    system: float

    def __rich__(self) -> Text:
        times = sum((self.user, self.system))
        hours = int(times // 3600)
        minutes = str(int(times % 3600 // 60))
        seconds = str(int(times % 3600 % 60)).zfill(2)
        milliseconds = str(int(times % 3600 % 60 % 1 * 100)).zfill(2)
        if hours > 0:
            return Text(f"{hours}hr{minutes}:{seconds}")
        else:
            return Text(f"{minutes}:{seconds}.{milliseconds}")


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
        self.pid = PID(pid)
        self.ppid = ppid
        self.name = name
        self.username = Username(username)
        self.nice = Nice(nice)
        self.pri = Priority(nice)

        self.virt = Memory(memory_info.vms)
        self.res = Memory(memory_info.rss)
        self.shr = Memory(memory_info.shared)
        self.status = Status(status)
        self.cpu_percent = Percent(cpu_percent)
        self.memory_percent = Percent(memory_percent)

        user, system = cpu_times.user, cpu_times.system
        self.cpu_times = CPUTimes(user, system)
        self.num_threads = num_threads

        if cmdline is None:
            self.cmdline = name
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


class CPU:
    cores = {}

    def __init__(self):
        self.cores.update(
            {
                core: percent
                for core, percent in enumerate(psutil.cpu_percent(percpu=True))
            }
        )

    def update(self):
        self.cores.update(
            {
                core: percent
                for core, percent in enumerate(psutil.cpu_percent(percpu=True))
            }
        )
