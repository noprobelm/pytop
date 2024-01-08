from textual.widgets import DataTable
from . import parser
import psutil
from textual.reactive import reactive


class ProcessTable(DataTable):
    processes = {
        p.pid: p.info
        for p in psutil.process_iter(
            [
                "pid",
                "name",
                "username",
                "nice",
                "memory_info",
                "memory_percent",
                "status",
                "cpu_percent",
                "cpu_times",
                "cmdline",
            ]
        )
    }
    generation = reactive(0)

    def on_mount(self):
        self.add_columns(
            "PID",
            "USER",
            "PRI",
            "NI",
            "VIRT",
            "RES",
            "SHR",
            "S",
            "CPU%",
            "MEM%",
            "TIME+",
            "COMMAND",
        )
        for pid in self.processes:
            virt, res, shr = parser.parse_pmem(self.processes[pid]["memory_info"])
            cpu_times = parser.parse_pcputimes(self.processes[pid]["cpu_times"])
            self.add_row(
                pid,
                self.processes[pid]["username"],
                self.processes[pid]["nice"],
                self.processes[pid]["nice"],
                virt,
                res,
                shr,
                self.processes[pid]["status"],
                self.processes[pid]["cpu_percent"],
                self.processes[pid]["memory_percent"],
                cpu_times,
                parser.parse_cmdline(self.processes[pid]["cmdline"])
                or self.processes[pid]["name"],
            )
