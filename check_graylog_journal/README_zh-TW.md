[English](README.md) | 繁體中文

# check_graylog_journal v1.1

檢查 Graylog 節點的 Journal 使用率：呼叫 `GET /api/system/journal`，以 `journal_size / journal_size_limit` 計算百分比，達到門檻就 CRITICAL。Journal 累積代表訊息進來的速度大於寫進 OpenSearch 的速度。

原本放在 https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons ，v1.1 起在本 repo 維護。

## 需求

`curl`、`bc`。

## 參數

| 參數 | 說明 |
|---|---|
| `-U` / `-P` | Graylog 帳號、密碼 |
| `-p` | 連接埠（通常 9000） |
| `-H` | Graylog 的 IP 或 FQDN（LibreNMS 會自動帶） |
| `-c` | 使用率門檻（%），達到就 CRITICAL |
| `-S` | 用 https（不驗證憑證） |

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_graylog_journal`，Check Type 選 `graylog_journal`：

```text
-U "monitor" -P 'your-password' -p 9000 -S -c 10
```

## 輸出範例

```text
OK: Journal usage is normal. 0.20% (10.48MB/5.00GB)|'journal_usage'=0.20;;10;0;100
CRITICAL: Journal usage exceeds 10% ! (612.00MB/5.00GB)|'journal_usage'=11.95;;10;0;100
UNKNOWN: Cannot get journal size from https://graylog.example.com:9000
```

## 版本紀錄

- **v1.1**（2026/10/27）：`-c` 改為必填（沒給時回 UNKNOWN，原本 `bc` 報錯）；API 連不到或沒有 journal 大小時回 UNKNOWN；百分比改成先乘 100 再除，小數不再被截成 0；效能資料加上門檻與 0～100 範圍；curl 逾時 30 秒
- **v1.0**（2023/12/22）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
