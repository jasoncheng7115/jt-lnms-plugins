English | [繁體中文](README_zh-TW.md)

# check_docker v1.1

NCPA plugin (Python 3): checks container state through the Docker Engine API (`/var/run/docker.sock`). It needs no `docker` command or extra packages, only the standard library.

## Rules

| Condition | Result |
|---|---|
| Restart policy is `always`, `unless-stopped` or `on-failure`, but the container is not running | CRITICAL |
| Restart policy is `no` and the container is stopped | Treated as disabled and skipped (for example, an old container kept for rollback) |
| Health check `unhealthy` | CRITICAL |
| Health check `starting` | WARNING |
| Restarting repeatedly, or restart count ≥ `--restart-warn` | WARNING |
| A container specified in `--require` does not exist | CRITICAL |
| Docker API unreachable | UNKNOWN |

## Installation

```bash
sudo install -m 755 check_docker.py /usr/local/ncpa/plugins/
sudo usermod -aG docker nagios
sudo systemctl restart ncpa     # 讓 nagios 的新群組生效
```

Note: **membership in the docker group is equivalent to root**; anyone who can access `docker.sock` can start privileged containers. Only do this in environments used for internal administration where only the monitoring server may connect to NCPA. In environments with stricter security requirements, use a Docker socket proxy that exposes only the read-only API (containers) and point `--socket` at it (the proxy must provide a Unix socket).

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `--lang` | `zh-tw` | Output language, `zh-tw` or `en` |
| `--require` | — | Containers that must exist, comma-separated; containers listed here are checked even if their policy is `no` |
| `--exclude` | — | Containers to skip, comma-separated |
| `--restart-warn` | 5 | Restart count that triggers WARNING |
| `--socket` | `/var/run/docker.sock` | Unix socket of the Docker API |

## LibreNMS setup

Set Check Type to `ncpa`:

```text
-t 'your-token' -M 'plugins/check_docker.py' -a "--require web,db,auth"
```

## Sample output

```text
OK - 容器全部正常（執行中 4）; 略過已停用 web-old | running=4;;;0;4 problems=0;;;0
CRITICAL - db 沒在執行（exited）; auth 不存在; 執行中 2/4 | running=2;;;0;4 problems=2;;;0
WARNING - web 已重啟 7 次; 執行中 4/4 | running=4;;;0;4 problems=1;;;0
```

## Limitations

- The container name is the first entry in `Names`
- The inspect API is called once per container; with many containers, watch the NCPA plugin timeout (default 59 seconds)

## Changelog

- **v1.1** (2026/10/27): renamed to `check_docker.py` (was `check_docker_containers.py`), no functional change. When upgrading, move the old file out of the plugin folder and change `-M` in the LibreNMS Parameters to the new name
- **v1.0** (2026/10/24)

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
