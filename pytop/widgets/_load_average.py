import psutil
from rich.text import Text
from textual.reactive import Reactive
from textual.widgets import Static


class LoadAverage(Static):
    """A meter for displaying 1, 5, and 15 minute CPU load averages"""

    COMPONENT_CLASSES = {
        "loadaverage--label",
        "loadaverage--one-minute",
        "loadaverage--five-minute",
        "loadaverage--fifteen-minute",
    }

    DEFAULT_CSS = """
    LoadAverage .loadaverage--label {
        color: $primary-lighten-3;
    }

    LoadAverage .loadaverage--one-minute{
        color: $text;
    }
    LoadAverage .loadaverage--five-minute{
        color: $text-muted;
    }
    LoadAverage .loadaverage--fifteen-minute{
        color: $text-disabled;
    }

    """

    load_avg: Reactive[tuple] = Reactive(psutil.getloadavg)

    def on_mount(self):
        self.set_interval(1.5, self.update_loadavg)

    def update_loadavg(self) -> None:
        self.load_avg = psutil.getloadavg()

    def render(self) -> Text:
        self.one, self.five, self.fifteen = (
            self.load_avg[0],
            self.load_avg[1],
            self.load_avg[2],
        )

        label = "Load Average: "
        one_minute = f"{round(self.one, 2)} "
        five_minute = f"{round(self.five, 2)} "
        fifteen_minute = f"{round(self.fifteen, 2)}"

        label_style = self.get_component_rich_style("loadaverage--label")
        one_minute_style = self.get_component_rich_style("loadaverage--one-minute")
        five_minute_style = self.get_component_rich_style("loadaverage--five-minute")
        fifteen_minute_style = self.get_component_rich_style(
            "loadaverage--fifteen-minute"
        )

        return Text.assemble(
            (label, label_style),
            (one_minute, one_minute_style),
            (five_minute, five_minute_style),
            (fifteen_minute, fifteen_minute_style),
        )
