from .meters import Meter
import psutil
from textual.reactive import Reactive
from time import time
from rich.text import Text


class Uptime(Meter):
    """A meter for displaying time elapsed since system boot"""

    COMPONENT_CLASSES = {
        "uptime--label",
        "uptime--readout",
    }

    DEFAULT_CSS = """
    Uptime .uptime--label {
        color: $primary-lighten-3;
    }

    Uptime .uptime--readout {
        color: $text;
    }
    """

    boot_time = psutil.boot_time()
    current_time: Reactive[float] = Reactive(time)

    def update_data(self) -> None:
        self.current_time = time()

    def watch_current_time(self) -> None:
        self.update()

    def render(self) -> Text:
        uptime_seconds = self.current_time - self.boot_time
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)

        label = "Uptime: "
        readout = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
        label_style = self.get_component_rich_style("uptime--label")
        readout_style = self.get_component_rich_style("uptime--readout")

        return Text.assemble((label, label_style), (readout, readout_style))
