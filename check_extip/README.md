English | [繁體中文](README_zh-TW.md)

# check_extip v1.0

Checks whether the external (WAN) IP address has changed. It asks several public "what is my IP" services in parallel and compares the majority answer with the expected address, so one misbehaving service does not raise a false alert.

Replaces `check_ext_ip` from it-scripts (v1.5, itself a modified version of Justin Reherman's plugin). It is a complete rewrite; `-H`, `-S`, `-t`, `-l`, `-v`, `-V` and `-h` are compatible, so an existing service only needs its Check Type changed.

## Differences from check_ext_ip

| | check_ext_ip v1.5 | check_extip |
|---|---|---|
| Decision | Picks 3 random services and trusts **the first one that answers** | Asks in parallel and needs **at least 2 matching answers**; asks one more round if needed |
| Services disagree | Not noticed | Every answer is listed; a tie is UNKNOWN |
| Querying | One by one; worst case is "services × timeout" | In parallel; stops when every service fails instead of waiting for each timeout |
| Expected address `-H` | One IPv4 address | IP, comma-separated list, CIDR, or **host name** (checks DDNS) |
| Backup WAN | None | `-W`: WARNING instead of CRITICAL when running on the backup line |
| IPv6 | None | `-6` |
| Address validation | Regular expression; `999.999.999.999` passes | Python `ipaddress` |
| Non-public answer | Compared as usual | UNKNOWN when a service returns a private or reserved address |
| Custom services | None | `-U` adds your own lookup URL |
| Perfdata | `match` | `match`, `providers`, `answered`, `agree`, `time` |
| Dead services | `ipsimple` no longer answers | `ipsimple` removed; `seeip` and `dnsomatic` added (each tested in 2026/10) |

## Requirements

Python 3.8 or later, standard library only. The LibreNMS server needs outbound HTTPS.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `-H` | - | Required. Expected external address: an IP, a comma-separated list, a CIDR, or a host name (its A/AAAA records are used). LibreNMS passes the service's IP address field |
| `-W` | - | Backup WAN IP(s) or CIDR; WARNING when the external IP is one of them |
| `-S` | 3 random | Services to ask, comma-separated; all of them are asked |
| `-U` | - | Extra lookup URL (https, plain-text reply); repeatable |
| `-n` | 3 | Services in the first round when `-S` is not given |
| `-q` | 2 | Matching answers required. Defaults to 1 when `-S` lists one or two services (the v1.5 behaviour) |
| `-t` | 5 | Timeout per service in seconds |
| `-6` | - | Check the IPv6 address |
| `-v` | - | List every answer and its response time |
| `--lang` | `en` | Output language, `en` or `zh-tw` |
| `-l` | - | List the built-in services |
| `-V` / `-h` | - | Version / help |

## Built-in services

`amazonaws`, `dnsomatic`, `icanhazip`, `ident`, `ifconfigco`, `ifconfigme`, `ipecho`, `ipify`, `ipinfo`, `ipme`, `seeip`, `wtfismyip`. All are free, need no API key and return the bare address as plain text; only HTTPS with certificate verification is used. `-l` shows their IPv4/IPv6 URLs.

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_extip`. Add a service with Check Type `extip`, put the expected external IP in the IP address field, and leave Parameters empty or use:

```text
(empty)
-W 198.51.100.20
-H 203.0.113.8/29
-H home.example.com
--lang zh-tw
```

`-H home.example.com` compares with what the DDNS name currently resolves to, which catches a DDNS client that stopped updating.

## Sample output

```text
OK - External IP 203.0.113.10 is as expected (3/3 providers agree: ipify, icanhazip, amazonaws) | match=1;;;0;1 providers=3;;;0 answered=3;;;0 agree=3;;;0 time=0.332s;;;0
CRITICAL - External IP changed to 198.51.100.7, expected 203.0.113.10 (3/3 providers agree: ident, ipme, seeip) | match=0;;;0;1 ...
WARNING - External IP 198.51.100.20 is a backup WAN address (failover active?) (3/3 providers agree: ...) | match=0;;;0;1 ...
CRITICAL - External IP 198.51.100.7 does not match home.example.com (203.0.113.10), DDNS not updated? (3/3 providers agree: ...) | match=0;;;0;1 ...
UNKNOWN - All providers failed (tried: ipify, ident, seeip). Could not determine external IP | match=0;;;0;1 ...
OK - 對外 IP 203.0.113.10 與預期相同 (3/3 個服務一致: ipify, icanhazip, amazonaws) | match=1;;;0;1 ...
```

With `-v`, the first line is the result, followed by one line per service, and the perfdata on the last line.

## Notes

- Each check sends about 3 HTTPS requests. At LibreNMS's default 5-minute interval this stays well within the services' limits
- Behind CGNAT the services see the carrier's address, not the one on the router's WAN interface

## Changelog

- **v1.0** (2026/10/27): first release, replaces `check_ext_ip` v1.5

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
