English | [繁體中文](README_zh-TW.md)

# check_ucs_replication v1.0

NCPA plugin (Python 3): checks the replication status of a Univention Corporate Server (UCS) domain controller.

- **UCS LDAP replication**: compares the Primary's notifier ID with the ID the local listener has processed. Lagging briefly during large LDAP changes is normal, so the state file `/var/tmp/check_ucs_replication.state` records when the listener got stuck, and the plugin alerts only when it is **lagging and has made no progress** for longer than the threshold; a non-empty `failed.ldif` is CRITICAL immediately
- **Samba AD DRS replication**: reads repsFrom from `samba-tool drs showrepl --json` and checks the consecutive failure count of each partition (naming context)

## Requirements

- UCS (in use on UCS 5.2)
- The system `python3`, standard library only

## Installation

```bash
sudo install -m 755 check_ucs_replication.py /usr/local/ncpa/plugins/
sudo install -m 440 sudoers-ncpa-ucs-replication /etc/sudoers.d/ncpa-ucs-replication
sudo visudo -c
```

`samba-tool drs showrepl` requires root, while NCPA runs plugins as `nagios`. The sudoers file allows only the single command `samba-tool drs showrepl --json` (written with its full arguments, so different arguments are not allowed), and the plugin automatically calls it with `sudo -n` when it is not running as root. Do not use NCPA's `run_with_sudo`, which would run the whole plugin as root.

On nodes without Samba AD, add `--no-drs`; the sudoers file is then not needed.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `--lang` | `zh-tw` | Output language, `zh-tw` or `en` |
| `-w` / `-c` | 10 / 30 | Minutes of LDAP lag with no progress that trigger WARNING / CRITICAL |
| `--drs-warn` | 1 | Consecutive DRS failures on any partition that trigger WARNING |
| `--drs-crit` | 3 | Consecutive DRS failures on any partition that trigger CRITICAL |
| `--no-drs` | — | Do not check Samba DRS |

## LibreNMS setup

Set Check Type to `ncpa`:

```text
-t 'your-token' -M 'plugins/check_ucs_replication.py' -a "--lang zh-tw"
```

## Sample output

```text
OK - LDAP 複寫同步（1234/1234）; Samba DRS 正常（5 個分區） | ldap_lag=0;;;0 drs_failures=0;1;3;0
WARNING - LDAP 落後 52 筆（1182/1234），已 12 分鐘沒有進度; Samba DRS 正常（5 個分區） | ldap_lag=52;;;0 drs_failures=0;1;3;0
CRITICAL - LDAP 複寫同步（1234/1234）; Samba DRS DomainDnsZones 從 DC01 連續失敗 3 次（...） | ldap_lag=0;;;0 drs_failures=3;1;3;0
```

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
