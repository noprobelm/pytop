from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Footer, Placeholder
from .widgets import ProcessTable, CPUBar
from textual.containers import Container, Horizontal, Vertical


class Main(Screen):
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

    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(
                Container(
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    classes="meters-column",
                ),
                Container(
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    Placeholder(),
                    classes="meters-column",
                ),
                id="meters",
            ),
            Container(ProcessTable(), Footer(), id="bot"),
        )
