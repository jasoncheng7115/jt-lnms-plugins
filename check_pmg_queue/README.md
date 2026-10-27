English | [繁體中文](README_zh-TW.md)

# check_pmg_queue v1.0

Checks the Postfix queue count on Proxmox Mail Gateway (PMG): it first obtains a ticket with the user name and password (`POST /api2/json/access/ticket`), then reads `GET /api2/json/nodes/<node>/postfix/queue/<queue>`.

Source: https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons (v1.0, 2024/02/24)

## Requirements

Python 3, `requests` (Debian/Ubuntu: `apt install python3-requests`).

## Parameters

| Parameter | Description |
|---|---|
| `-H` | PMG FQDN (LibreNMS adds it automatically) |
| `-P` | Port (usually 8006) |
| `-u` | user@realm, for example `monitor@pmg` |
| `-p` | Password |
| `-n` | Node name |
| `-q` | Queue name: `active`, `deferred`, `hold`, `incoming` |
| `-c` | CRITICAL when the count "exceeds" this value |

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_pmg_queue` and set Check Type to `pmg_queue`:

```text
-P 8006 -u "monitor@pmg" -p 'your-password' -n "pmg01" -q "deferred" -c 20
```

## Sample output

```text
OK - Queue count is 3 | 'queue_count'=3;20;20;
CRITICAL - Queue count is 25, exceeds critical threshold of 20 | 'queue_count'=25;20;20;0;
```

## Known issues

- The threshold is "greater than", not "greater than or equal to"; there is no WARNING level
- The PMG TLS certificate is not verified
- A read-only PMG account with the Audit role is recommended

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
