English | [繁體中文](README_zh-TW.md)

# check_file_count v1.0

NCPA Windows plugin (pure CMD): CRITICAL if the folder contains files, OK if it does not. Intended for folders that should be emptied once processed, such as import queues or outgoing staging areas. It uses only `dir` and `find` and does not require PowerShell.

## Installation (monitored Windows host)

Copy it to `C:\Program Files\Nagios\NCPA\plugins\check_file_count.bat`.

The file is plain ASCII with CRLF line endings, so it works under any Windows code page.

## Parameters

The first argument is the folder to check. The count includes files in subfolders (`dir /s`) and does not count the folders themselves.

## LibreNMS setup

Set Check Type to `ncpa`:

```text
-t 'your-token' -M 'plugins/check_file_count.bat' -a 'D:\Inbox'
```

## Sample output

```text
OK - no files in "D:\Inbox"
CRITICAL - 2 files found in "D:\Inbox"
CRITICAL - directory "D:\Inbox" does not exist or cannot be accessed
```

## Limitations

- No perfdata and no threshold parameters; if you need min/max counts, use [check_files](../check_files/) instead

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
