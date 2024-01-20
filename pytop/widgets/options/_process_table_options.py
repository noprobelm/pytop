from textual.containers import Horizontal
from textual.widgets import SelectionList


class ProcessTableOptions(Horizontal):
    ACTIVE_SCREENS = (("Main", 0), ("IO", 0))
    ACTIVE_COLUMNS = (("PID", 0), ("USER", 1))
    AVAILABLE_COLUMNS = (("PID", 0), ("USER", 1))

    def on_mount(self):
        self.query_one("#screens-list").border_title = "Screens"
        self.query_one("#active-columns-list").border_title = "Active Columns"
        self.query_one("#available-columns-list").border_title = "Available Columns"

    def compose(self):
        yield SelectionList(*self.ACTIVE_SCREENS, id="screens-list")
        yield SelectionList(*self.ACTIVE_COLUMNS, id="active-columns-list")
        yield SelectionList(*self.AVAILABLE_COLUMNS, id="available-columns-list")
