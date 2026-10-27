[English](README.md) | 繁體中文

# check_pmg_queue v1.0

檢查 Proxmox Mail Gateway（PMG）的 Postfix 佇列筆數：先以帳密取得 ticket（`POST /api2/json/access/ticket`），再讀 `GET /api2/json/nodes/<節點>/postfix/queue/<佇列>`。

來源：https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons （v1.0，2024/02/24）

## 需求

Python 3、`requests`（Debian/Ubuntu：`apt install python3-requests`）。

## 參數

| 參數 | 說明 |
|---|---|
| `-H` | PMG 的 FQDN（LibreNMS 會自動帶） |
| `-P` | 連接埠（通常 8006） |
| `-u` | 帳號＠realm，例如 `monitor@pmg` |
| `-p` | 密碼 |
| `-n` | 節點名稱 |
| `-q` | 佇列名稱：`active`、`deferred`、`hold`、`incoming` |
| `-c` | 筆數「超過」這個值就 CRITICAL |

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_pmg_queue`，Check Type 選 `pmg_queue`：

```text
-P 8006 -u "monitor@pmg" -p 'your-password' -n "pmg01" -q "deferred" -c 20
```

## 輸出範例

```text
OK - Queue count is 3 | 'queue_count'=3;20;20;
CRITICAL - Queue count is 25, exceeds critical threshold of 20 | 'queue_count'=25;20;20;0;
```

## 已知問題

- 門檻是「大於」，不是「大於等於」；沒有 WARNING 等級
- 不驗證 PMG 的 TLS 憑證
- PMG 帳號建議用 Audit 角色的唯讀帳號

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
