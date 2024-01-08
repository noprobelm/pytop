from psutil._pslinux import pmem, pcputimes
from typing import List


def _format_bytes(data: int):
    units = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T"}
    unit_key = 0
    exp = 2**10
    while data > exp:
        data = data // exp
        unit_key += 1

    if unit_key == 0:
        return "0K"
    return f"{str(round(data, 2)).zfill(2)}{units[unit_key]}"


def parse_pmem(pmem):
    virt = _format_bytes(pmem.vms)
    res = _format_bytes(pmem.rss)
    shr = _format_bytes(pmem.shared)

    return virt, res, shr


def parse_pcputimes(pcputimes):
    user, system = pcputimes.user, pcputimes.system
    return sum((user, system))


def parse_cmdline(cmdline: List[str]) -> str:
    return " ".join(cmdline)
