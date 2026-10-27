English | [繁體中文](README_zh-TW.md)

# check_graylog_journal v1.1

Checks the Journal utilization of a Graylog node: calls `GET /api/system/journal`, computes the percentage as `journal_size / journal_size_limit`, and returns CRITICAL when it reaches the threshold. A growing Journal means messages are arriving faster than they are written to OpenSearch.

Originally published in https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons , maintained here since v1.1.

## Requirements

`curl`, `bc`.

## Parameters

| Parameter | Description |
|---|---|
| `-U` / `-P` | Graylog user name, password |
| `-p` | Port (usually 9000) |
| `-H` | Graylog IP or FQDN (LibreNMS adds it automatically) |
| `-c` | Utilization threshold (%); CRITICAL when reached |
| `-S` | Use https (certificate not verified) |

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_graylog_journal` and set Check Type to `graylog_journal`:

```text
-U "monitor" -P 'your-password' -p 9000 -S -c 10
```

## Sample output

```text
OK: Journal usage is normal. 0.20% (10.48MB/5.00GB)|'journal_usage'=0.20;;10;0;100
CRITICAL: Journal usage exceeds 10% ! (612.00MB/5.00GB)|'journal_usage'=11.95;;10;0;100
UNKNOWN: Cannot get journal size from https://graylog.example.com:9000
```

## Changelog

- **v1.1** (2026/10/27): `-c` is required (UNKNOWN when missing; `bc` used to fail); UNKNOWN when the API is unreachable or returns no journal size; the percentage is multiplied before dividing so small values are no longer truncated to 0; perfdata thresholds and 0-100 range; 30 s curl timeout
- **v1.0** (2023/12/22)

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
