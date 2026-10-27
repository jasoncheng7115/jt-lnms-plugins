English | [繁體中文](README_zh-TW.md)

# check_pyhs v1.1

Checks the real-time power usage of each outlet on a TP-Link Kasa 6-outlet smart power strip (models such as the HS300 with a power meter on every outlet), with thresholds for power, voltage, and current. It reads the device state with the `pyhs100` command and parses the `== Current State ==` section.

Install it on the LibreNMS server as `/usr/lib/nagios/plugins/check_pyhs`.

## Requirements

- Python 3
- The `pyhs100` command (`pip install pyHS100`; the installed version is currently 0.3.5.2)

Note: pyHS100 is no longer maintained. Its successor is `python-kasa` (command `kasa`), which has a different output format; switching packages requires changing this plugin as well.

## Parameters

| Parameter | Description |
|---|---|
| `-H` | IP of the power strip (LibreNMS adds it automatically) |
| `--plug` | Outlet number 1-6; if omitted, all outlets are listed |
| `-w` / `-c` | Thresholds, comma-separated. `metric:value` applies to all outlets, `plug<number>:metric:value` applies only to that outlet; alerts when reached (≥) |
| `--show-device-name` | Add the device name to the output |

Metric names are the fields returned by the device, for example `power_mw` (milliwatts), `voltage_mv` (millivolts), `current_ma` (milliamps), `total_wh` (cumulative watt-hours).

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_pyhs` and set Check Type to `pyhs`, one entry per outlet:

```text
--plug 2 -c power_mw:230000
```

The example above is CRITICAL when outlet 2 reaches 230 W.

## Sample output

```text
OK - Plug 2 (NAS) |voltage_mv=110512 current_ma=812 power_mw=85230;;230000.0 total_wh=15320
CRITICAL - Plug 2 (NAS) - Alert on: power_mw=231200 |voltage_mv=110230 current_ma=2105 power_mw=231200;;230000.0 total_wh=15322
CRITICAL - Cannot connect to 192.168.1.30
```

Without `--plug`, the first line is a summary, each outlet gets one status line, and the perfdata is printed once on the last line with a `plug<number>_` prefix:

```text
OK - Status for all plugs:
Plug 1 (Router): OK
Plug 2 (NAS): OK
...
| plug1_voltage_mv=110512 plug1_current_ma=72 plug1_power_mw=4043 plug1_total_wh=463 plug2_voltage_mv=110288 ...
```

## Changelog

- **v1.1** (2026/10/27): in all-outlet mode the perfdata is printed once on the last line (`plug<number>_` prefix), so LibreNMS parses it correctly; errors are detected by the `pyhs100` exit code, so warnings on stderr no longer cause a false CRITICAL; outlet names are read in list order, including outlets without a custom name; 30 s timeout; `--plug` range checked
- **v1.0** (2025/02/08)

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
