[English](README.md) | 繁體中文

# check_extip v1.0

檢查對外（WAN）IP 有沒有變更。同時向多個公開的「查詢我的 IP」服務查詢，取多數一致的結果與預期位址比對，避免單一服務出錯就誤報。

取代 it-scripts 裡的 `check_ext_ip`（v1.5，改寫自 Justin Reherman 的版本），整支重新撰寫，`-H`、`-S`、`-t`、`-l`、`-v`、`-V`、`-h` 的用法相容，原本的服務直接換 Check Type 就能用。

## 與 check_ext_ip 的差異

| 項目 | check_ext_ip v1.5 | check_extip |
|---|---|---|
| 判斷方式 | 隨機挑 3 個服務，**第一個有回應的**就當結果 | 同時查詢，**至少 2 個結果相同**才判斷；不夠時再補問一輪 |
| 服務結果不一致 | 不會發現 | 列出各服務的結果；票數相同時回 UNKNOWN |
| 查詢方式 | 逐一查詢，最壞情況要等「服務數 × 逾時」 | 平行查詢；全部失敗就停止，不再逐一等逾時 |
| 預期位址 `-H` | 單一 IPv4 | IP、多個 IP（逗號分隔）、CIDR、**主機名稱**（比對 DDNS） |
| 備援線路 | 沒有 | `-W`：切到備援線路時回 WARNING，不是 CRITICAL |
| IPv6 | 沒有 | `-6` |
| IP 格式檢查 | 正規表示式，`999.999.999.999` 也會通過 | Python `ipaddress` 驗證 |
| 回傳非公開位址 | 照樣比對 | 服務回傳私有/保留位址時回 UNKNOWN |
| 自訂服務 | 沒有 | `-U` 加入自己的查詢網址 |
| 效能資料 | `match` | `match`、`providers`、`answered`、`agree`、`time` |
| 失效的服務 | `ipsimple` 已無法連線 | 移除 `ipsimple`，新增 `seeip`、`dnsomatic`（2026/10 逐一實測） |

## 需求

Python 3.8 以上，只用標準函式庫。LibreNMS 主機要能連到外部 HTTPS。

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `-H` | — | 必填。預期的對外位址：IP、逗號分隔的多個 IP、CIDR，或主機名稱（解析 A/AAAA 記錄後比對）。LibreNMS 會帶入服務的「IP 位址」欄位 |
| `-W` | — | 備援線路的 IP 或 CIDR，對外 IP 是這些位址時回 WARNING |
| `-S` | 隨機 3 個 | 指定服務，逗號分隔，全部都會查詢 |
| `-U` | — | 額外的查詢網址（https，回傳純文字 IP），可重複 |
| `-n` | 3 | 沒有 `-S` 時第一輪查詢幾個服務 |
| `-q` | 2 | 需要幾個相同結果。`-S` 只列 1～2 個服務時預設 1（與 v1.5 相同的行為） |
| `-t` | 5 | 每個服務的逾時秒數 |
| `-6` | — | 檢查 IPv6 位址 |
| `-v` | — | 列出每個服務的結果與耗時 |
| `--lang` | `en` | 輸出語言，`en` 或 `zh-tw` |
| `-l` | — | 列出內建的服務 |
| `-V` / `-h` | — | 版本 / 說明 |

## 內建服務

`amazonaws`、`dnsomatic`、`icanhazip`、`ident`、`ifconfigco`、`ifconfigme`、`ipecho`、`ipify`、`ipinfo`、`ipme`、`seeip`、`wtfismyip`。全部免費、不需要 API key，回傳純文字的位址；只連 HTTPS 並驗證憑證。`-l` 可看各自的 IPv4/IPv6 網址。

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_extip`，新增服務時 Check Type 選 `extip`，「IP 位址」欄位填預期的對外 IP，Parameters 可以留空：

```text
（留空）
-W 198.51.100.20
-H 203.0.113.8/29
-H home.example.com
--lang zh-tw
```

`-H home.example.com` 會比對 DDNS 名稱目前解析到的位址，用來發現 DDNS 沒有更新。

## 輸出範例

```text
OK - External IP 203.0.113.10 is as expected (3/3 providers agree: ipify, icanhazip, amazonaws) | match=1;;;0;1 providers=3;;;0 answered=3;;;0 agree=3;;;0 time=0.332s;;;0
CRITICAL - External IP changed to 198.51.100.7, expected 203.0.113.10 (3/3 providers agree: ident, ipme, seeip) | match=0;;;0;1 ...
WARNING - External IP 198.51.100.20 is a backup WAN address (failover active?) (3/3 providers agree: ...) | match=0;;;0;1 ...
CRITICAL - External IP 198.51.100.7 does not match home.example.com (203.0.113.10), DDNS not updated? (3/3 providers agree: ...) | match=0;;;0;1 ...
UNKNOWN - All providers failed (tried: ipify, ident, seeip). Could not determine external IP | match=0;;;0;1 ...
OK - 對外 IP 203.0.113.10 與預期相同 (3/3 個服務一致: ipify, icanhazip, amazonaws) | match=1;;;0;1 ...
```

加 `-v` 時，第一行是結果，接著每個服務一行，效能資料在最後一行。

## 注意事項

- 每次檢查會對外發出 3 個左右的 HTTPS 請求。LibreNMS 預設每 5 分鐘檢查一次，不會碰到這些服務的使用限制
- 在 CGNAT 後面時，服務看到的是電信業者的位址，不是路由器 WAN 介面上的位址

## 版本紀錄

- **v1.0**（2026/10/27）：第一版，取代 `check_ext_ip` v1.5

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
