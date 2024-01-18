from textual.reactive import Reactive
from textual.widgets import DataTable
from textual.widgets._data_table import ColumnKey
from dataclasses import dataclass
from rich.text import Text
import psutil
import os
from psutil._pslinux import pmem
from psutil._common import pcputimes
from typing import Optional, List
from dataclasses import dataclass


STATUS_MAPPER = {
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

        if cmdline is None:
            self.cmdline = self.name
        else:
            self.cmdline = "".join(cmdline)


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
        status = STATUS_MAPPER[self.status]
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


class ProcessTable(DataTable):
    processes: Reactive[list[Process]] = Reactive([])
    current_sort: tuple[ColumnKey, bool] = (ColumnKey("CPU%"), True)

    def on_mount(self):
        self.cursor_type = "row"
        for label in (
            "PID",
            "USER",
            "PRI",
            "NI",
            "VIRT",
            "RES",
            "SHR",
            "S",
            "CPU%",
            "MEM%",
            "TIME+",
            "Command",
        ):
            self.add_column(label, key=label)

        self.fixed_rows = 0
        self.sort(self.current_sort[0], reverse=self.current_sort[1])

    def watch_processes(self):
        old_keys = set(row.value for row in self.rows.copy())
        new_keys = set()
        for p in self.processes:
            row_key = str(p.pid)
            new_keys.add(row_key)
            if row_key in old_keys:
                self.update_cell(row_key, "PRI", Nice(p.nice))
                self.update_cell(row_key, "NI", Nice(p.nice))
                self.update_cell(row_key, "VIRT", Memory(p.virt))
                self.update_cell(row_key, "RES", Memory(p.res))
                self.update_cell(row_key, "SHR", Memory(p.shr))
                self.update_cell(row_key, "S", Status(p.status))
                self.update_cell(row_key, "CPU%", Percent(p.cpu_percent))
                self.update_cell(row_key, "MEM%", Percent(p.memory_percent))
                self.update_cell(row_key, "Command", p.cmdline)
            else:
                self.add_row(
                    PID(p.pid),
                    Username(p.username),
                    Nice(p.nice),
                    Nice(p.nice),
                    Memory(p.virt),
                    Memory(p.res),
                    Memory(p.shr),
                    Status(p.status),
                    Percent(p.cpu_percent),
                    Percent(p.memory_percent),
                    CPUTimes(p.cpu_times.user, p.cpu_times.system),
                    p.cmdline,
                    key=row_key,
                )

        diff = old_keys.difference(new_keys)
        for row_key in diff:
            assert isinstance(row_key, str)
            self.remove_row(row_key)

        self.sort(self.current_sort[0], reverse=self.current_sort[1])

    def on_data_table_header_selected(self, selected: DataTable.HeaderSelected):
        if self.current_sort[0] == selected.column_key:
            self.current_sort = (selected.column_key, not self.current_sort[1])
        else:
            self.current_sort = (selected.column_key, True)
        self.sort(self.current_sort[0], reverse=self.current_sort[1])
