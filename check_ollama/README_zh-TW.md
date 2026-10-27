[English](README.md) | 繁體中文

# check_ollama v1.0

檢查 Ollama 目前載入在記憶體裡的模型：呼叫 `GET /api/ps`（另讀 `/api/version` 顯示版本，失敗不影響結果）。Ollama 可以同時常駐多個模型，所以全部列出，每個模型顯示 VRAM 用量、在 GPU 上的比例、參數量與量化、上下文長度，以及多久後卸載。

安裝在 LibreNMS 主機的 `/usr/lib/nagios/plugins/check_ollama`。

## 需求

Python 3，只用標準函式庫。

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `-H` | — | Ollama 主機（LibreNMS 會自動帶） |
| `-p` | 11434 | 連接埠 |
| `--ssl` | — | 用 https |
| `--api-key` | — | 前面有反向代理要 Bearer token 時使用 |
| `-t` | 10 | 逾時秒數 |
| `-l` | `zh-tw` | 輸出語言，`zh-tw` 或 `en` |
| `-w` / `-c` | — | 所有模型 VRAM 合計（GB）達到多少算 WARNING / CRITICAL |
| `--min-models` | — | 載入的模型少於 N 個就 WARNING，用來發現應該常駐卻被卸載的模型 |
| `--expiring` | — | 有模型在 N 秒內就要卸載時 WARNING |

## LibreNMS 設定

Check Type 選 `ollama`：

```text
-w 80 -c 100
```

## 輸出範例

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

連不到 Ollama 或回 HTTP 錯誤是 CRITICAL，回傳不是 JSON 是 UNKNOWN。

## 設計重點

- **效能資料放在最後一行**：LibreNMS 把所有輸出合併後以第一個 `|` 切開，`|` 之後全部當效能資料，所以明細一定要在前面
- **效能資料的欄位名稱固定**（`models`、`vram`、`size`），不用模型名稱：LibreNMS 第一次輪詢就決定 RRD 的欄位，載入的模型換了就會對不上；而且它會去掉非英數字元並截成 19 字，`qwen3-vl:2b` 會變 `qwen3vl2b`
- LibreNMS 的訊息欄很窄，而且會把連續空白壓成一個，所以每行都短、不用空白對齊

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
