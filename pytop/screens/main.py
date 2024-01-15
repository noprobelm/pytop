from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer
from ..containers.meters import Meters
from textual.reactive import Reactive
from ..data import data
from ..widgets import CPUUsage, ProcessTable, Tasks


class Main(Screen):
    processes: Reactive[data.Processes] = Reactive(data.Processes())

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

    def compose(self) -> ComposeResult:
        yield Vertical(
            Meters(),
            Vertical(ProcessTable(), Footer(), id="bot"),
        )
