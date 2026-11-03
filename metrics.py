import platform
import socket

import psutil


def collect_host():
    return {
        "hostname": platform.node(),
        "operating_system": platform.platform(),
    }


def collect_cpu():
    per_core = [float(value) for value in psutil.cpu_percent(interval=None, percpu=True)]
    overall = round(sum(per_core) / len(per_core), 1) if per_core else 0.0
    return {"overall": overall, "per_core": per_core}


def collect_memory():
    memory = psutil.virtual_memory()
    return {
        "total": int(memory.total),
        "used": int(memory.used),
        "available": int(memory.available),
        "percent": float(memory.percent),
    }


def collect_network():
    counters = psutil.net_io_counters(pernic=True)
    return [
        {
            "interface": name,
            "bytes_sent": int(counters[name].bytes_sent),
            "bytes_recv": int(counters[name].bytes_recv),
        }
        for name in sorted(counters)
    ]


def collect_ports():
    rows = []
    for conn in psutil.net_connections(kind="inet"):
        protocol = _protocol(conn.type)
        if protocol is None or not conn.laddr:
            continue
        if protocol == "TCP" and conn.status != psutil.CONN_LISTEN:
            continue
        if protocol == "UDP" and conn.raddr:
            continue
        rows.append(
            {
                "port": int(conn.laddr.port),
                "address": conn.laddr.ip,
                "protocol": protocol,
                "process": _process_name(conn.pid),
            }
        )
    rows.sort(key=lambda row: (row["port"], row["protocol"], row["address"]))
    return rows


def collect_all():
    collectors = {
        "host": collect_host,
        "cpu": collect_cpu,
        "memory": collect_memory,
        "network": collect_network,
        "ports": collect_ports,
    }
    payload = {}
    for name, collector in collectors.items():
        try:
            payload[name] = collector()
        except Exception:
            payload[name] = None
    return payload


def format_bytes(value):
    size = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            if unit == "B":
                return f"{int(size)} B"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{int(value)} B"


def _protocol(sock_type):
    if sock_type == socket.SOCK_STREAM:
        return "TCP"
    if sock_type == socket.SOCK_DGRAM:
        return "UDP"
    return None


try:
    psutil.cpu_percent(interval=None, percpu=True)
except Exception:
    pass


def _process_name(pid):
    if not pid:
        return None
    try:
        return psutil.Process(pid).name()
    except (psutil.Error, OSError):
        return None
