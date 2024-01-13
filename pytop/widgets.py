from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Placeholder, Static, TextArea
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive, Reactive
from typing_extensions import Literal
from .data import Process
import psutil
from datetime import datetime, timedelta


class ProcessTable(DataTable):
    processes = reactive({})
    current_sort = ("CPU%", True)

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
        queued = set(self.processes.keys())
        rows = self.rows.copy()
        for row_key in rows:
            pid = row_key.value
            assert pid is not None

            if pid not in self.processes.keys():
                self.remove_row(pid)
                continue
            p = self.processes[pid]
            self.update_cell(pid, "PRI", p.nice)
            self.update_cell(pid, "NI", p.nice)
            self.update_cell(pid, "VIRT", p.virt)
            self.update_cell(pid, "RES", p.res)
            self.update_cell(pid, "SHR", p.shr)
            self.update_cell(pid, "S", p.status)
            self.update_cell(pid, "CPU%", p.cpu_percent)
            self.update_cell(pid, "MEM%", p.memory_percent)
            self.update_cell(pid, "Command", p.cmdline)
            queued.remove(pid)

        for pid in queued:
            p = self.processes[pid]
            self.add_row(
                p.pid,
                p.username,
                p.nice,
                p.nice,
                p.virt,
                p.res,
                p.shr,
                p.status,
                p.cpu_percent,
                p.memory_percent,
                p.cpu_times,
                p.cmdline,
                key=pid,
            )
        self.sort(self.current_sort[0], reverse=self.current_sort[1])

    def on_data_table_header_selected(self, selected: DataTable.HeaderSelected):
        if self.current_sort[0] == selected.column_key:
            self.current_sort = (selected.column_key, not self.current_sort[1])
        else:
            self.current_sort = (selected.column_key, True)
        self.sort(self.current_sort[0], reverse=self.current_sort[1])


ReadoutType = Literal["percent", "size"]


class ProgressBar(Static):
    progress = reactive(25.0)
    total = reactive(100.0)

    DEFAULT_CSS = """
    ProgressBar {
        width: 1fr;
    }
    """

    def __init__(self, progress: float, total: float):
        self.progress = progress
        self.total = total
        super().__init__()

    def render(self):
        num_bars = int((self.size.width * self.progress // self.total))
        whitespace = self.size.width - num_bars - 2
        return f"[{'[bold green]|' * num_bars}{' ' * whitespace}]"


class CPUMeter(Widget):
    progress = reactive(25.0)
    total = reactive(100.0)

    DEFAULT_CSS = """
    TextProgressBar {
        width: 1fr;
    }
    """

    def __init__(
        self,
        label: str,
        progress: float,
        total: float,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.label = label
        self.progress = progress
        self.total = total

    def validate_progress(self, progress: float):
        if progress == 0:
            return 0.1
        return progress

    def render(self):
        progress_region_width = (
            self.size.width - 4 - len(self.label) - len(str(self.progress))
        )

        num_bars = int(progress_region_width * self.progress // self.total)
        num_whitespace = progress_region_width - num_bars
        return f"{self.label}[{'[bold green]|' * num_bars}{' ' * num_whitespace}{self.progress}%]"

    # def render(self):
    #     bar_width = self.size.width - len(self.label) - len(str(self.progress)) - 2
    #     num_bars = int(bar_width * self.progress // self.total)
    #     bars = "|" * num_bars
    #     empty = " " * (bar_width - len(bars))
    #     return f"{self.label}[{bars}{empty}{self.progress}]"


class LoadAverage(Static):
    one: Reactive[float] = Reactive(0.0)
    five: Reactive[float] = Reactive(0.0)
    fifteen: Reactive[float] = Reactive(0.0)

    def on_mount(self):
        self.set_interval(1.5, self.update_averages)

    def update_averages(self):
        load_avg = psutil.getloadavg()
        self.one, self.five, self.fifteen = load_avg[0], load_avg[1], load_avg[2]

    def render(self):
        return f"Load average: {round(self.one, 2)} {round(self.five, 2)} {round(self.fifteen, 2)}"


class Uptime(Static):
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime: Reactive[timedelta] = Reactive(datetime.now() - boot_time)

    def on_mount(self):
        self.set_interval

    def __init__(self):
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
