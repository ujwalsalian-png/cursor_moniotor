const REFRESH_MS = 5000;

function formatBytes(value) {
  let size = Number(value);
  const units = ["B", "KB", "MB", "GB", "TB"];
  for (let index = 0; index < units.length; index += 1) {
    const unit = units[index];
    if (size < 1024 || unit === "TB") {
      if (unit === "B") {
        return `${Math.trunc(size)} B`;
      }
      return `${size.toFixed(1)} ${unit}`;
    }
    size /= 1024;
  }
  return `${value} B`;
}

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) {
    node.textContent = value;
  }
}

function fillHost(host) {
  if (!host) {
    setText("host-name", "Unavailable");
    setText("host-os", "Unavailable");
    return;
  }
  setText("host-name", host.hostname);
  setText("host-os", host.operating_system);
}

function fillCpu(cpu) {
  const list = document.getElementById("cpu-cores");
  list.replaceChildren();
  if (!cpu) {
    setText("cpu-overall", "Unavailable");
    const item = document.createElement("li");
    item.textContent = "Unavailable";
    list.append(item);
    return;
  }
  setText("cpu-overall", `${Number(cpu.overall).toFixed(1)}%`);
  cpu.per_core.forEach((value, index) => {
    const item = document.createElement("li");
    item.textContent = `Core ${index + 1}: ${Number(value).toFixed(1)}%`;
    list.append(item);
  });
}

function fillMemory(memory) {
  if (!memory) {
    ["memory-total", "memory-used", "memory-available", "memory-percent"].forEach((id) => {
      setText(id, "Unavailable");
    });
    return;
  }
  setText("memory-total", formatBytes(memory.total));
  setText("memory-used", formatBytes(memory.used));
  setText("memory-available", formatBytes(memory.available));
  setText("memory-percent", `${Number(memory.percent).toFixed(1)}%`);
}

function fillTable(bodyId, columns, rows, emptyText) {
  const body = document.getElementById(bodyId);
  body.replaceChildren();
  const values = rows === null ? null : rows;
  if (values === null || values.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = columns;
    cell.textContent = values === null ? "Unavailable" : emptyText;
    row.append(cell);
    body.append(row);
    return;
  }
  values.forEach((item) => {
    const row = document.createElement("tr");
    item.forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.append(cell);
    });
    body.append(row);
  });
}

function fillNetwork(network) {
  const rows = network && network.map((row) => [
    row.interface,
    formatBytes(row.bytes_sent),
    formatBytes(row.bytes_recv),
  ]);
  fillTable("network-body", 3, network === null ? null : rows, "None");
}

function fillPorts(ports) {
  const rows = ports && ports.map((row) => [
    String(row.port),
    row.address,
    row.protocol,
    row.process || "—",
  ]);
  fillTable("ports-body", 4, ports === null ? null : rows, "None");
}

async function refreshMetrics() {
  const response = await fetch("/api/metrics", { headers: { Accept: "application/json" } });
  if (response.status === 401) {
    window.location.assign("/login");
    return;
  }
  if (!response.ok) {
    return;
  }
  const payload = await response.json();
  fillHost(payload.host);
  fillCpu(payload.cpu);
  fillMemory(payload.memory);
  fillNetwork(payload.network);
  fillPorts(payload.ports);
}

document.getElementById("refresh").addEventListener("click", () => {
  refreshMetrics();
});
window.setInterval(refreshMetrics, REFRESH_MS);
