from textual.app import ComposeResult, RenderResult
from textual.widget import Widget
from textual.widgets import DataTable, Placeholder, Static, TextArea, Label
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive, Reactive
from typing_extensions import Literal
from .data import Process
from rich.text import Text

ReadoutType = Literal["percent", "memory", "proportion"]


class Readout(Static):
    pass


class PercentReadout(Static):
    progress = reactive(float)

    def __init__(
        self,
        progress: float,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.progress = progress

    def on_mount(self):
        return f"{self.progress}%"


class TextMeter(Widget):
    label = reactive("")
    progress = reactive(0.0)
    total = reactive(0.0)
    readout = reactive("")
    readout_type: Reactive[ReadoutType] = Reactive[ReadoutType]("percent")

    DEFAULT_CSS = """
    TextMeter {
        width: 1fr;
    }
    """

    def __init__(
        self,
        label: str,
        progress: float,
        total: float,
        readout_type: ReadoutType,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.label = label
        self.progress = progress
        self.total = total
        self.readout_type = readout_type
        self.compute_readout()

    def validate_progress(self, progress: float):
        if progress == 0.0:
            return 0.1
        return progress

    def validate_total(self, total: float):
        if total == 0.0:
            return 0.1
        return total

    def compute_readout(self) -> str:
        match self.readout_type:
            case "percent":
                return f"{self.total}%"
            case "proportion":
                return f"{self.progress}/{self.total}"

    def render(self):
        progress_region_width = (
            self.size.width - 4 - len(self.label) - len(str(self.readout))
        )

        num_bars = int(progress_region_width * self.progress // self.total)
        num_whitespace = progress_region_width - num_bars
        return f"{self.label}[{'[bold green]|' * num_bars}{' ' * num_whitespace}{self.readout}]"
