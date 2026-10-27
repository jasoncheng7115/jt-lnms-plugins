English | [繁體中文](README_zh-TW.md)

# check_strata v1.0

Checks the API status of Strata (a local LLM inference service). It only reads `GET /v1/status` and `GET /metrics`; it does not load models or generate text.

- Whether a model is loaded, host-wide GPU/RAM usage, context limit
- Input/output tokens of the last request, generation and prompt-processing speed, duration, time since it finished, expert cache hit rate
- Alert when the queue length exceeds the threshold
- Strata and ComfyUI take turns using the same GPU: when the Strata API is unreachable, the plugin asks the image API on the same host (`--comfy-api-port`, default 8189) whether ComfyUI is using the GPU, and if so the state is considered normal (OK); WARNING only when neither is running

Install it on the LibreNMS server as `/usr/lib/nagios/plugins/check_strata`, together with [check_comfyui](../check_comfyui/).

## Requirements

Python 3, standard library only. Store the API key in a file readable only by the LibreNMS run-as account:

```bash
sudo install -m 640 -o root -g librenms /dev/null /etc/librenms/strata-api-key
sudo editor /etc/librenms/strata-api-key
```

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `-H` | — | Strata host (LibreNMS adds it automatically) |
| `-p` | 8080 | Strata API port |
| `--ssl` | — | Use https |
| `--api-key-file` | — | Required, path to the API key file |
| `--comfy-api-port` | 8189 | Port of the image API on the same host |
| `-t` | 8 | Overall timeout in seconds |
| `-l` | `zh-tw` | Output language, `zh-tw` or `en` |
| `-w` / `-c` | 2 / 5 | Queue length that triggers WARNING / CRITICAL |

## LibreNMS setup

Set Check Type to `strata`:

```text
-p 8080 -t 8 --api-key-file /etc/librenms/strata-api-key -l zh-tw -w 2 -c 5
```

## Output format

The first line is the status summary, followed by multiple lines of detail; the last line is the perfdata, starting with `| `. Perfdata field names are fixed (they do not change with language, state, or model); values that cannot be retrieved are output as `U`, not filled with 0:

```text
STRATA OK - 已載入 · example-model
（明細數行）
| loaded=1.000;;;0 gpuusedmib=... queued=0.000;2;5;0 livetps=U;;;0
```

An unreadable API key is UNKNOWN, an HTTP error from the API is CRITICAL, and malformed data is UNKNOWN.

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
