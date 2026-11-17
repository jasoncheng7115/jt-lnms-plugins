English | [繁體中文](README_zh-TW.md)

# check_jt_waf_mgr v1.2

Checks whether the WAF managed by [jt-waf-mgr](https://github.com/jasoncheng7115/jt-waf-mgr) (nginx + ModSecurity) is working. It only reads `GET /api/v1/health` with an API token whose only scope is `status:read`; it changes nothing.

- WAF paused for troubleshooting (jt-waf-mgr 0.4.82 or later: WARNING while it lasts)
- nginx master process running, ModSecurity in blocking mode (`DetectionOnly` is WARNING, engine off is CRITICAL)
- Managed rule files changed outside jt-waf-mgr, the last apply failed, the configuration was changed outside in the last 24 hours
- Event collector still reading the ModSecurity audit log, IP block list loaded by nginx, program integrity, audit chain, the last two event analyses failed
- Events and blocks in the last hour / 24 hours, active IP blocks, open alerts and changes awaiting approval as perfdata

The overall state is the worst check jt-waf-mgr reports; `--ignore` leaves named checks out of it. Requires jt-waf-mgr 0.4.80 or later.

Install it on the LibreNMS server as `/usr/lib/nagios/plugins/check_jt_waf_mgr`.

## Requirements

Python 3, standard library only.

In jt-waf-mgr, Admin → API tokens: create a token with only the `status:read` scope, allowed source address = the LibreNMS server (for example `192.168.1.x/32`). Store it in a file readable only by the LibreNMS run-as account:

```bash
sudo install -m 640 -o root -g librenms /dev/null /etc/librenms/jt-waf-mgr-token
sudo editor /etc/librenms/jt-waf-mgr-token
```

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `-H` | — | Host or address of the jt-waf-mgr server (LibreNMS adds it automatically) |
| `-p` | 443 | Port |
| `--vhost` | value of `-H` | Name of the management site, sent as the Host header and TLS SNI (for example `waf.example.com`) |
| `--no-ssl` | — | Plain http (for example straight to the service at `127.0.0.1:8095` on the same host) |
| `-k` | — | Do not verify the TLS certificate |
| `--ca-file` | — | CA bundle for a certificate from a private CA |
| `--token-file` | — | Required, path to the API token file |
| `--ignore` | — | Comma-separated check names left out of the overall state (for example `analyst,ip_blocks`) |
| `-t` | 10 | Timeout in seconds |
| `-l` | `zh-tw` | Output language, `zh-tw` or `en` |

Check names: `nginx`, `modsecurity`, `waf_pause`, `managed_rules`, `last_apply`, `collector`, `ip_blocks`, `program_integrity`, `audit_chain`, `config_changes`, `analyst`.

## LibreNMS setup

Add the service to the device of the WAF host and set Check Type to `jt_waf_mgr`:

```text
-p 443 --vhost waf.example.com --token-file /etc/librenms/jt-waf-mgr-token -l zh-tw
```

## Output format

The first line is the status summary (the worst problems, or "working" with the version), followed by one line per check and the counts; the last line is the perfdata, starting with `| `. Perfdata field names are fixed (they do not change with language or state); values that cannot be retrieved are output as `U`, not filled with 0:

```text
JT-WAF-MGR OK - 運作正常 · jt-waf-mgr 0.4.80
（明細數行）
| problems=0;;;0 events1h=12;;;0 blocked1h=9;;;0 blocked24h=240;;;0 lasteventagesec=85;;;0 collectorlagsec=1;;;0 ipblocks=3;;;0 openalerts=1;;;0 pendingchanges=0;;;0
```

jt-waf-mgr unreachable or an HTTP error is CRITICAL; an unreadable token file, a token refused (401/403) or malformed data is UNKNOWN.

## Changelog

- **v1.2** (2026/11/17): new `waf_pause` check (WAF paused for troubleshooting, jt-waf-mgr 0.4.82 or later); ModSecurity reported as blocking through rules when the engine is set to detection only; zh-tw text for the last apply result
- **v1.0** (2026/11/17)

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
