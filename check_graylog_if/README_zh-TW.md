[English](README.md) | 繁體中文

# check_graylog_if v1.2

檢查 Graylog 最近 5 分鐘有沒有索引失敗（Index Failure）：呼叫 `GET /api/system/indexer/failures/count?since=<5 分鐘前>`。

原本放在 https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons ，v1.2 起在本 repo 維護。

## 需求

LibreNMS 主機（或 Nagios 主機）要有 `curl`。

## 參數

| 參數 | 說明 |
|---|---|
| `-U` | Graylog 帳號 |
| `-P` | 密碼 |
| `-p` | 連接埠（通常 9000） |
| `-H` | Graylog 的 IP 或 FQDN（LibreNMS 會自動帶） |
| `-S` | 用 https（不驗證憑證，curl `-k`） |

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_graylog_if`，Check Type 選 `graylog_if`：

```text
-U "monitor" -P 'your-password' -p 9000 -S
```

## 輸出範例

```text
OK: No index failure.|'index_failure'=0;;1;0
CRITICAL: Index failure occurred (3 records in the last 5 minutes)|'index_failure'=3;;1;0
UNKNOWN: Cannot get index failure count from https://graylog.example.com:9000
```

## 注意事項

- 密碼寫在 LibreNMS 的 Parameters 裡，建議用 Graylog 只有讀取權限的帳號
- 不驗證 Graylog 的 TLS 憑證（curl `-k`）

## 版本紀錄

- **v1.2**（2026/10/27）：5 分鐘內有任何失敗（> 0）都是 CRITICAL，原本只有剛好 1 筆才是；API 連不到或回應不正確時回 UNKNOWN；效能資料加上門檻與最小值；curl 逾時 30 秒
- **v1.1**（2023/12/15）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
