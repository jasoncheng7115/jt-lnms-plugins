English | [繁體中文](README_zh-TW.md)

> Superseded by the rewritten [check_webdiff](../check_webdiff/); use it for new deployments. This plugin is kept as is.

# check_diff_webhtml v1.1

Detects whether web page content has changed: each run fetches the URL once and compares the character count with the content fetched the previous time; if they differ, the result is CRITICAL. Useful for spotting changes such as a replaced home page or injected content.

Originally published in https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons , maintained here since v1.1.

## Requirements

`curl`, `bc`, `diff`, `md5sum`.

## Parameters

| Parameter | Description |
|---|---|
| `-H` | URL without the protocol, e.g. `www.example.com/index.html` (LibreNMS adds the device host name automatically) |
| `-S` | Use https |
| `-k` | Do not verify the certificate |
| `-d` | Allowed difference in character count (growth or shrinkage); a difference within this range is still OK |
| `-P` | Persistent: after a change, keep the old baseline and keep reporting CRITICAL until it is accepted with `-A` |
| `-A` | Accept the current content as the new baseline (with `-P`, run by hand) |

The baseline is stored in `/var/tmp/check_diff_webhtml/<URL md5>.previous` and survives a reboot; a v1.0 baseline in `/tmp` is moved there on the first run.

Without `-P`, every run makes the current content the next baseline, so a change is reported as CRITICAL for one run only; pair it with alert notifications. To keep the alert up until someone has looked at the change, add `-P`, then accept the change by running the check once with `-A` as the LibreNMS user:

```bash
sudo -u librenms /usr/lib/nagios/plugins/check_diff_webhtml -H www.example.com -S -A
```

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_diff_webhtml` and set Check Type to `diff_webhtml`:

```text
-S
```

## Sample output

```text
OK: First time execution, no previous content to compare with (File size: 12.31KB)
OK: Content is unchanged (File size: 12.31KB)
CRITICAL: Content has changed. Difference in character count: 42 (Difference text is "3c3< <title>"...) (File size: 12.35KB, Previous file size: 12.31KB)
```

## Limitations

- Only the character count is compared; a change that keeps the same length is not detected
- Dynamic pages (timestamps, random values, CSRF tokens) differ on every fetch and are not suitable

## Changelog

- **v1.1** (2026/10/27): baseline kept in `/var/tmp` (old files are moved automatically); `-d` compares the absolute difference, so shrinking pages also alert; new `-P` and `-A`; HTTP errors (4xx, 5xx) count as a failed fetch; 30 s curl timeout; diff excerpt truncation fixed
- **v1.0** (2023/12/26)

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
