English | [繁體中文](README_zh-TW.md)

# check_ollama v1.0

Checks the models Ollama currently has loaded in memory by calling `GET /api/ps` (it also reads `/api/version` to show the version; a failure there does not affect the result). Ollama can keep several models resident at once, so all of them are listed, each with its VRAM usage, share on the GPU, parameter count and quantization, context length, and time until unload.

Install it on the LibreNMS server as `/usr/lib/nagios/plugins/check_ollama`.

## Requirements

Python 3, standard library only.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `-H` | — | Ollama host (LibreNMS adds it automatically) |
| `-p` | 11434 | Port |
| `--ssl` | — | Use https |
| `--api-key` | — | Use when a reverse proxy in front requires a Bearer token |
| `-t` | 10 | Timeout in seconds |
| `-l` | `zh-tw` | Output language, `zh-tw` or `en` |
| `-w` / `-c` | — | Total VRAM of all models (GB) that triggers WARNING / CRITICAL |
| `--min-models` | — | WARNING if fewer than N models are loaded; used to detect models that should stay resident but were unloaded |
| `--expiring` | — | WARNING if any model will be unloaded within N seconds |

## LibreNMS setup

Set Check Type to `ollama`:

```text
-w 80 -c 100
```

## Sample output

```text
OLLAMA OK - 2 個模型 · VRAM 21.40 GB

qwen3:32b
19.80 GB · 32.8B · Q4_K_M
ctx 40K · 4m12s 後卸載

nomic-embed-text:latest
1.60 GB · 137M · F16
ctx 8K · 常駐不卸載

ollama 0.12.3
| models=2;;;0 vram=21.400GB;80.0;100.0;0 size=21.400GB;;;0
```

An unreachable Ollama or an HTTP error response is CRITICAL; a response that is not JSON is UNKNOWN.

## Design notes

- **Perfdata is on the last line**: LibreNMS joins all output and splits it at the first `|`, treating everything after `|` as perfdata, so the details must come first
- **Perfdata field names are fixed** (`models`, `vram`, `size`) instead of using model names: LibreNMS fixes the RRD fields on the first poll, so they would no longer match once the loaded models change; it also strips non-alphanumeric characters and truncates to 19 characters, so `qwen3-vl:2b` becomes `qwen3vl2b`
- The LibreNMS message column is narrow and collapses consecutive spaces into one, so every line is short and spaces are not used for alignment

## Author

- Jason Cheng (Jason Tools)
- jason@jason.tools
- Blog: https://blog.jason.tools
- GitHub: https://github.com/jasoncheng7115

## License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](../LICENSE) for the full text.
