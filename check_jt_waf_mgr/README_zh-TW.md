[English](README.md) | 繁體中文

# check_jt_waf_mgr v1.2

檢查由 [jt-waf-mgr](https://github.com/jasoncheng7115/jt-waf-mgr) 管理的 WAF（nginx＋ModSecurity）是否正常運作。只用只有 `status:read` 權限的 API 權杖讀 `GET /api/v1/health`，不會改動任何東西。

- WAF 是否暫停中（排查用；jt-waf-mgr 0.4.82 以上，暫停期間是 WARNING）
- nginx 主程序是否執行中、ModSecurity 是否為封鎖模式（`DetectionOnly` 是 WARNING，引擎關閉是 CRITICAL）
- 受管理規則檔是否被外部修改、最近一次套用是否失敗、24 小時內設定是否被外部修改
- 事件收集是否仍在讀 ModSecurity 稽核記錄、IP 封鎖清單是否被 nginx 載入、程式完整性、稽核鏈、事件分析是否連續兩次失敗
- 最近 1 小時／24 小時的事件與封鎖數、封鎖中的 IP、待處理警示、待核准變更輸出成效能資料

整體狀態取 jt-waf-mgr 回報的最差檢查項目；`--ignore` 可把指定項目排除在外。需要 jt-waf-mgr 0.4.80 以上。

安裝在 LibreNMS 主機的 `/usr/lib/nagios/plugins/check_jt_waf_mgr`。

## 需求

Python 3，只用標準函式庫。

在 jt-waf-mgr 的「管理 → API 權杖」新增權杖：權限只勾 `status:read`，允許的來源位址填 LibreNMS 主機（例如 `192.168.1.x/32`）。權杖存成檔案，只給 LibreNMS 執行帳號讀：

```bash
sudo install -m 640 -o root -g librenms /dev/null /etc/librenms/jt-waf-mgr-token
sudo editor /etc/librenms/jt-waf-mgr-token
```

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `-H` | — | jt-waf-mgr 主機名稱或位址（LibreNMS 會自動帶） |
| `-p` | 443 | 連接埠 |
| `--vhost` | 同 `-H` | 管理介面的站名，當作 Host 標頭與 TLS SNI（例如 `waf.example.com`） |
| `--no-ssl` | — | 用 http（例如在同一台直接連服務的 `127.0.0.1:8095`） |
| `-k` | — | 不驗證 TLS 憑證 |
| `--ca-file` | — | 私有 CA 簽發的憑證要用的 CA 檔 |
| `--token-file` | — | 必填，API 權杖檔案路徑 |
| `--ignore` | — | 不列入整體狀態的檢查項目，以逗號分隔（例如 `analyst,ip_blocks`） |
| `-t` | 10 | 逾時秒數 |
| `-l` | `zh-tw` | 輸出語言，`zh-tw` 或 `en` |

檢查項目名稱：`nginx`、`modsecurity`、`waf_pause`、`managed_rules`、`last_apply`、`collector`、`ip_blocks`、`program_integrity`、`audit_chain`、`config_changes`、`analyst`。

## LibreNMS 設定

在 WAF 主機那台裝置新增 Service，Check Type 選 `jt_waf_mgr`：

```text
-p 443 --vhost waf.example.com --token-file /etc/librenms/jt-waf-mgr-token -l zh-tw
```

## 輸出格式

第一行是狀態摘要（最嚴重的幾個問題，或「運作正常」加版本），接著每個檢查項目一行與統計數字，最後一行是 `| ` 開頭的效能資料。效能資料的欄位名稱固定（不隨語言、狀態改變），取不到的值輸出 `U`，不會補 0：

```text
JT-WAF-MGR OK - 運作正常 · jt-waf-mgr 0.4.80
（明細數行）
| problems=0;;;0 events1h=12;;;0 blocked1h=9;;;0 blocked24h=240;;;0 lasteventagesec=85;;;0 collectorlagsec=1;;;0 ipblocks=3;;;0 openalerts=1;;;0 pendingchanges=0;;;0
```

連不到 jt-waf-mgr 或 HTTP 錯誤是 CRITICAL；權杖檔讀不到、權杖被拒（401/403）、資料格式不對是 UNKNOWN。

## 版本紀錄

- **v1.2**（2026/11/17）：新增 `waf_pause` 檢查（排查時暫停 WAF，jt-waf-mgr 0.4.82 以上）；引擎設定為只偵測、但由規則封鎖時，ModSecurity 會顯示「由規則封鎖」；最近一次套用的結果改用中文顯示
- **v1.0**（2026/11/17）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
