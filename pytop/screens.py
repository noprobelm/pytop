from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Footer, Placeholder, ProgressBar
from .widgets import ProcessTable
from .meter import TextMeter
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
        cpu_meters = self.query(".cpu").results(TextMeter)
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
                        TextMeter("0", 25.0, 100.0, "percent", classes="cpu"),
                        TextMeter("1", 25.0, 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextMeter("2", 25.0, 100.0, "percent", classes="cpu"),
                        TextMeter("3", 25.0, 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextMeter("4", 25.0, 100.0, "percent", classes="cpu"),
                        TextMeter("5", 25.0, 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextMeter("6", 25.0, 100.0, "percent", classes="cpu"),
                        TextMeter("7", 25.0, 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    TextMeter("Mem", 25.0, 100.0, "proportion", classes="memory"),
                    Placeholder("Swap", classes="meter"),
                    id="col1",
                ),
                Vertical(
                    Horizontal(
                        TextMeter("8", 25.0, 100.0, "percent", classes="cpu"),
                        TextMeter("9", 25.0, 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextMeter("10", 25.0, 100.0, "percent", classes="cpu"),
                        TextMeter("11", 25.0, 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextMeter("12", 25.0, 100.0, "percent", classes="cpu"),
                        TextMeter("13", 25.0, 100.0, "percent", classes="cpu"),
                        classes="meter-row",
                    ),
                    Horizontal(
                        TextMeter("14", 25.0, 100.0, "percent", classes="cpu"),
                        TextMeter("15", 25.0, 100.0, "percent", classes="cpu"),
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
