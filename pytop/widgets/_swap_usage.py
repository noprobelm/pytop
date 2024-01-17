from ._memory_usage import MemoryUsage
from textual.reactive import Reactive
from psutil._common import sswap
import psutil


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
