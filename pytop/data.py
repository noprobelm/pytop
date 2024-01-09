from __future__ import annotations
import psutil
from psutil._pslinux import pmem
from psutil._common import pcputimes
from typing import List, Optional

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


def get_processes() -> dict[str, Process]:
    processes = {
        str(p.pid): Process(
            p.pid,
            p.name(),
            p.username(),
            p.nice(),
            p.memory_info(),
            p.status(),
            p.cpu_percent(),
            p.memory_percent(),
            p.cpu_times(),
            p.cmdline(),
        )
        for p in psutil.process_iter()
    }
    return processes


class Process:
    def __init__(
        self,
        pid: int,
        name: str,
        username: str,
        nice: int,
        memory_info: pmem,
        status: str,
        cpu_percent: float,
        memory_percent: float,
        cpu_times: pcputimes,
        cmdline: Optional[List[str]] = None,
    ):
        self.pid = pid
        self.name = name
        self.username = username
        self.nice = nice
        self.pri = nice

        self.virt = self._format_bytes(memory_info.vms)
        self.res = self._format_bytes(memory_info.rss)
        self.shr = self._format_bytes(memory_info.shared)
        self.status = STATUS[status]
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent

        user, system = cpu_times.user, cpu_times.system
        self.cpu_times = sum((user, system))

        if cmdline is None:
            self.cmdline = name
        else:
            self.cmdline = "".join(cmdline)

    def _format_bytes(self, data: int):
        units = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T"}
        unit_key = 0
        exp = 2**10
        while data > exp:
            data = data // exp
            unit_key += 1

        if unit_key == 0:
            return "0K"
        return f"{str(round(data, 2)).zfill(2)}{units[unit_key]}"


def parse_pcputimes(pcputimes: pcputimes):
    user, system = pcputimes.user, pcputimes.system
    return sum((user, system))


def parse_cmdline(cmdline: Optional[List[str]] = None) -> str:
    if cmdline is None:
        return ""
    return " ".join(cmdline)


def parse_status(status: str):
    return STATUS[status]
