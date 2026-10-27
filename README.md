English | [繁體中文](README_zh-TW.md)

# jt-lnms-plugins

A collection of self-developed LibreNMS / Nagios-compatible monitoring plugins. Each plugin has its own folder named after the plugin, containing the plugin itself and a `README.md` (purpose, install location, parameters, sample output, LibreNMS setup).

## Plugins

| Plugin | Version | Runs on | Platform | Purpose |
|---|---|---|---|---|
| [check_ncpa_short](check_ncpa_short/) | v1.0 | LibreNMS server | bash | Wraps `check_ncpa` and keeps only the first line, so the long output of NCPA `logs` is not parsed as perfdata |
| [check_files](check_files/) | v1.0 | Monitored host (NCPA) | Windows PowerShell | File/folder existence, min/max count, age of the newest file in hours |
| [check_file_count](check_file_count/) | v1.0 | Monitored host (NCPA) | Windows CMD | CRITICAL if the folder contains any files (a pending queue that should be empty) |
| [check_ucs_replication](check_ucs_replication/) | v1.0 | Monitored host (NCPA) | UCS, Python 3 | UCS LDAP replication progress + Samba AD DRS replication failure count |
| [check_docker_containers](check_docker_containers/) | v1.0 | Monitored host (NCPA) | Linux, Python 3 | Container state based on restart policy and health check |
| [check_graylog_if](check_graylog_if/) | v1.2 | LibreNMS server | bash | Graylog indexing failures in the last 5 minutes |
| [check_graylog_journal](check_graylog_journal/) | v1.1 | LibreNMS server | bash | Graylog Journal utilization |
| [check_pmg_queue](check_pmg_queue/) | v1.0 | LibreNMS server | Python 3 | Postfix queue count on Proxmox Mail Gateway |
| [check_pve_cephosd](check_pve_cephosd/) | v1.1 | LibreNMS server | Python 3 | Ceph OSDs that are down on a Proxmox VE node |
| [check_udp_nmap](check_udp_nmap/) | v1.1 | LibreNMS server | bash + nmap | Whether a UDP port is listening |
| [check_diff_webhtml](check_diff_webhtml/) | v1.1 | LibreNMS server | bash | Whether web page content has changed |
| [check_ollama](check_ollama/) | v1.0 | LibreNMS server | Python 3 | Ollama loaded models, VRAM, unload countdown |
| [check_strata](check_strata/) | v1.0 | LibreNMS server | Python 3 | Strata LLM inference API status, queue length, performance of the last request |
| [check_comfyui](check_comfyui/) | v1.0 | LibreNMS server | Python 3 | ComfyUI status, VRAM, queue length, last image |
| [check_pyhs](check_pyhs/) | v1.1 | LibreNMS server | Python 3 | Per-outlet power usage of a TP-Link Kasa 6-outlet smart power strip |

check_graylog_*, check_pmg_queue, check_pve_cephosd, check_udp_nmap and check_diff_webhtml were originally hosted at https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons .

Related articles:

- Monitoring Windows 11 with LibreNMS and NCPA: https://blog.jason.tools/2026/10/librenms-ncpa-windows.html
- Monitoring Linux hosts with LibreNMS and NCPA: https://blog.jason.tools/2026/10/librenms-ncpa-linux.html

## Conventions

- **Exit codes** follow the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN
- **One line of output**: `STATUS - message | perfdata`. LibreNMS parses everything after `|` as perfdata and stores it in RRD/InfluxDB, so only the `'label'=value;warn;crit;min;max` format may follow `|`. Do not append descriptive text after it
- **NCPA plugin directory**: Linux `/usr/local/ncpa/plugins/`, Windows `C:\Program Files\Nagios\NCPA\plugins\`. NCPA decides how to run a plugin by its extension (`.py` with the system `python3`, `.ps1` with `powershell -ExecutionPolicy Bypass -File`). The default plugin timeout is 59 seconds (`plugin_timeout`)
- **NCPA run-as user**: `nagios` on Linux (`uid/gid` under `[general]` in `ncpa.cfg`), LocalSystem on Windows. For commands that need root, allow only that one command in sudoers and call it with `sudo -n` inside the plugin. Do not use `run_with_sudo` to give the whole plugin root
- **On the LibreNMS side**, to call an NCPA plugin: set Check Type to `ncpa` and Parameters to `-t 'your-token' -M 'plugins/<file name>' -a '<plugin arguments>'`. Do not include `-H` (LibreNMS adds it automatically)
- **Plugins on the LibreNMS server** go in `/usr/lib/nagios/plugins/`. The file name must start with `check_`; the Check Type is shown as the name without the prefix
- Plugins with localized output provide `--lang zh-tw|en`, defaulting to zh-tw

## Adding a plugin

1. Create a folder with the same name as the plugin (without extension) and put the plugin in it
2. Write `README.md` (English, default) and `README_zh-TW.md` (Traditional Chinese): the title includes the version number, and the content covers purpose, requirements, install location and permissions, parameters, sample output, LibreNMS Parameters example, known issues, author, and license
3. Always use fictitious data in examples (`example.com`, `192.168.1.x`, `your-token`). Do not include real host names, IPs, container names, or domains
4. Add `SPDX-License-Identifier: AGPL-3.0-or-later` at the top of the plugin
5. Update the plugin list (including version) on this page and in the Chinese version

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](LICENSE) for the full text.
