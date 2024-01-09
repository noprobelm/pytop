from textual.widgets import DataTable
from textual.reactive import reactive

from .processes import (
    get_processes,
    parse_pmem,
    parse_pcputimes,
    parse_cmdline,
    parse_status,
)


class ProcessTable(DataTable):
    processes = reactive(get_processes())

    current_sort = ("CPU%", True)

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
            virt, res, shr = parse_pmem(self.processes[pid]["memory_info"])
            cpu_times = parse_pcputimes(self.processes[pid]["cpu_times"])
            cmdline = parse_cmdline(self.processes[pid]["cmdline"])
            status = parse_status(self.processes[pid]["status"])
            self.add_row(
                int(pid),
                self.processes[pid]["username"],
                self.processes[pid]["nice"],
                self.processes[pid]["nice"],
                virt,
                res,
                shr,
                status,
                self.processes[pid]["cpu_percent"],
                self.processes[pid]["memory_percent"],
                cpu_times,
                cmdline or self.processes[pid]["name"],
                key=pid,
            )

        self.set_interval(1.5, self.update_processes)

        self.sort(self.current_sort[0], reverse=self.current_sort[1])

    def update_processes(self):
        self.processes = get_processes()

        queued = set(self.processes.keys())
        rows = self.rows.copy()
        for row_key in rows:
            pid = row_key.value
            assert pid is not None

            if pid not in self.processes.keys():
                self.remove_row(pid)
                continue
            process_info = self.processes[pid]
            virt, res, shr = parse_pmem(process_info["memory_info"])
            cpu_times = parse_pcputimes(process_info["cpu_times"])
            cmdline = parse_cmdline(process_info["cmdline"])
            status = parse_status(self.processes[pid]["status"])

            self.update_cell(pid, "PRI", process_info["nice"])
            self.update_cell(pid, "NI", process_info["nice"])
            self.update_cell(pid, "VIRT", virt)
            self.update_cell(pid, "RES", res)
            self.update_cell(pid, "SHR", shr)
            self.update_cell(pid, "S", status)
            self.update_cell(pid, "CPU%", process_info["cpu_percent"])
            self.update_cell(pid, "MEM%", process_info["memory_percent"])
            self.update_cell(
                pid,
                "Command",
                cmdline or process_info["name"],
            )
            queued.remove(pid)

        for pid in queued:
            virt, res, shr = parse_pmem(self.processes[pid]["memory_info"])
            cpu_times = parse_pcputimes(self.processes[pid]["cpu_times"])
            cmdline = parse_cmdline(self.processes[pid]["cmdline"])
            status = parse_status(self.processes[pid]["status"])
            self.add_row(
                int(pid),
                self.processes[pid]["username"],
                self.processes[pid]["nice"],
                self.processes[pid]["nice"],
                virt,
                res,
                shr,
                status,
                self.processes[pid]["cpu_percent"],
                self.processes[pid]["memory_percent"],
                cpu_times,
                cmdline or self.processes[pid]["name"],
                key=pid,
            )

    def on_data_table_header_selected(self, selected: DataTable.HeaderSelected):
        if self.current_sort[0] == selected.column_key:
            self.current_sort = (selected.column_key, not self.current_sort[1])
        else:
            self.current_sort = (selected.column_key, True)
        self.sort(self.current_sort[0], reverse=self.current_sort[1])
