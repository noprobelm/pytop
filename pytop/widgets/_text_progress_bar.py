from typing import Optional

from rich.text import Text
from textual.reactive import Reactive
from textual.widgets import Static
from typing_extensions import Literal

ReadoutType = Literal["percent", "proportion"]


class TextProgressBar(Static):
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
        color: $primary-lighten-3;
    }

    TextProgressBar .textprogressbar--readout {
        color: $text-disabled;
    }

    TextProgressBar .textprogressbar--bars {
        color: $text-muted
    }
    """

    def __init__(
        self,
        label: str,
        readout_type: ReadoutType,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.left_bound = "["
        self.right_bound = "]"
        self.label = label
        self.readout_type = readout_type
        if self.readout_type == "percent":
            self.total = 100.0

    def compute__readout(self) -> str:
        if self.progress is None or self.total is None:
            return f"-/-"
        match self.readout_type:
            case "percent":
                return f"{self.progress}%"
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
