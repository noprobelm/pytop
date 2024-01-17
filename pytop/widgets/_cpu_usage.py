from ._text_progress_bar import TextProgressBar
from textual.reactive import Reactive


class CPUUsage(TextProgressBar):
    """A meter for displaying CPU usage (per core) as a text progress meter"""

    progress: Reactive[float] = Reactive(0.0)

    DEFAULT_CSS = """
    CPUUsage {
        height: 1;
        width: 1fr;
    }
    """

    def __init__(
        self,
        label: str,
        core: int,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self.label = label
        self.core = core
        super().__init__(label, "percent", name=name, id=id, classes=classes)
