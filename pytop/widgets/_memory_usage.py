from ._text_progress_bar import TextProgressBar


class MemoryUsage(TextProgressBar):
    """A meter for displaying memory usage as a text progress meter"""

    def __init__(
        self,
        label: str,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        self.label = label
        super().__init__(label, "proportion", name=name, id=id, classes=classes)

    def watch_total(self, total):
        self.total_readout = self._convert_units(total)

    def compute__readout(self) -> str:
        if self.progress is None or self.total is None:
            return f"-/-"
        used = self._convert_units(self.progress)
        total = self._convert_units(self.total)
        return f"{used}/{total}"

    def _convert_units(self, data: int | float):
        units = {0: "K", 1: "K", 2: "M", 3: "G", 4: "T"}
        unit_key = 0
        while data > 1024:
            data = data / 1024
            unit_key += 1

        if unit_key == 0:
            return "0K"
        elif unit_key == 4:
            return f">{str(round(data, 2))}{units[unit_key]}"
        else:
            return f"{str(round(data, 1))}{units[unit_key]}"
