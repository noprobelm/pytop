from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Footer, Placeholder, ProgressBar
from .widgets import ProcessTable
from .meter import TextProgressBar, CPUUsage, MemoryUsage
from textual.containers import Container, Horizontal, Vertical, Grid
from . import data


class Main(Screen):
    processes = data.get_processes()
    cpu = data.CPU()
    virtual_memory = data.VirtualMemory()

    BINDINGS = [
        Binding(key="F1", action="help", description="Help"),
        Binding(key="F2", action="setup", description="Setup"),
        Binding(key="F3", action="search", description="Search"),
        Binding(key="F4", action="filter", description="Filter"),
        Binding(key="F5", action="tree", description="Tree"),
        Binding(key="F6", action="sortby", description="SortBy"),
        Binding(key="F7", action="nice_down", description="Nice -"),
        Binding(key="F8", action="nice_up", description="Nice +"),
        Binding(key="F9", action="kill", description="Kill"),
        Binding(key="F10", action="quit", description="Quit"),
    ]

    STYLES = "styles/styles.tcss"

    def on_mount(self) -> None:
        self.set_interval(1.5, self.update_data)
        self.update_data()

    def update_data(self) -> None:
        top = self.query_one(ProcessTable)
        top.processes = data.get_processes()

        self.cpu.update()
        cpu_meters = self.query(".cpu").results(CPUUsage)
        for i, meter in enumerate(cpu_meters):
            meter.progress = self.cpu.cores[i]

        self.virtual_memory.update()
        virtual_memory_meter = self.query_one(".memory", MemoryUsage)
        virtual_memory_meter.progress = self.virtual_memory.used

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Vertical(
                    Horizontal(
                        CPUUsage("0", classes="cpu"),
                        CPUUsage("1", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        CPUUsage("2", classes="cpu"),
                        CPUUsage("3", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        CPUUsage("4", classes="cpu"),
                        CPUUsage("5", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        CPUUsage("6", classes="cpu"),
                        CPUUsage("7", classes="cpu"),
                        classes="meter-row",
                    ),
                    MemoryUsage("Mem", self.virtual_memory.total, classes="memory"),
                    Placeholder("Swap", classes="meter"),
                    id="col1",
                ),
                Vertical(
                    Horizontal(
                        CPUUsage("8", classes="cpu"),
                        CPUUsage("9", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        CPUUsage("10", classes="cpu"),
                        CPUUsage("11", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        CPUUsage("12", classes="cpu"),
                        CPUUsage("13", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        CPUUsage("14", classes="cpu"),
                        CPUUsage("15", classes="cpu"),
                        classes="meter-row",
                    ),
                    Placeholder("Tasks", classes="meter"),
                    Placeholder("Load Average", classes="meter"),
                    Placeholder("Uptime", classes="meter"),
                    id="col2",
                ),
                id="top",
            ),
            Vertical(ProcessTable(), Footer(), id="bot"),
        )
