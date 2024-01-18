from ._text_progress_bar import TextProgressBar


class CPUUsage(TextProgressBar):
    """A meter for displaying CPU usage (per core) as a text progress meter"""

    def __init__(
        self,
        core: int,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self.core = core
        self.label = str(self.core)
        super().__init__(str(core), "percent", name=name, id=id, classes=classes)
