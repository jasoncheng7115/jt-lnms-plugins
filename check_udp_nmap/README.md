English | [繁體中文](README_zh-TW.md)

# check_udp_nmap v1.1

Uses `nmap -sU` to check whether a given UDP port is listening, for example SNMP 161, Syslog 514, NTP 123. UDP has no connection handshake, so ordinary TCP checks do not work.

Originally published in https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons , maintained here since v1.1.

## Requirements

- `nmap` (`/usr/bin/nmap`)
- UDP scanning requires root, so the LibreNMS run-as account must be able to run `sudo nmap`:

```text
librenms ALL=(root) NOPASSWD: /usr/bin/nmap
```

Note: **allowing nmap through sudo is equivalent to granting root** (nmap can run arbitrary Lua via `--script`). Only do this in environments where the LibreNMS server itself is under control.

## Parameters

| Parameter | Description |
|---|---|
| `-H` | Target IP (LibreNMS adds it automatically) |
| `-p` | UDP port |
| `-s` | Strict: only `open` is OK, `open\|filtered` is CRITICAL |
| `-t` | nmap host timeout in seconds, default 30 |

How nmap classifies a UDP port:

| nmap state | Meaning | Default | `-s` |
|---|---|---|---|
| `open` | The service replied | OK | OK |
| `open\|filtered` | No reply. Syslog, GELF and most custom listeners never answer an empty probe, so this is their normal state | OK | CRITICAL |
| `closed` | ICMP port unreachable came back: nothing is listening | CRITICAL | CRITICAL |
| `filtered` | Another ICMP error came back | CRITICAL | CRITICAL |

`open|filtered` can also mean that a firewall drops ICMP, so the default mode only confirms that the port is not explicitly closed. For services that do reply (SNMP, DNS, NTP), use `-s`.

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_udp_nmap` and set Check Type to `udp_nmap`:

```text
-p 161
```

## Sample output

```text
OK: 161/udp is listening.
OK: 514/udp is listening or filtered (nmap: open/filtered, no reply).
CRITICAL: 514/udp is not listening (closed).
CRITICAL: 161/udp did not reply (nmap: open/filtered).
UNKNOWN: No result for 161/udp on 192.168.1.30 (host down or timed out).
```

## Changelog

- **v1.1** (2026/10/27): reports the real nmap state; `open|filtered` is no longer matched as `open` by accident; new `-s` strict mode; UNKNOWN on missing options or nmap failure; `sudo -n` so it never waits for a password; host timeout `-t`; `-P0` replaced by the current `-Pn`
- **v1.0**

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
