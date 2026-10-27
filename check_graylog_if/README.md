English | [繁體中文](README_zh-TW.md)

# check_graylog_if v1.2

Checks whether Graylog has had any index failures in the last 5 minutes by calling `GET /api/system/indexer/failures/count?since=<5 minutes ago>`.

Originally published in https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons , maintained here since v1.2.

## Requirements

`curl` on the LibreNMS server (or Nagios server).

## Parameters

| Parameter | Description |
|---|---|
| `-U` | Graylog user name |
| `-P` | Password |
| `-p` | Port (usually 9000) |
| `-H` | Graylog IP or FQDN (LibreNMS adds it automatically) |
| `-S` | Use https (certificate not verified, curl `-k`) |

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_graylog_if` and set Check Type to `graylog_if`:

```text
-U "monitor" -P 'your-password' -p 9000 -S
```

## Sample output

```text
OK: No index failure.|'index_failure'=0;;1;0
CRITICAL: Index failure occurred (3 records in the last 5 minutes)|'index_failure'=3;;1;0
UNKNOWN: Cannot get index failure count from https://graylog.example.com:9000
```

## Notes

- The password is written in the LibreNMS Parameters; use a Graylog account with read-only permissions
- The Graylog TLS certificate is not verified (curl `-k`)

## Changelog

- **v1.2** (2026/10/27): any failure count above 0 is CRITICAL (previously only exactly 1); UNKNOWN when the API is unreachable or the reply is invalid; perfdata thresholds and minimum; 30 s curl timeout
- **v1.1** (2023/12/15)

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
