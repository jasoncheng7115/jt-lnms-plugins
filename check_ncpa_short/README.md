English | [繁體中文](README_zh-TW.md)

# check_ncpa_short v1.0

A wrapper plugin for `check_ncpa`: keeps only the first line of output (status + perfdata) and passes the exit code through unchanged.

## Why

The NCPA `logs` module (Windows event log) appends the details of every event after the `|` on the first line. LibreNMS parses everything after `|` as perfdata, so the event details cannot be written to RRD, InfluxDB reports `missing field key`, and the service's `service_ds` fills up with junk fields.

The long output of the `processes` module comes before the `|`, so it is not affected; keep using `ncpa` for it.

## Installation (LibreNMS server)

```bash
sudo install -m 755 check_ncpa_short /usr/lib/nagios/plugins/check_ncpa_short
```

This requires `/usr/lib/nagios/plugins/check_ncpa` to already exist.

## LibreNMS setup

Set Check Type to `ncpa_short`; Parameters are exactly the same as for `ncpa`:

```text
-t 'your-token' -M 'logs' -q 'name=Security,event_id=4625,logged_after=1h' -w 5 -c 20
```

For services already created with `ncpa` whose `service_ds` has been polluted, clear `service_ds` to `{}` after changing the Check Type; otherwise the old fields remain.

## Sample output

```text
OK: Security has 0 logs, Total Count has 0 logs (Time range - last 1 hour) | 'Security'=0;5;20; 'Total Count'=0;5;20;
```

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
