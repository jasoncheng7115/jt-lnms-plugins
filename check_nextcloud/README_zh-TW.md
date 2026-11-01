[English](README.md) | 繁體中文

# check_nextcloud v1.0

監測 Nextcloud 伺服器，一支外掛，每個服務用 `-C` 指定看哪一面：

| `-C` | 看什麼 | 何時告警 |
|---|---|---|
| `status` | `status.php`（不用登入） | 未安裝完成、維護模式、需要資料庫升級 → CRITICAL |
| `updates` | 核心與 app 更新 | 有更新 → WARNING，列出每個 app 的新版本 |
| `storage` | 資料目錄剩餘空間、使用者、檔案數 | 剩餘空間 ≤ `-w` / `-c` GB（預設 50 / 20） |
| `shares` | 分享數、公開連結、沒有密碼的公開連結 | 無密碼公開連結 ≥ `-w` / `-c` 個（預設不告警） |
| `users` | 5 分鐘 / 1 小時 / 24 小時 / 7 天活躍使用者 | 只畫圖 |
| `php` | OPcache（啟用、已滿、命中率、浪費比例、interned strings）、APCu | OPcache 未啟用 → CRITICAL；已滿、命中率 < `--hit-warn`（95%）、浪費 > `--wasted-warn`（10%）、interned strings 或 APCu 剩不到 5% → WARNING |
| `system` | Nextcloud 主機的負載與記憶體 | 每顆 CPU 的 5 分鐘負載 ≥ `-w` / `-c`（預設 2 / 4）；記憶體使用 ≥ `--mem-warn` / `--mem-crit`（90 / 95%） |
| `database` | 資料庫種類、版本、大小 | 大小 ≥ `-w` / `-c` GB（預設不告警） |
| `setup` | 管理設定「概覽」頁的設定檢查：背景工作（cron）多久沒跑、缺少的索引、安全性警告、紀錄檔錯誤…… | 有「錯誤」→ CRITICAL，有「警告」→ WARNING；結果快取 `--cache` 分鐘 |

除了 `status`，其他都讀 serverinfo API（`/ocs/v2.php/apps/serverinfo/api/v1/info`），需要管理員帳號，或 serverinfo token（`--nc-token`）。`setup` 一定要管理員帳號。

取代 BornToBeRoot 的 `check_nextcloud.py`：那支的 `apps` 檢查在 Nextcloud 28 以後會直接崩潰（serverinfo 沒指定就不回傳 app 清單），而且看不到維護模式、核心更新、剩餘空間、OPcache 與設定檢查。

安裝在 LibreNMS 主機的 `/usr/lib/nagios/plugins/check_nextcloud`。

## 需求

- Python 3，只用標準函式庫
- Nextcloud 啟用 serverinfo app（預設就有）
- 一個管理員帳號，建議專門給監控用，並設成 app 密碼

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `-H` | — | Nextcloud 主機（LibreNMS 會自動帶） |
| `-C` | — | 要檢查的項目，見上表 |
| `-P` | 443 | 連接埠 |
| `--http` | — | 用 http |
| `-k` | — | 不驗證憑證 |
| `-u` | — | 帳號 |
| `-a` | — | 認證檔，一行 `帳號:密碼` |
| `--password` | — | 密碼（會出現在 LibreNMS 畫面與行程清單，建議改用 `-a`） |
| `--nc-token` | — | serverinfo token（`occ config:app:set serverinfo token --value ...`），`setup` 以外的檢查可以不用管理員密碼 |
| `-t` | 30 | 逾時秒數（`setup` 至少 90） |
| `-w` / `-c` | 見上表 | 依檢查項目而定 |
| `--mem-warn` / `--mem-crit` | 90 / 95 | `system` 記憶體使用率 |
| `--hit-warn` | 95 | `php` OPcache 命中率下限 |
| `--wasted-warn` | 10 | `php` OPcache 浪費比例上限 |
| `--ignore` | — | 逗號分隔。`updates`：不看這些 app；`setup`：忽略名稱或類別名稱含這些字的項目 |
| `--ignore-core` | — | `updates` 不看核心更新（刻意停在某個大版本時） |
| `--cache` | 60 | `setup` 結果快取幾分鐘（跑一次要數十秒） |
| `-l` | `zh-tw` | 輸出語言，`zh-tw` 或 `en` |

