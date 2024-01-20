from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.containers import Horizontal
from textual.widgets.option_list import Option
from .. import *


class MeterLayoutOptions(Horizontal):
    METER_MAPPER = {0: RAMUsage, 1: SwapUsage, 2: Tasks, 3: LoadAverage, 4: Uptime}

    AVAILABLE_METERS = [
        Option("Memory"),
        Option("Swap"),
        Option("Tasks"),
        Option("Load Average"),
        Option("Uptime"),
    ]

    def on_mount(self):
        self.query_one("#col-1-meter-layout").border_title = "Column 1"
        self.query_one("#col-2-meter-layout").border_title = "Column 2"
        self.query_one("#col-3-meter-layout").border_title = "Column 3"
        self.query_one("#col-4-meter-layout").border_title = "Column 4"
        self.query_one("#meter-list").border_title = "Available Meters"

    def compose(self) -> ComposeResult:
        yield OptionList(
            Option("Placeholder 1"),
            Option("Placeholder 2"),
            Option("Placeholder 3"),
            Option("Placeholder 4"),
            id="col-1-meter-layout",
            classes="enabled",
        )
        yield OptionList(
            Option("Placeholder 1"),
            Option("Placeholder 2"),
            Option("Placeholder 3"),
            Option("Placeholder 4"),
            id="col-2-meter-layout",
            classes="enabled",
        )
        yield OptionList(
            Option("Placeholder 1"),
            Option("Placeholder 2"),
            Option("Placeholder 3"),
            Option("Placeholder 4"),
            id="col-3-meter-layout",
            classes="disabled",
        )
        yield OptionList(
            Option("Placeholder 1"),
            Option("Placeholder 2"),
            Option("Placeholder 3"),
            Option("Placeholder 4"),
            id="col-4-meter-layout",
            classes="disabled",
        )

        yield OptionList(*self.AVAILABLE_METERS, id="meter-list")
