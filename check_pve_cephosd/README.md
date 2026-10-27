English | [繁體中文](README_zh-TW.md)

# check_pve_cephosd v1.1

Checks the state of the Ceph OSDs on a given Proxmox VE node: calls `GET /api2/json/nodes/<node>/ceph/osd` with an API Token and finds the OSDs under that node whose state is not `up`.

Originally published in https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons , maintained here since v1.1.

## Requirements

Python 3, `requests`, `urllib3` (Debian/Ubuntu: `apt install python3-requests`).

On the PVE side, create a read-only API Token, for example user `monitoring@pve`, Token ID `mon`, with the `PVEAuditor` role.

## Parameters

| Parameter | Description |
|---|---|
| `-H` | PVE host (LibreNMS adds it automatically; the port is fixed at 8006) |
| `--node_name` | Name of the node to check |
| `--user` | user@realm |
| `--token_id` / `--token_secret` | API Token |
| `-c` | Number of down OSDs that triggers CRITICAL; 1 or more but below the threshold is WARNING |
| `-d` | Debug: print the JSON of all OSDs on the node |

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_pve_cephosd` and set Check Type to `pve_cephosd`, one entry per node:

```text
--node_name pve01 --user monitoring@pve --token_id mon --token_secret 'your-token-secret' -c 1
```

## Sample output

```text
OK - All 4 OSDs are up | 'osd_down'=0;;1;0 'osd_total'=4;;;0
CRITICAL - 1 OSD(s) (osd.3) are down | 'osd_down'=1;;1;0 'osd_total'=4;;;0
OK - No OSDs found under node pve04 | 'osd_down'=0;;1;0 'osd_total'=0;;;0
```

## Notes

- With `-c 1` there is never a WARNING (1 OSD down is already CRITICAL)
- The PVE TLS certificate is not verified

## Changelog

- **v1.1** (2026/10/27): perfdata (down and total count); the OK message shows the OSD count and says so when the node has no OSDs; 30 s API timeout; example file name in the help text corrected
- **v1.0** (2024/03/01)

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
