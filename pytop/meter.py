from typing import Optional
from textual.app import ComposeResult, RenderResult
from textual.widget import Widget
from textual.widgets import DataTable, Placeholder, Static, TextArea, Label
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive, Reactive
from typing_extensions import Literal
from .data import Process
from rich.text import Text

ReadoutType = Literal["percent", "memory", "proportion"]


class TextProgressBar(Widget):
    progress: Reactive[float | None] = Reactive[Optional[float]](None)
    total: Reactive[float | None] = Reactive[Optional[float]](None)
    readout_type: Reactive[ReadoutType] = Reactive[ReadoutType]("percent")
    _readout: Reactive[str] = Reactive("0.0%")
    _bars: Reactive[str] = Reactive("")

    COMPONENT_CLASSES = {
        "textprogressbar--label",
        "textprogressbar--bound",
        "textprogressbar--readout",
        "textprogressbar--bars",
    }

    DEFAULT_CSS = """
    TextProgressBar .textprogressbar--label {
        color: $primary-lighten-3;
    }

    TextProgressBar .textprogressbar--bound {
        color: $accent-lighten-3;
    }

    TextProgressBar .textprogressbar--readout {
        color: $secondary-background-lighten-2;
    }

    TextProgressBar .textprogressbar--bars {
        color: $secondary
    }
    """

    def __init__(
        self,
        label: str,
        total: float,
        readout_type: ReadoutType,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.label = label
        self.total = total
        self.readout_type = readout_type
        self.left_bound = "["
        self.right_bound = "]"

    def _convert_units(self, data: int | float):
        units = {0: "K", 1: "K", 2: "M", 3: "G", 4: "T"}
        unit_key = 0
        while data > 1024:
            data = data // 1024
            unit_key += 1

        if unit_key == 0:
            return "0K"
        elif unit_key == 4:
            return f">{str(round(data, 2))}{units[unit_key]}"
        else:
            return f"{str(round(data, 2))}{units[unit_key]}"

    def compute__readout(self) -> str:
        if self.progress is None or self.total is None:
            return f"-/-"
        match self.readout_type:
            case "percent":
                return f"{self.progress}%"
            case "memory":
                used = self._convert_units(self.progress)
                total = self._convert_units(self.total)
                return f"{used}/{total}"
            case "proportion":
                return f"{self.progress}/{self.total}"

    def compute__bars(self) -> str:
        bar_region = self.size.width - len(self.label) - len(self._readout) - 2
        if self.progress is None or self.total is None:
            return " " * bar_region

        bars = "|" * int(bar_region * self.progress / self.total)
        whitespace = " " * (bar_region - len(bars))
        return f"{bars}{whitespace}"

    def render(self) -> Text:
        progress_bar = Text()
        progress_bar.append_text(
            Text(
                self.label,
                style=self.get_component_rich_style("textprogressbar--label"),
            )
        )
        progress_bar.append_text(
            Text(
                self.left_bound,
                style=self.get_component_rich_style("textprogressbar--bound"),
            )
        )
        progress_bar.append_text(
            Text(
                self._bars,
                style=self.get_component_rich_style("textprogressbar--bars"),
            ),
        )
        progress_bar.append_text(
            Text(
                self._readout,
                style=self.get_component_rich_style("textprogressbar--readout"),
            )
        )
        progress_bar.append_text(
            Text(
                self.right_bound,
                style=self.get_component_rich_style("textprogressbar--bound"),
            )
        )

        return progress_bar


class CPUUsage(TextProgressBar):
    def __init__(
        self,
        label: str,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(label, 100.0, "percent", name=name, id=id, classes=classes)


class MemoryUsage(TextProgressBar):
    def __init__(
        self,
        label: str,
        total: float,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self._total_readout = self._convert_units(total)
        super().__init__(label, total, "proportion", name=name, id=id, classes=classes)

    def _convert_units(self, data: int | float):
        units = {0: "K", 1: "K", 2: "M", 3: "G", 4: "T"}
        unit_key = 0
        while data > 1024:
            data = data / 1024
            unit_key += 1

        if unit_key == 0:
            return "0K"
        elif unit_key == 4:
            return f">{str(round(data, 1))}{units[unit_key]}"
        else:
            return f"{str(round(data, 1))}{units[unit_key]}"

    def compute__readout(self) -> str:
        if self.progress is None or self.total is None:
            return f"-/-"
        used = self._convert_units(self.progress)
        total = self._convert_units(self.total)
        return f"{used}/{total}"
