from textual.widget import Widget
from textual.widgets import RadioSet, RadioButton, SelectionList
from textual.containers import Horizontal, Vertical

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

HEADER_LAYOUT_OPTIONS = (
    ("2 columns - 50/50 (default)", 0),
    ("2 columns - 33/67", 1),
    ("2 columns - 67/33", 2),
    ("3 columns - 33/33/33", 3),
    ("3 columns - 25/25/50", 4),
    ("3 columns - 25/50/25", 5),
    ("3 columns - 50/25/25", 6),
    ("3 columns - 40/30/30", 7),
    ("3 columns - 30/40/30", 8),
    ("3 columns - 30/30/40", 9),
    ("3 columns - 40/20/40", 10),
    ("4 columns - 25/25/25/25", 11),
)


class Setup(Widget):
    def on_mount(self):
        self.query_one("#categories", RadioSet).border_title = "Categories"
        self.query_one("#display-options").border_title = "Display Options"
        self.query_one("#global-options").border_title = "Global Options"

    def compose(self):
        with Horizontal():
            with RadioSet(id="categories"):
                yield RadioButton("Display options", value=True)
                yield RadioButton("Header layout")
                yield RadioButton("Meters")
                yield RadioButton("Screens")
                yield RadioButton("Colors")

            with Vertical():
                yield SelectionList(*SCREEN_DISPLAY_OPTIONS, id="display-options")
                yield SelectionList(*SCREEN_GLOBAL_OPTIONS, id="global-options")

    def on_show(self):
        self.query_one(RadioSet).focus()
