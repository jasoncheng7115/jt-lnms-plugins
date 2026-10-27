English | [繁體中文](README_zh-TW.md)

# check_files v1.0

NCPA Windows plugin (PowerShell): checks whether a file or folder exists, and can also check the number of matching files and the age of the newest file in hours. NCPA has no built-in file module, so use this plugin for checks on backup files, export files, and the like.

## Installation (monitored Windows host)

Copy it to `C:\Program Files\Nagios\NCPA\plugins\check_files.ps1`. NCPA runs `.ps1` files with `powershell -ExecutionPolicy Bypass -File`, so there is no need to change the system execution policy or restart NCPA.

## Parameters

| Parameter | Description |
|---|---|
| `-Path` | Required, file or folder |
| `-Filter` | Wildcard used for counting, default `*`, for example `*.bak` |
| `-MinCount` | CRITICAL if the count is below this number |
| `-MaxCount` | CRITICAL if the count is above this number |
| `-MaxAgeHours` | CRITICAL if the newest file is older than this many hours |
| `-Recurse` | Include subfolders when counting |

With only `-Path`, the plugin only checks for existence. A path that does not exist is CRITICAL; an execution error is UNKNOWN.

## LibreNMS setup

Set Check Type to `ncpa`:

```text
-t 'your-token' -M 'plugins/check_files.ps1' -a '-Path D:\Backup -Filter *.bak -MinCount 3'
-t 'your-token' -M 'plugins/check_files.ps1' -a '-Path D:\Backup -Filter *.bak -MaxAgeHours 24'
```

## Sample output

```text
OK: 3 file(s) matching *.bak in D:\Backup | 'count'=3;;;
CRITICAL: 3 file(s) matching *.bak in D:\Backup, newest file db-1.bak is 30.2 hours old | 'count'=3;;;
CRITICAL: D:\Backup not found
```

## Limitations

- File age is based on `LastWriteTime`
- Count and age violations always return CRITICAL; there is no WARNING level

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
