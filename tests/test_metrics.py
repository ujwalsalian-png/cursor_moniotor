import json
import socket

import metrics


class _Memory:
    total = 1000
    used = 400
    available = 600
    percent = 40.0
    cached = 50


class _Counters:
    def __init__(self, sent, received):
        self.bytes_sent = sent
        self.bytes_recv = received


class _Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


class _Connection:
    def __init__(self, sock_type, status, port, pid, remote=()):
        self.type = sock_type
        self.status = status
        self.laddr = _Address("127.0.0.1", port)
        self.raddr = remote
        self.pid = pid


class _Process:
    def name(self):
        return "sshd"

    def cmdline(self):
        raise AssertionError("command line must not be read")


def test_host_shape(monkeypatch):
    monkeypatch.setattr(metrics.platform, "node", lambda: "demo-host")
    monkeypatch.setattr(metrics.platform, "platform", lambda: "Linux-demo")

    host = metrics.collect_host()

    assert set(host) == {"hostname", "operating_system"}
    assert isinstance(host["hostname"], str) and host["hostname"]
    assert isinstance(host["operating_system"], str) and host["operating_system"]


def test_cpu_uses_per_core_numbers(monkeypatch):
    def cpu_percent(interval=None, percpu=False):
        assert percpu is True
        return [10.0, 30.0]

    monkeypatch.setattr(metrics.psutil, "cpu_percent", cpu_percent)

    cpu = metrics.collect_cpu()

    assert cpu["overall"] == 20.0
    assert cpu["per_core"] == [10.0, 30.0]


def test_memory_returns_four_figures(monkeypatch):
    monkeypatch.setattr(metrics.psutil, "virtual_memory", lambda: _Memory())

    memory = metrics.collect_memory()

    assert memory == {"total": 1000, "used": 400, "available": 600, "percent": 40.0}


def test_network_returns_interface_counters(monkeypatch):
    monkeypatch.setattr(
        metrics.psutil,
        "net_io_counters",
        lambda pernic=True: {"eth0": _Counters(12, 34)},
    )

    network = metrics.collect_network()

    assert network == [{"interface": "eth0", "bytes_sent": 12, "bytes_recv": 34}]


def test_ports_use_process_name_only(monkeypatch):
    monkeypatch.setattr(metrics.psutil, "CONN_LISTEN", "LISTEN")
    monkeypatch.setattr(
        metrics.psutil,
        "net_connections",
        lambda kind="inet": [
            _Connection(socket.SOCK_STREAM, "LISTEN", 22, 7),
            _Connection(socket.SOCK_DGRAM, "NONE", 53, None),
            _Connection(socket.SOCK_STREAM, "ESTABLISHED", 4000, 7),
        ],
    )
    monkeypatch.setattr(metrics.psutil, "Process", lambda pid: _Process())

    ports = metrics.collect_ports()

    assert ports == [
        {"port": 22, "address": "127.0.0.1", "protocol": "TCP", "process": "sshd"},
        {"port": 53, "address": "127.0.0.1", "protocol": "UDP", "process": None},
    ]


def test_failed_section_is_unavailable_without_the_error_text(monkeypatch):
    def explode():
        raise RuntimeError("secret /etc/shadow")

    monkeypatch.setattr(metrics, "collect_memory", explode)

    payload = metrics.collect_all()

    assert payload["memory"] is None
    assert payload["host"] is not None
    assert "shadow" not in json.dumps(payload)
