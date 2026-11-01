English | [繁體中文](README_zh-TW.md)

# check_nextcloud v1.0

Monitors a Nextcloud server. One plugin; each service picks one aspect with `-C`:

| `-C` | What it checks | Alerts when |
|---|---|---|
| `status` | `status.php` (no login) | not installed, maintenance mode, database upgrade pending → CRITICAL |
| `updates` | core and app updates | any update → WARNING, listing each app's new version |
| `storage` | free space of the data directory, users, files | free space ≤ `-w` / `-c` GB (default 50 / 20) |
| `shares` | shares, public links, public links without a password | links without a password ≥ `-w` / `-c` (no alert by default) |
| `users` | active users in 5 min / 1 h / 24 h / 7 days | graphs only |
| `php` | OPcache (enabled, full, hit rate, wasted, interned strings), APCu | OPcache disabled → CRITICAL; full, hit rate < `--hit-warn` (95%), wasted > `--wasted-warn` (10%), interned strings or APCu under 5% free → WARNING |
| `system` | load and memory of the Nextcloud host | 5-min load per CPU ≥ `-w` / `-c` (default 2 / 4); memory used ≥ `--mem-warn` / `--mem-crit` (90 / 95%) |
| `database` | database type, version, size | size ≥ `-w` / `-c` GB (no alert by default) |
| `setup` | the setup checks of Administration settings > Overview: background jobs (cron) last run, missing indices, security warnings, log errors ... | any error → CRITICAL, any warning → WARNING; cached for `--cache` minutes |

Everything except `status` reads the serverinfo API (`/ocs/v2.php/apps/serverinfo/api/v1/info`) and needs an admin account or a serverinfo token (`--nc-token`). `setup` always needs an admin account.

Replaces BornToBeRoot's `check_nextcloud.py`, whose `apps` check crashes on Nextcloud 28+ (serverinfo omits the app list unless asked for it) and which cannot see maintenance mode, core updates, free space, OPcache or the setup checks.

Installed on the LibreNMS server as `/usr/lib/nagios/plugins/check_nextcloud`.

## Requirements

- Python 3, standard library only
- The Nextcloud serverinfo app (enabled by default)
- An admin account, preferably dedicated to monitoring and used with an app password

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `-H` | — | Nextcloud host (LibreNMS passes it) |
| `-C` | — | What to check, see above |
| `-P` | 443 | Port |
| `--http` | — | Use http |
| `-k` | — | Do not verify the certificate |
| `-u` | — | User |
| `-a` | — | Auth file, one line `user:password` |
| `--password` | — | Password (shown in the LibreNMS UI and the process list; prefer `-a`) |
| `--nc-token` | — | serverinfo token (`occ config:app:set serverinfo token --value ...`), so checks other than `setup` need no admin password |
| `-t` | 30 | Timeout in seconds (at least 90 for `setup`) |
| `-w` / `-c` | see above | Depends on the check |
| `--mem-warn` / `--mem-crit` | 90 / 95 | `system` memory used % |
| `--hit-warn` | 95 | `php` minimum OPcache hit rate |
| `--wasted-warn` | 10 | `php` maximum OPcache wasted % |
| `--ignore` | — | Comma separated. `updates`: apps to skip; `setup`: skip items whose name or class name contains these words |
| `--ignore-core` | — | `updates` ignores core updates (when staying on a major version on purpose) |
| `--cache` | 60 | Minutes to cache the `setup` result (one run takes tens of seconds) |
| `-l` | `zh-tw` | Output language, `zh-tw` or `en` |

Password precedence: `--password`, the `-a` auth file, the `NEXTCLOUD_PASSWORD` environment variable.

## Install

```bash
install -o root -g root -m 0755 check_nextcloud /usr/lib/nagios/plugins/check_nextcloud
install -d -o root -g librenms -m 0750 /etc/librenms-checks
printf 'monitor:your-app-password\n' > /etc/librenms-checks/nextcloud.auth
chown librenms:librenms /etc/librenms-checks/nextcloud.auth
chmod 600 /etc/librenms-checks/nextcloud.auth
```

The `setup` cache lives in `/var/tmp/check_nextcloud/` (mode 700, created by the LibreNMS user).

## LibreNMS setup

Check Type `nextcloud`, one service per aspect:

```text
-a /etc/librenms-checks/nextcloud.auth -C status -l en
-a /etc/librenms-checks/nextcloud.auth -C updates -l en
-a /etc/librenms-checks/nextcloud.auth -C storage -w 50 -c 20 -l en
-a /etc/librenms-checks/nextcloud.auth -C shares -l en
-a /etc/librenms-checks/nextcloud.auth -C users -l en
-a /etc/librenms-checks/nextcloud.auth -C php -l en
-a /etc/librenms-checks/nextcloud.auth -C system -w 2 -c 4 -l en
-a /etc/librenms-checks/nextcloud.auth -C database -l en
-a /etc/librenms-checks/nextcloud.auth -C setup --cache 30 --ignore whiteboard,HighPerformanceBackend -l en
```

Add `-P 8443` when Nextcloud is not on port 443.

## Sample output

```text
NEXTCLOUD WARNING - Nextcloud 31.0.9.1 - core update to 32.0.1.2 available; 2 app updates available
calendar -> 5.5.6
mail -> 5.5.12
64 apps installed
| app_updates=2;1;;0 core_update=1;1;;0;1
```

```text
NEXTCLOUD OK - PHP 8.3.6 - OPcache hit 99.87% · used 30% · wasted 5.2%
APCu used 12% · hit 98.9%
memory_limit 1.0 GB · upload 10.0 GB
| opcache_hit=99.87%;95;;0;100 opcache_used=29.8%;;;0;100 opcache_wasted=5.22%;10;;0;100 strings_used=63.9%;95;;0;100 apcu_used=11.7%;95;;0;100 apcu_hit=98.85%;;;0;100
```

Unreachable host, HTTP errors and wrong credentials are CRITICAL; non-JSON responses and missing credentials are UNKNOWN.

## Design notes

- **Perfdata goes last**: LibreNMS joins all output and splits on the first `|`, so any `|` in the message (including text returned by Nextcloud) is replaced with `/`
- **Perfdata labels are fixed and at most 19 alphanumerics**: LibreNMS strips other characters, truncates to 19 and fixes the RRD's data sources on the first poll, so app names appear only in the message, never as labels
- **`setup` is cached**: Nextcloud takes tens of seconds to run the setup checks, too heavy for every 5-minute poll
- **No system proxy**: the plugin always connects to Nextcloud directly
- Moving from the old `check_nextcloud.py`: the perfdata labels differ, so create new services instead of changing the Check Type of the old ones

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later), see [LICENSE](../LICENSE).
