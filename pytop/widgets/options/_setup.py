from textual.widget import Widget
from textual.widgets import RadioSet, RadioButton, SelectionList
from textual.containers import Horizontal
from ._display_options import DisplayOptions
from ._meter_header_options import MeterHeaderOptions
from ._meter_layout_options import MeterLayoutOptions
from ._process_table_options import ProcessTableOptions


class Setup(Widget):
    SELECTION_MAPPER = {
        0: DisplayOptions,
        1: MeterHeaderOptions,
        2: MeterLayoutOptions,
        3: ProcessTableOptions,
    }

    def on_mount(self):
        self.query_one("#categories", RadioSet).border_title = "Categories"

    def compose(self):
        with Horizontal(id="options-layout"):
            with RadioSet(id="categories"):
                yield RadioButton(
                    "Display options", value=True, id="display-options-radio-button"
                )
                yield RadioButton(
                    "Header layout", value=True, id="header-layout-radio-button"
                )
                yield RadioButton("Meters")
                yield RadioButton("Screens")

            yield DisplayOptions(id="activated-options")

    def on_show(self):
        self.query_one(RadioSet).focus()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.query_one("#activated-options").remove()
        self.query_one("#options-layout").mount(
            self.SELECTION_MAPPER[event.index](id="activated-options")
        )
