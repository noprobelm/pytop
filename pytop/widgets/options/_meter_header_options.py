from textual.app import ComposeResult
from textual.widgets import RadioButton, RadioSet
from textual.containers import Container


class MeterHeaderOptions(Container):
    def on_mount(self) -> None:
        self.query_one("#meter-layout-options").border_title = "Header Layout"

    def compose(self) -> ComposeResult:
        with RadioSet(id="meter-layout-options"):
            yield RadioButton("2 columns - 50/50 (default)")
            yield RadioButton("2 columns - 33/67")
            yield RadioButton("2 columns - 67/33")
            yield RadioButton("3 columns - 33/33/33")
            yield RadioButton("3 columns - 25/25/50")
            yield RadioButton("3 columns - 25/50/25")
            yield RadioButton("3 columns - 50/25/25")
            yield RadioButton("3 columns - 40/30/30")
            yield RadioButton("3 columns - 30/40/30")
            yield RadioButton("3 columns - 30/30/40")
            yield RadioButton("3 columns - 40/20/40")
            yield RadioButton("4 columns - 25/25/25/25")

    def on_radio_set_changed(self, event: RadioSet.Changed):
        event.stop()
