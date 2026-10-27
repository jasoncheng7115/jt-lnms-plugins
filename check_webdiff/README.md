English | [繁體中文](README_zh-TW.md)

# check_webdiff v1.0

Detects tampering with a web page. Before comparing, it strips content that changes on every request (cache-busting parameters, nonces, CSRF tokens, timestamps, HTML comments). When a difference is found the page is fetched again right away: parts that differ between the two fetches are random and ignored, and only changes present in both fetches and different from the baseline raise an alert. External script, iframe and form hosts are tracked separately, and text that must or must not appear can be checked on every run.

Replaces [check_diff_webhtml](../check_diff_webhtml/). A complete rewrite; the options are not compatible.

## What it detects

| Item | Description | Default state |
|---|---|---|
| Content change | Differs from the baseline after dynamic content is removed | CRITICAL (`--on-change warn` for WARNING) |
| New external host | A third-party domain not seen before in a script, iframe, form action or embed/object | WARNING (`--new-hosts crit/off`) |
| Missing expected text | Text given with `-e` is not on the page | CRITICAL |
| Rejected text present | Text given with `-x` is on the page (case-insensitive) | CRITICAL |
| Redirect to another site | The final URL is on a different domain | Noted in the message |
| Fetch failure | Unreachable, timeout, or HTTP status not in `--status` | UNKNOWN (`--fetch-error crit` for CRITICAL) |

Content changes and new external hosts **keep alerting until accepted with `--accept`**; they do not turn OK again on the next run by themselves. Use `--once` to report a change only once.

## Removing dynamic content

**Built-in rules** (turn off with `--raw`) replace these with fixed placeholders before comparing:

| Rule | Target |
|---|---|
| comment | HTML comments (cache plugins, generation time), except IE conditional comments |
| buster | Values of cache-busting parameters: `v`, `ver`, `version`, `t`, `ts`, `time`, `timestamp`, `_`, `cb`, `cache`, `rand`, `random`, `r`, `nocache`, `nc`, `bust`, `rev`, `hash` |
| qnumber | Any URL parameter value with 6+ digits or 16+ hex characters |
| nonce | `nonce`, `data-nonce`, `data-csrf`, `data-token` attributes |
| csrf-meta | Meta tags such as `<meta name="csrf-token">` |
| token-input | Hidden fields: `_csrf*`, `_token`, `authenticity_token`, `_wpnonce`, `__VIEWSTATE*`, `__EVENTVALIDATION`, `__RequestVerificationToken`, `form_build_id`, `form_token`, `security`, `nonce` |
| js-nonce | `"nonce":"…"`, `"csrfToken":"…"` and similar in JavaScript objects |
| datetime / time / epoch | `2026-10-27 21:22:47`, ISO 8601, `21:22:47`, 10- or 13-digit Unix time |
| uuid | UUIDs |

`integrity="sha384-…"` is not removed: it only changes when the script itself is replaced.

**Fetching twice** (turn off with `--no-confirm`): when the content differs from the baseline, the page is fetched again at once, and lines that differ between the two fetches are treated as random. The baseline is also built from two fetches. An unchanged static site is fetched only once per check.

**Custom rules**: `-I 'regex'`, repeatable, replaces matches before comparing.

## Comparison modes (`-m`)

| Mode | Compares | Suitable for |
|---|---|---|
| `full` (default) | The whole HTML, one tag or text run per line | Most sites |
| `text` | Visible text only (no script, style) | Sites whose layout changes but whose text should not |
| `key` | `<title>`, scripts (src + integrity, or "inline"), iframes, forms, stylesheets, meta refresh, base, embed/object | Sites with news lists or carousels that change all the time: catches structural tampering only |

## Requirements

