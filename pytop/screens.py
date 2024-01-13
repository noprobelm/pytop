from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Footer, Placeholder, ProgressBar
from .widgets import ProcessTable
from .meter import TextProgressBar
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
        cpu_meters = self.query(".cpu").results(TextProgressBar)
        for i, meter in enumerate(cpu_meters):
            meter.progress = self.cpu.cores[i]

        self.virtual_memory.update()
        virtual_memory_meter = self.query_one(".memory")
        virtual_memory_meter.progress = self.virtual_memory.used
        virtual_memory_meter.total = self.virtual_memory.free + self.virtual_memory.used

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Vertical(
                    Horizontal(
                        TextProgressBar("0", 100.0, "percent", classes="cpu"),
                        TextProgressBar("1", 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextProgressBar("2", 100.0, "percent", classes="cpu"),
                        TextProgressBar("3", 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextProgressBar("4", 100.0, "percent", classes="cpu"),
                        TextProgressBar("5", 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextProgressBar("6", 100.0, "percent", classes="cpu"),
                        TextProgressBar("7", 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    TextProgressBar("Mem", 100.0, "memory", classes="memory"),
                    Placeholder("Swap", classes="meter"),
                    id="col1",
                ),
                Vertical(
                    Horizontal(
                        TextProgressBar("8", 100.0, "percent", classes="cpu"),
                        TextProgressBar("9", 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextProgressBar("10", 100.0, "percent", classes="cpu"),
                        TextProgressBar("11", 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextProgressBar("12", 100.0, "percent", classes="cpu"),
                        TextProgressBar("13", 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextProgressBar("14", 100.0, "percent", classes="cpu"),
                        TextProgressBar("15", 100.0, "percent", classes="cpu"),
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