密碼的優先順序：`--password`、`-a` 認證檔、環境變數 `NEXTCLOUD_PASSWORD`。

## 安裝

```bash
install -o root -g root -m 0755 check_nextcloud /usr/lib/nagios/plugins/check_nextcloud
install -d -o root -g librenms -m 0750 /etc/librenms-checks
printf 'monitor:your-app-password\n' > /etc/librenms-checks/nextcloud.auth
chown librenms:librenms /etc/librenms-checks/nextcloud.auth
chmod 600 /etc/librenms-checks/nextcloud.auth
```

`setup` 的快取放在 `/var/tmp/check_nextcloud/`（權限 700，由 LibreNMS 帳號自動建立）。

## LibreNMS 設定

Check Type 選 `nextcloud`，每一項建一個服務：

```text
-a /etc/librenms-checks/nextcloud.auth -C status
-a /etc/librenms-checks/nextcloud.auth -C updates
-a /etc/librenms-checks/nextcloud.auth -C storage -w 50 -c 20
-a /etc/librenms-checks/nextcloud.auth -C shares
-a /etc/librenms-checks/nextcloud.auth -C users
-a /etc/librenms-checks/nextcloud.auth -C php
-a /etc/librenms-checks/nextcloud.auth -C system -w 2 -c 4
-a /etc/librenms-checks/nextcloud.auth -C database
-a /etc/librenms-checks/nextcloud.auth -C setup --cache 30 --ignore whiteboard,HighPerformanceBackend
```

Nextcloud 不在 443 時加 `-P 8443`。

## 輸出範例

```text
NEXTCLOUD WARNING - Nextcloud 31.0.9.1 - 核心可更新到 32.0.1.2; 2 個 app 可更新
calendar -> 5.5.6
mail -> 5.5.12
已安裝 64 個 app
| app_updates=2;1;;0 core_update=1;1;;0;1
```

```text
NEXTCLOUD OK - PHP 8.3.6 - OPcache 命中率 99.87% · 使用 30% · 浪費 5.2%
APCu 使用 12% · 命中率 98.9%
memory_limit 1.0 GB · upload 10.0 GB
| opcache_hit=99.87%;95;;0;100 opcache_used=29.8%;;;0;100 opcache_wasted=5.22%;10;;0;100 strings_used=63.9%;95;;0;100 apcu_used=11.7%;95;;0;100 apcu_hit=98.85%;;;0;100
```

```text
NEXTCLOUD WARNING - 0 個錯誤、1 個警告（已忽略 2 項）（快取 12 分鐘前）

[警告] 紀錄檔中的錯誤 (LogErrors)
從 2026年1月5日 凌晨3:59:07 開始，紀錄檔中有 9 個錯誤
| errors=0;;1;0 warnings=1;1;;0
```

連不到主機、HTTP 錯誤、帳號密碼錯誤是 CRITICAL；回傳不是 JSON、缺少帳號密碼是 UNKNOWN。

## 設計重點

- **效能資料放在最後一行**：LibreNMS 把所有輸出合併後以第一個 `|` 切開，所以訊息裡的 `|`（包含 Nextcloud 回傳的文字）都會換成 `/`
- **效能資料的欄位名稱固定，而且不超過 19 個英數字**：LibreNMS 會去掉其他字元、截成 19 字，並在第一次輪詢就決定 RRD 欄位。所以 app 名稱只出現在訊息，不當成欄位
- **`setup` 有快取**：Nextcloud 跑一次設定檢查要數十秒，每 5 分鐘跑一次太重
- **不經過系統代理伺服器**，直接連 Nextcloud
- 從舊的 `check_nextcloud.py` 改過來時，效能資料欄位名稱不同，要建新服務，不能直接改舊服務的 Check Type

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