Python 3.8 or later, standard library only.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `-u`, `--url` | - | Full URL; takes precedence over `-H` |
| `-H`, `--host` | - | Host name (LibreNMS passes the device host or the service's IP field) |
| `-p`, `--path` | - | Path appended to `-H`, e.g. `/index.html` |
| `--http` | - | Use http with `-H` (default https) |
| `-k`, `--insecure` | - | Do not verify the TLS certificate |
| `--no-follow` | - | Do not follow redirects |
| `--status` | `200` | Accepted HTTP status codes, comma-separated |
| `-t`, `--timeout` | 15 | Timeout in seconds |
| `-m`, `--mode` | `full` | `full`, `text`, `key` |
| `-I`, `--ignore` | - | Regex removed before comparing; repeatable |
| `--raw` | - | Turn off the built-in rules |
| `--no-confirm` | - | Do not fetch a second time when a difference is found |
| `-d`, `--max-diff` | 0 | A change of up to this many bytes (removed + added) is OK |
| `-e`, `--expect` | - | Text that must appear (case-sensitive); repeatable |
| `-x`, `--reject` | - | Text that must not appear (case-insensitive); repeatable |
| `--new-hosts` | `warn` | New external host: `warn`, `crit`, `off` |
| `--on-change` | `crit` | State for a content change: `crit`, `warn` |
| `--fetch-error` | `unknown` | State for a failed fetch: `unknown`, `crit` |
| `--once` | - | Report a change once, then make the new content the baseline |
| `-A`, `--accept` | - | Accept the current content as the new baseline (run by hand) |
| `--state-dir` | `/var/tmp/check_webdiff` | Where baselines are kept |
| `--keep` | 5 | Number of recent changes whose before/after versions are kept (0 = none) |
| `-v`, `--verbose` | - | Show the changed lines and what was ignored |
| `--lang` | `en` | Output language, `en` or `zh-tw` |
| `-V` | - | Version |

## LibreNMS setup

Place it at `/usr/lib/nagios/plugins/check_webdiff` and set Check Type to `webdiff`. LibreNMS passes `-H` (the service's IP field or the device host name):

```text
(empty)                                    https://<device host>/
--http                                     http://<device host>/
-p /index.html -e "Example Corp" -x "hacked by"
-m key --new-hosts crit
-u https://www.example.com/shop/ -I 'id="visitor-count">[0-9]+'
```

Once a change has been confirmed as a normal update, run the check **as the LibreNMS user** with **the same parameters as the service** plus `--accept`:

```bash
sudo -u librenms /usr/lib/nagios/plugins/check_webdiff -H www.example.com --accept
```

Running it as root also works; the files keep the owner of their folder. Baselines are stored per URL + mode + `-I` rules, so the parameters must match the service to update the same baseline.

The before and after versions of each change are kept in `/var/tmp/check_webdiff/<id>/history/` (`-before.html`, `-after.html`). While a change keeps alerting it is saved only once, and the files can be compared with `diff` afterwards.

## Sample output

```text
OK - Content unchanged (https://www.example.com) | size=225668B;;;0 time=0.636s;;;0 hosts=0;;;0 changed=0B;;0;0
CRITICAL - Content changed: 1 block(s), 16 bytes; not accepted yet, baseline from 2026-10-27 21:27:00 (accept with --accept) (https://www.example.com) | ...
CRITICAL - New external host(s): cdn.evil.example.net; Content changed: 1 block(s), 57 bytes; ... | ... hosts=1;;;0 ...
CRITICAL - Expected text not found: Example Corp; Rejected text found: hacked by; ... | ...
UNKNOWN - Fetch failed: HTTP 404 (expected 200) (https://www.example.com/missing)
```

With `-v`, the first line is the result, followed by the ignore statistics and the changed lines (`-` baseline, `+` current), with the perfdata on the last line:

```text
CRITICAL - Content changed: 1 block(s), 16 bytes; ...
ignored: buster 3, comment 1, csrf-meta 1, epoch 1, js-nonce 1, nonce 1, token-input 1, random between two fetches 1
- Welcome
+ Defaced
| size=734B;;;0 ...
```

## Limitations

- JavaScript is not executed: content rendered by front-end frameworks is not seen, although `key` mode still catches a replaced script
- Content that changes hourly or daily without a fixed format (a quote of the day, for example) is not caught by fetching twice; use `-I` or `-m key`
- Third-party hosts are judged by domain (`www.example.com` and `cdn.example.com` count as the same site); the full Public Suffix List is not used
- Pages are limited to 5 MB

## Changelog

- **v1.0** (2026/10/27): first release, replaces `check_diff_webhtml`

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
