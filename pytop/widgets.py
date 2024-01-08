from textual.widgets import DataTable
from textual.widgets._data_table import RowDoesNotExist
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
    generation = reactive(processes)

    def on_mount(self):
        for label in (
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
            "Command",
        ):
            self.add_column(label, key=label)
        for pid in self.processes:
            virt, res, shr = parser.parse_pmem(self.processes[pid]["memory_info"])
            cpu_times = parser.parse_pcputimes(self.processes[pid]["cpu_times"])
            cmdline = parser.parse_cmdline(self.processes[pid]["cmdline"])

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
                cmdline or self.processes[pid]["name"],
                key=str(pid),
            )

        self.set_interval(1.5, self.update_processes)

    def update_processes(self):
        self.processes = {
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
        updated = set()
        for pid in self.processes:
            row_key = str(pid)
            updated.add(row_key)
            try:
                self.get_row(str(row_key))
            except RowDoesNotExist:
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
                    key=row_key,
                )
            else:
                virt, res, shr = parser.parse_pmem(self.processes[pid]["memory_info"])
                cpu_times = parser.parse_pcputimes(self.processes[pid]["cpu_times"])
                cmdline = parser.parse_cmdline(self.processes[pid]["cmdline"])
                self.update_cell(row_key, "PRI", self.processes[pid]["nice"])
                self.update_cell(row_key, "NI", self.processes[pid]["nice"])
                self.update_cell(row_key, "VIRT", virt)
                self.update_cell(row_key, "RES", res)
                self.update_cell(row_key, "SHR", shr)
                self.update_cell(row_key, "S", self.processes[pid]["status"])
                self.update_cell(row_key, "CPU%", self.processes[pid]["cpu_percent"])
                self.update_cell(row_key, "MEM%", self.processes[pid]["memory_percent"])
                self.update_cell(
                    row_key,
                    "Command",
                    cmdline or self.processes[pid]["name"],
                )
        row_keys = set(k.value for k in self._row_locations)
        dropped_pids = updated.difference(row_keys)
        for p in dropped_pids:
            self.remove_row(p)
