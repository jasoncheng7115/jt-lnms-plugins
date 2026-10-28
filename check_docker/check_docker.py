#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""check_docker - NCPA 外掛：透過 Docker Engine API（/var/run/docker.sock）檢查容器狀態。

Version: 1.2
Author: Jason Cheng (Jason Tools) <jason@jason.tools>
https://github.com/jasoncheng7115/jt-lnms-plugins

1.0 (2026/10/24)  first release as check_docker_containers.py
1.1 (2026/10/27)  renamed to check_docker.py, no functional change
1.2 (2026/10/28)  zh-tw wording: use 重新啟動

判斷規則：
  - 重新啟動政策為 always / unless-stopped / on-failure 卻沒在跑 → CRITICAL
  - 重新啟動政策為 no 且已停止 → 視為手動停用，略過（例如保留回復用的舊容器）
  - 健康檢查 unhealthy → CRITICAL；starting → WARNING
  - 正在 restarting，或重新啟動次數 ≥ --restart-warn → WARNING
  - --require 指定的容器不存在 → CRITICAL

用法：
  check_docker.py [--lang zh-tw|en] [--require a,b] [--exclude x,y] [--restart-warn N]
"""
import argparse
import http.client
import json
import socket
import sys

OK, WARNING, CRITICAL, UNKNOWN = 0, 1, 2, 3
STATE_NAME = {OK: "OK", WARNING: "WARNING", CRITICAL: "CRITICAL", UNKNOWN: "UNKNOWN"}

MSG = {
    "zh-tw": {
        "api_err": "無法連到 Docker API（{}）",
        "missing": "{} 不存在",
        "down": "{} 沒在執行（{}）",
        "unhealthy": "{} 健康檢查失敗",
        "starting": "{} 健康檢查啟動中",
        "restarting": "{} 正在反覆重新啟動",
        "restarts": "{} 已重新啟動 {} 次",
        "ok": "容器全部正常（執行中 {}）",
        "skipped": "略過已停用 {}",
        "running": "執行中 {}/{}",
    },
    "en": {
        "api_err": "cannot reach Docker API ({})",
        "missing": "{} does not exist",
        "down": "{} is not running ({})",
        "unhealthy": "{} is unhealthy",
        "starting": "{} health check starting",
        "restarting": "{} is restarting",
        "restarts": "{} restarted {} times",
        "ok": "all containers OK (running {})",
        "skipped": "skipped disabled {}",
        "running": "running {}/{}",
    },
}


class UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, path, timeout=10):
        super().__init__("localhost", timeout=timeout)
        self.path = path

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(self.path)


def api(path, sock):
    conn = UnixHTTPConnection(sock)
    conn.request("GET", path)
    resp = conn.getresponse()
    body = resp.read()
    if resp.status != 200:
        raise RuntimeError("HTTP {}".format(resp.status))
    return json.loads(body)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lang", default="zh-tw", choices=["zh-tw", "en"])
    p.add_argument("--require", default="", help="必須存在的容器，逗號分隔")
    p.add_argument("--exclude", default="", help="不檢查的容器，逗號分隔")
    p.add_argument("--restart-warn", type=int, default=5)
    p.add_argument("--socket", default="/var/run/docker.sock")
    a = p.parse_args()
    m = MSG[a.lang]
    require = {x.strip() for x in a.require.split(",") if x.strip()}
    exclude = {x.strip() for x in a.exclude.split(",") if x.strip()}

    try:
        summary = api("/containers/json?all=1", a.socket)
    except Exception as e:
        print("UNKNOWN - " + m["api_err"].format(e))
        return UNKNOWN

    status, problems, skipped = OK, [], []
    seen, running, checked = set(), 0, 0
    for c in summary:
        name = c["Names"][0].lstrip("/")
        seen.add(name)
        if name in exclude:
            continue
        try:
            info = api("/containers/{}/json".format(c["Id"]), a.socket)
        except Exception as e:
            print("UNKNOWN - " + m["api_err"].format(e))
            return UNKNOWN
        st = info["State"]
        policy = info["HostConfig"]["RestartPolicy"]["Name"] or "no"
        if not st["Running"] and policy == "no" and name not in require:
            skipped.append(name)
            continue
        checked += 1
        if st.get("Restarting"):
            problems.append((WARNING, m["restarting"].format(name)))
        elif not st["Running"]:
            problems.append((CRITICAL, m["down"].format(name, st["Status"])))
            continue
        running += 1
        health = (st.get("Health") or {}).get("Status")
        if health == "unhealthy":
            problems.append((CRITICAL, m["unhealthy"].format(name)))
        elif health == "starting":
            problems.append((WARNING, m["starting"].format(name)))
        if info.get("RestartCount", 0) >= a.restart_warn:
            problems.append((WARNING, m["restarts"].format(name, info["RestartCount"])))

    for name in sorted(require - seen):
        checked += 1
        problems.append((CRITICAL, m["missing"].format(name)))

    if problems:
        status = max(s for s, _ in problems)
        problems.sort(key=lambda x: -x[0])
        text = "; ".join(t for _, t in problems) + "; " + m["running"].format(running, checked)
    else:
        text = m["ok"].format(running)
    if skipped:
        text += "; " + m["skipped"].format(", ".join(sorted(skipped)))
    print("{} - {} | running={};;;0;{} problems={};;;0".format(
        STATE_NAME[status], text, running, checked, len(problems)))
    return status


if __name__ == "__main__":
    sys.exit(main())
