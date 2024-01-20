from textual.app import ComposeResult
from textual.widgets import SelectionList
from textual.containers import Container


class MeterHeaderOptions(Container):
    METER_LAYOUT_OPTIONS = (
        ("2 columns - 50/50 (default)", 0),
        ("2 columns - 33/67", 1),
        ("2 columns - 67/33", 2),
        ("3 columns - 33/33/33", 3),
        ("3 columns - 25/25/50", 4),
        ("3 columns - 25/50/25", 5),
        ("3 columns - 50/25/25", 6),
        ("3 columns - 40/30/30", 7),
        ("3 columns - 30/40/30", 8),
        ("3 columns - 30/30/40", 9),
        ("3 columns - 40/20/40", 10),
        ("4 columns - 25/25/25/25", 11),
    )

    def on_mount(self) -> None:
        self.query_one("#meter-layout-options").border_title = "Header Layout"

    def compose(self) -> ComposeResult:
        yield SelectionList(*self.METER_LAYOUT_OPTIONS, id="meter-layout-options")
