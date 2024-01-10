from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, ProgressBar, Placeholder, Static
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive, Reactive
from typing_extensions import Literal
from . import data


class CPUBar(ProgressBar):
    def __init__(self, percent: float, *args, **kwargs):
        self.percent = percent
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        """Set up a timer to simulate progess happening."""
        self.progress_timer = self.set_interval(1.5, self.update_usage)

    def update_usage(self):
        self.update(total=100.0)
        self.progress = self.percent


class ProcessTable(DataTable):
    processes: dict[str, data.Process] = {}
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
        self.update_processes()
        self.set_interval(1.5, self.update_processes)
        self.sort(self.current_sort[0], reverse=self.current_sort[1])

    def update_processes(self):
        self.processes = data.get_processes()
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


class Progress(Static):
    progress = reactive(0.0)
    total = reactive(0.0)

    DEFAULT_CSS = """
    Progress {
        align-horizontal: left;
        overflow: hidden;
    }
    """

    def watch_progress(self):
        num_bars = int(self.size.width * self.progress // self.total)
        self.update(f"{'|' * num_bars}{' ' * (self.size.width - num_bars)}")


class TextProgressBar(Static):
    readout_type: Reactive[ReadoutType] = Reactive[ReadoutType]("percent")
    progress: Reactive[float] = Reactive[float](0.0)
    DEFAULT_CSS = """
    Meter {
        align-horizontal: left;
        overflow: hidden;
        color: $text;
    }
    """

    def __init__(
        self,
        label: str,
        total: float,
        show_progress: bool = False,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self.label = label
        self.total = total
        self.show_progress = False
        super().__init__(name=name, id=id, classes=classes)

    def watch_progress(self):
        num_bars = int(self.size.width * self.progress // self.total)
        self.update(f"[{'|' * num_bars}{' ' * (self.size.width - num_bars)}]")

    def render(self):
        bar_width = self.size.width - len(self.label) - len(str(self.progress)) - 2
        num_bars = int(bar_width * self.progress // self.total)
        bars = "|" * num_bars
        empty = " " * (bar_width - len(bars))
        return f"{self.label}[{bars}{empty}{self.progress}]"


class PercentBar(TextProgressBar):
    def __init__(
        self,
        cpu_core: int,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        label = str(cpu_core)
        total = 100.0
        super().__init__(label, total, False, name=name, id=id, classes=classes)

    def on_mount(self):
        self.progress = 25.0
