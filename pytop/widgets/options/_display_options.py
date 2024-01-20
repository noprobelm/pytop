from textual.app import ComposeResult
from textual.widgets import SelectionList
from textual.containers import Vertical


class DisplayOptions(Vertical):
    SCREEN_DISPLAY_OPTIONS = (
        ("Process Table - Tree View", 0),
        (" - Tree view is always sorted by PID", 1),
        (" - Tree view is collapsed by default", 2),
    )

    SCREEN_GLOBAL_OPTIONS = (
        ("Show tabs for screens", 0),
        ("Shadow other uses' processes", 1),
        ("Hide kernel threads", 2),
        ("Hide userland process threads", 3),
        ("Hide processes running in containers", 4),
        ("Display threads in different color", 5),
        ("Show custom thread names", 6),
        ("Show program path", 7),
        ('Highlight program "basename"', 8),
        ("Highlight out-dated/removed programs (red) / libraries (yellow)", 9),
        ("Shadow distribution path prefixes", 10),
        ("Merge exe, comm, and cmdline in Command", 11),
        (" - Try to find comm in cmdline (when Command is merged)", 12),
        (" - Try to strip exe from cmdline (when Command is merged)", 13),
        ("Highlight large numbers in memory counters", 14),
        ("Leave a margin around header", 15),
        ("Detailed CPU time (System/IO-Wait/Hard-IRQ/Soft-IRQ/Steal/Guest)", 16),
        ("Count CPUs from 1 instead of 0", 17),
        ("Update process names on every refresh", 18),
        ("Add guest time in CPU meter percentage", 19),
        ("Also show CPU percentage numerically", 20),
        ("Also show CPU frequency", 21),
        ("Also show CPU temperature (requires libsensors)", 22),
        (" - Show temperature in Fahrenheit", 23),
        ("Enable the mouse", 24),
        ("Update interval (in seconds)", 25),
        ("Highlight new and old processes", 26),
        (" - Highlight time (in seconds)", 27),
        (
            "Hide main function bar (0 - off, 1 - on ESC until next input, 2 - permanently)",
            28,
        ),
    )

    def on_mount(self):
        self.query_one("#display-options").border_title = "Display Options"
        self.query_one("#global-options").border_title = "Global Options"

    def compose(self) -> ComposeResult:
        yield SelectionList(*self.SCREEN_DISPLAY_OPTIONS, id="display-options")
        yield SelectionList(*self.SCREEN_GLOBAL_OPTIONS, id="global-options")
