[English](README.md) | 繁體中文

# check_strata v1.0

檢查 Strata（本機 LLM 推論服務）的 API 狀態。只讀 `GET /v1/status` 與 `GET /metrics`，不會載入模型或產生文字。

- 模型是否已載入、整機 GPU/RAM 用量、上下文上限
- 上一筆請求的輸入/輸出 token、生成與讀取速度、耗時、距今時間、專家快取命中率
- 排隊數超過門檻告警
- Strata 與 ComfyUI 輪流使用同一張 GPU：Strata API 連不到時，會問同一台的圖片 API（`--comfy-api-port`，預設 8189）ComfyUI 是否在用 GPU，是的話視為正常（OK）；兩者都沒在執行才 WARNING

安裝在 LibreNMS 主機的 `/usr/lib/nagios/plugins/check_strata`，搭配 [check_comfyui](../check_comfyui/)。

## 需求

Python 3，只用標準函式庫。API key 存成檔案，只給 LibreNMS 執行帳號讀：

```bash
sudo install -m 640 -o root -g librenms /dev/null /etc/librenms/strata-api-key
sudo editor /etc/librenms/strata-api-key
```

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `-H` | — | Strata 主機（LibreNMS 會自動帶） |
| `-p` | 8080 | Strata API 連接埠 |
| `--ssl` | — | 用 https |
| `--api-key-file` | — | 必填，API key 檔案路徑 |
| `--comfy-api-port` | 8189 | 同一台圖片 API 的連接埠 |
| `-t` | 8 | 整體逾時秒數 |
| `-l` | `zh-tw` | 輸出語言，`zh-tw` 或 `en` |
| `-w` / `-c` | 2 / 5 | 排隊數達到幾筆算 WARNING / CRITICAL |

## LibreNMS 設定

Check Type 選 `strata`：

```text
-p 8080 -t 8 --api-key-file /etc/librenms/strata-api-key -l zh-tw -w 2 -c 5
```

## 輸出格式

第一行是狀態摘要，接著是多行明細，最後一行是 `| ` 開頭的效能資料。效能資料的欄位名稱固定（不隨語言、狀態、模型改變），取不到的值輸出 `U`，不會補 0：

```text
STRATA OK - 已載入 · example-model
（明細數行）
| loaded=1.000;;;0 gpuusedmib=... queued=0.000;2;5;0 livetps=U;;;0
```

API key 讀不到是 UNKNOWN、API 回 HTTP 錯誤是 CRITICAL、資料格式不對是 UNKNOWN。

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
