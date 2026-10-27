[English](README.md) | 繁體中文

# check_comfyui v1.1

檢查 ComfyUI（影像產生）的狀態。只讀 ComfyUI 的 `GET /system_stats`、`/queue`、`/history`，以及圖片 API 的 `/status` 與 MCP 端點是否可連線，不會產生圖片。

- ComfyUI 版本、GPU 名稱、整張 VRAM 與 ComfyUI 佔用、系統 RAM
- 使用的模型：主模型、LoRA（含強度）、文字編碼器、VAE。有工作在執行時取正在產圖的工作流程，閒置時取上一張圖的；ComfyUI 沒有 API 可以查詢目前常駐在 VRAM 的模型，所以畫面會標明是哪一種
- 執行中/排隊數，排隊超過門檻告警
- 上一張圖的耗時、距今時間、成功或失敗
- 圖片 API（8189）、MCP（8190）是否正常
- ComfyUI 與 Strata 輪流使用同一張 GPU：ComfyUI 沒在執行但 Strata 在用 GPU 時視為正常（OK）；兩者都沒在執行、或圖片 API/MCP 連不到才 WARNING

安裝在 LibreNMS 主機的 `/usr/lib/nagios/plugins/check_comfyui`，搭配 [check_strata](../check_strata/)。

## 需求

Python 3，只用標準函式庫。

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `-H` | — | ComfyUI 主機（LibreNMS 會自動帶） |
| `-p` | 8188 | ComfyUI 連接埠 |
| `--api-port` | 8189 | 圖片 API 連接埠 |
| `--mcp-port` | 8190 | MCP 連接埠 |
| `-t` | 8 | 整體逾時秒數 |
| `-l` | `zh-tw` | 輸出語言，`zh-tw` 或 `en` |
| `-w` / `-c` | 3 / 10 | 排隊數達到幾筆算 WARNING / CRITICAL |

## LibreNMS 設定

Check Type 選 `comfyui`：

```text
-t 8 -l zh-tw -w 3 -c 10
```

## 輸出格式

第一行是狀態摘要，接著是多行明細，最後一行是 `| ` 開頭的效能資料。欄位名稱固定，取不到的值輸出 `U`：

```text
COMFYUI OK - 執行中 · ComfyUI 0.42.0 · flux-2-klein-4b

GPU: NVIDIA GeForce RTX 4060 Ti
整張 VRAM: 4462.0 / 16030.9 MiB · ComfyUI 佔用: 8.7 MiB
系統 RAM: 24.0 / 125.6 GiB
執行中 / 排隊: 0 / 0

模型 (上一張圖): flux-2-klein-4b
文字編碼器: qwen_3_4b · VAE: flux2-vae

上一張圖 (距今 319 s)
耗時: 27.3 s

圖片 API (8189): 正常 · MCP (8190): 正常
Strata: 停止
| running=1.000;;;0 strata=0.000;;;0 apiup=1.000;;;0 ... queued=0.000;3;10;0 ...
```

## 版本紀錄

- **v1.1**（2026/10/27）：顯示使用的模型（主模型、LoRA、文字編碼器、VAE），主模型也加在第一行
- **v1.0**（2026/10/25）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
