from ._memory_usage import MemoryUsage
from textual.reactive import Reactive
from psutil._pslinux import svmem
import psutil


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
