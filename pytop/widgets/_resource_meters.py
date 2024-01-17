import psutil
from psutil._common import sswap
from psutil._pslinux import svmem
from textual.reactive import Reactive
from ._text_progress_bar import TextProgressBar


class MemoryUsage(TextProgressBar):
    """A meter for displaying memory usage as a text progress meter"""

    DEFAULT_CSS = """
    MemoryUsage {
        height: 1;
        width: 1fr;
    }
    """

    def __init__(
        self,
        label: str,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self.label = label
        super().__init__(label, "proportion", name=name, id=id, classes=classes)

    def watch_total(self, total):
        self.total_readout = self._convert_units(total)

    def compute__readout(self) -> str:
        if self.progress is None or self.total is None:
            return f"-/-"
        used = self._convert_units(self.progress)
        total = self._convert_units(self.total)
        return f"{used}/{total}"

    def _convert_units(self, data: int | float):
        units = {0: "K", 1: "K", 2: "M", 3: "G", 4: "T"}
        unit_key = 0
        while data > 1024:
            data = data / 1024
            unit_key += 1

        if unit_key == 0:
            return "0K"
        elif unit_key == 4:
            return f">{str(round(data, 2))}{units[unit_key]}"
        else:
            return f"{str(round(data, 1))}{units[unit_key]}"


class RAMUsage(MemoryUsage):
    """A meter for displaying Random Access Memory (RAM) usage"""

    virtual_memory: Reactive[svmem] = Reactive(psutil.virtual_memory)

    def on_mount(self):
        self.progress = self.virtual_memory.used
        self.total = self.virtual_memory.total
        self.update_data = self.set_interval(1.5, self.update_virtual_memory)

    def start(self):
        self.update_data.pause()

    def stop(self):
        self.update_data.resume()

    def update_virtual_memory(self):
        self.virtual_memory = psutil.virtual_memory()

    def watch_virtual_memory(self):
        self.progress = self.virtual_memory.used
        self.update()


class SwapUsage(MemoryUsage):
    """A meter for displaying swap memory usage"""

    swap_memory: Reactive[sswap] = Reactive(psutil.swap_memory)

    def on_mount(self):
        self.progress = self.swap_memory.used
        self.total = self.swap_memory.total
        self.update_data = self.set_interval(1.5, self.update_swap_memory)

    def start(self):
        self.update_data.pause()

    def stop(self):
        self.update_data.resume()

    def update_swap_memory(self):
        self.swap_memory = psutil.swap_memory()

    def watch_swap_memory(self):
        self.progress = self.swap_memory.used
        self.update()
