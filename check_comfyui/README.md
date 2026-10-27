English | [繁體中文](README_zh-TW.md)

# check_comfyui v1.0

Checks the status of ComfyUI (image generation). It only reads ComfyUI's `GET /system_stats`, `/queue` and `/history`, and checks whether the image API `/status` and the MCP endpoint are reachable. It does not generate images.

- ComfyUI version, GPU name, total VRAM and ComfyUI usage, system RAM
- Running/queued count, with an alert when the queue exceeds the threshold
- Duration of the last image, time since it finished, success or failure
- Whether the image API (8189) and MCP (8190) are working
- ComfyUI and Strata take turns using the same GPU: when ComfyUI is not running but Strata is using the GPU, the state is considered normal (OK); WARNING only when neither is running, or the image API/MCP is unreachable

Install it on the LibreNMS server as `/usr/lib/nagios/plugins/check_comfyui`, together with [check_strata](../check_strata/).

## Requirements

Python 3, standard library only.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `-H` | — | ComfyUI host (LibreNMS adds it automatically) |
| `-p` | 8188 | ComfyUI port |
| `--api-port` | 8189 | Image API port |
| `--mcp-port` | 8190 | MCP port |
| `-t` | 8 | Overall timeout in seconds |
| `-l` | `zh-tw` | Output language, `zh-tw` or `en` |
| `-w` / `-c` | 3 / 10 | Queue length that triggers WARNING / CRITICAL |

## LibreNMS setup

Set Check Type to `comfyui`:

```text
-t 8 -l zh-tw -w 3 -c 10
```

## Output format

The first line is the status summary, followed by multiple lines of detail; the last line is the perfdata, starting with `| `. Field names are fixed; values that cannot be retrieved are output as `U`:

```text
COMFYUI OK - 執行中 · ComfyUI 0.3.x
（明細數行）
| running=1.000;;;0 strata=0.000;;;0 apiup=1.000;;;0 ... queued=0.000;3;10;0 ...
```

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
