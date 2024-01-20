from textual.app import ComposeResult
from textual.widgets import SelectionList
from textual.containers import Horizontal


class MeterLayoutOptions(Horizontal):
    def on_mount(self):
        self.query_one("#col-1-meter-layout").border_title = "Column 1"
        self.query_one("#col-2-meter-layout").border_title = "Column 2"
        self.query_one("#meter-list").border_title = "Available Meters"

    def compose(self) -> ComposeResult:
        yield SelectionList(
            ("1", 1), ("2", 2), ("3", 3), ("4", 4), id="col-1-meter-layout"
        )
        yield SelectionList(
            ("1", 1), ("2", 2), ("3", 3), ("4", 4), id="col-2-meter-layout"
        )
        yield SelectionList(("okay jose", 1), id="meter-list")
