from rich.text import Text
from textual.widgets import Static
from textual.reactive import Reactive


class Tasks(Static):
    """A meter for displaying number of tasks running"""

    COMPONENT_CLASSES = {
        "tasks--label",
        "tasks--num-tasks",
        "tasks--num-threads",
        "tasks--num-kthreads",
        "tasks--num-running",
    }

    DEFAULT_CSS = """
    Tasks .tasks--label {
        color: $primary-lighten-3;
    }

    Tasks .tasks--num-tasks {
        color: $success;
    }
    Tasks .tasks--num-threads {
        color: $text;
    }
    Tasks .tasks--num-kthreads {
        color: $text-muted;
    }
    Tasks .tasks--num-running {
        color: $text-disabled;
    }


    """

    num_tasks: Reactive[int] = Reactive(0)
    num_threads: Reactive[int] = Reactive(0)
    num_kthreads: Reactive[int] = Reactive(0)
    num_running: Reactive[int] = Reactive(0)

    def render(self) -> Text:
        label_style = self.get_component_rich_style("tasks--label")
        num_tasks_style = self.get_component_rich_style("tasks--num-tasks")
        num_threads_style = self.get_component_rich_style("tasks--num-threads")
        num_kthreads_style = self.get_component_rich_style("tasks--num-kthreads")
        num_running_style = self.get_component_rich_style("tasks--num-running")

        return Text.assemble(
            ("Tasks: ", label_style),
            (f"{self.num_tasks}, ", num_tasks_style),
            (f"{self.num_threads} thr, ", num_threads_style),
            (f"{self.num_kthreads} kthr, ", num_kthreads_style),
            (f"{self.num_running} running", num_running_style),
        )
