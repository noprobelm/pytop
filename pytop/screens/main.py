from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Footer
from ..widgets.process_table import ProcessTable
from ..widgets.meters import LoadAverage, CPUUsage, RAMUsage, SwapUsage
from textual.containers import Horizontal, Vertical
from ..widgets import Uptime, LoadAverage, Tasks
from .. import data


class Main(Screen):
    processes = data.Processes()
    cpu = data.CPU()

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
        self.processes.query_processes()
        top = self.query_one(ProcessTable)
        top.processes = self.processes.processes

        tasks = self.query_one(Tasks)
        tasks.num_tasks = self.processes.num_tasks
        tasks.num_threads = self.processes.num_threads
        tasks.num_kthreads = self.processes.num_kthreads
        tasks.num_running = self.processes.num_running

        self.cpu.update()
        cpu_meters = self.query(".cpu").results(CPUUsage)
        for i, meter in enumerate(cpu_meters):
            meter.progress = self.cpu.cores[i]

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
                    RAMUsage("Mem", classes="virt-memory"),
                    SwapUsage("Swp", classes="swap-memory"),
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
                    Tasks(classes="meter"),
                    LoadAverage(classes="meter"),
                    Uptime(classes="meter"),
                    id="col2",
                ),
                id="top",
            ),
            Vertical(ProcessTable(), Footer(), id="bot"),
        )
