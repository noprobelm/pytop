from textual.containers import Container, Horizontal, Vertical, Grid
from textual.app import ComposeResult


class MeterColumn(Vertical):
    pass


class Meters:
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield MeterColumn()
            yield MeterColumn()
