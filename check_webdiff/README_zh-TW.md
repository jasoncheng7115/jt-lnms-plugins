[English](README.md) | 繁體中文

# check_webdiff v1.0

偵測網頁有沒有被竄改。比對前先排除每次請求都會變的內容（防快取參數、nonce、CSRF token、時間戳記、HTML 註解）；發現差異時立刻再抓一次，兩次之間就不同的部分視為隨機內容略過，只有兩次都一致、而且與比較基準不同的變更才告警。另外會追蹤頁面引用的外部 script、iframe、表單主機，也可以檢查「必須出現」與「不得出現」的文字。

取代 [check_diff_webhtml](../check_diff_webhtml/)，整支重新撰寫，參數不相容。

## 偵測項目

| 項目 | 說明 | 預設狀態 |
|---|---|---|
| 內容變更 | 排除動態內容後與比較基準不同 | CRITICAL（`--on-change warn` 改為 WARNING） |
| 新的外部主機 | script、iframe、表單送出網址、embed/object 出現沒看過的第三方網域 | WARNING（`--new-hosts crit/off`） |
| 缺少預期文字 | `-e` 指定的文字不在頁面上 | CRITICAL |
| 出現不允許的文字 | `-x` 指定的文字出現在頁面上（不分大小寫） | CRITICAL |
| 轉址到其他網站 | 最後的網址不在同一個網域 | 附註在訊息裡 |
| 抓取失敗 | 連不到、逾時、HTTP 狀態碼不在 `--status` 裡 | UNKNOWN（`--fetch-error crit` 改為 CRITICAL） |

內容變更與新的外部主機預設會**持續告警，直到用 `--accept` 接受**，不會下一輪就自己恢復 OK。要沿用「只回報一次」的做法就加 `--once`。

## 動態內容的排除

**內建規則**（`--raw` 可關閉），比對前換成固定的佔位字串：

| 規則 | 對象 |
|---|---|
| comment | HTML 註解（快取外掛、產生時間），IE 條件註解除外 |
| buster | 防快取參數的值：`v`、`ver`、`version`、`t`、`ts`、`time`、`timestamp`、`_`、`cb`、`cache`、`rand`、`random`、`r`、`nocache`、`nc`、`bust`、`rev`、`hash` |
| qnumber | 任何網址參數中 6 位以上的數字或 16 位以上的十六進位值 |
| nonce | `nonce`、`data-nonce`、`data-csrf`、`data-token` 屬性 |
| csrf-meta | `<meta name="csrf-token">` 這類 meta |
| token-input | 隱藏欄位：`_csrf*`、`_token`、`authenticity_token`、`_wpnonce`、`__VIEWSTATE*`、`__EVENTVALIDATION`、`__RequestVerificationToken`、`form_build_id`、`form_token`、`security`、`nonce` |
| js-nonce | JavaScript 物件裡的 `"nonce":"…"`、`"csrfToken":"…"` 等 |
| datetime / time / epoch | `2026-10-27 21:22:47`、ISO 8601、`21:22:47`、10 或 13 位數的 Unix 時間 |
| uuid | UUID |

`integrity="sha384-…"` 不排除：這個值只在 script 本身被換掉時才會變。

**連抓兩次**（`--no-confirm` 可關閉）：內容與基準不同時立刻再抓一次，兩次之間就不同的行視為隨機內容。建立比較基準時也會抓兩次。內容沒變的靜態網站每次只抓一次。

**自訂規則**：`-I '正規表示式'` 可重複指定，比對前先換掉符合的部分。

## 比對模式（`-m`）

| 模式 | 比對內容 | 適合 |
|---|---|---|
| `full`（預設） | 整頁 HTML，每個標籤與文字一行 | 一般網站 |
| `text` | 只比可見文字（不含 script、style） | 版面常改、但文字不該被改的網站 |
| `key` | `<title>`、script（src＋integrity，或「inline」）、iframe、表單、樣式表、meta refresh、base、embed/object | 最新消息、輪播這類內容本來就常更新的網站：只抓結構被動手腳 |

## 需求

Python 3.8 以上，只用標準函式庫。

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `-u`, `--url` | — | 完整網址，優先於 `-H` |
| `-H`, `--host` | — | 主機名稱（LibreNMS 會自動帶裝置主機或服務的 IP 欄位） |
| `-p`, `--path` | — | 接在 `-H` 後面的路徑，例如 `/index.html` |
| `--http` | — | 搭配 `-H` 時改用 http（預設 https） |
| `-k`, `--insecure` | — | 不驗證 TLS 憑證 |
| `--no-follow` | — | 不跟隨轉址 |
| `--status` | `200` | 可接受的 HTTP 狀態碼，逗號分隔 |
| `-t`, `--timeout` | 15 | 逾時秒數 |
| `-m`, `--mode` | `full` | `full`、`text`、`key` |
| `-I`, `--ignore` | — | 比對前排除的正規表示式，可重複 |
| `--raw` | — | 關閉內建的排除規則 |
| `--no-confirm` | — | 發現差異時不再抓第二次 |
| `-d`, `--max-diff` | 0 | 變更量（刪除＋新增的 bytes）在這個值以內算 OK |
| `-e`, `--expect` | — | 必須出現的文字（區分大小寫），可重複 |
| `-x`, `--reject` | — | 不得出現的文字（不分大小寫），可重複 |
| `--new-hosts` | `warn` | 新的外部主機：`warn`、`crit`、`off` |
| `--on-change` | `crit` | 內容變更的狀態：`crit`、`warn` |
| `--fetch-error` | `unknown` | 抓取失敗的狀態：`unknown`、`crit` |
| `--once` | — | 變更只回報一次，之後以新內容為基準 |
| `-A`, `--accept` | — | 接受目前內容為新的基準（手動執行） |
| `--state-dir` | `/var/tmp/check_webdiff` | 比較基準存放位置 |
| `--keep` | 5 | 保留最近幾次變更的前後版本（0 = 不保留） |
| `-v`, `--verbose` | — | 列出變更的行與排除了哪些內容 |
| `--lang` | `en` | 輸出語言，`en` 或 `zh-tw` |
| `-V` | — | 版本 |

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_webdiff`，Check Type 選 `webdiff`。LibreNMS 會帶 `-H`（服務的 IP 欄位或裝置主機名稱）：

```text
（留空）                                   https://<裝置主機>/
--http                                     http://<裝置主機>/
-p /index.html -e "Example Corp" -x "hacked by"
-m key --new-hosts crit
-u https://www.example.com/shop/ -I 'id="visitor-count">[0-9]+'
```

確認變更是正常更新後，用 **LibreNMS 的執行帳號**、**與服務相同的參數**加上 `--accept`：

```bash
sudo -u librenms /usr/lib/nagios/plugins/check_webdiff -H www.example.com --accept
```

用 root 執行也可以，檔案擁有者會維持資料夾原本的帳號。比較基準依「網址＋模式＋`-I` 規則」分開存放，參數要和服務一致才會更新到同一份。

每次變更的前後版本存在 `/var/tmp/check_webdiff/<代碼>/history/`（`-before.html`、`-after.html`），持續告警期間同一個變更只存一次，事後可以直接用 `diff` 比對。

## 輸出範例

```text
OK - Content unchanged (https://www.example.com) | size=225668B;;;0 time=0.636s;;;0 hosts=0;;;0 changed=0B;;0;0
CRITICAL - Content changed: 1 block(s), 16 bytes; not accepted yet, baseline from 2026-10-27 21:27:00 (accept with --accept) (https://www.example.com) | ...
CRITICAL - New external host(s): cdn.evil.example.net; Content changed: 1 block(s), 57 bytes; ... | ... hosts=1;;;0 ...
CRITICAL - Expected text not found: Example Corp; Rejected text found: hacked by; ... | ...
UNKNOWN - Fetch failed: HTTP 404 (expected 200) (https://www.example.com/missing)
```

加 `-v` 時第一行是結果，接著是排除統計與變更的行（`-` 是基準、`+` 是目前），效能資料在最後一行：

```text
CRITICAL - Content changed: 1 block(s), 16 bytes; ...
ignored: buster 3, comment 1, csrf-meta 1, epoch 1, js-nonce 1, nonce 1, token-input 1, random between two fetches 1
- Welcome
+ Defaced
| size=734B;;;0 ...
```

## 限制

- 不執行 JavaScript：前端框架渲染出來的內容看不到，`key` 模式仍可抓到 script 被換掉
- 每小時或每天才變一次、又沒有固定格式的內容（例如每日一句），「連抓兩次」看不出來，要用 `-I` 或 `-m key`
- 外部主機以網域判斷是否為第三方（`www.example.com` 與 `cdn.example.com` 視為同一個網站），沒有使用完整的 Public Suffix List
- 頁面上限 5 MB

## 版本紀錄

- **v1.0**（2026/10/27）：第一版，取代 `check_diff_webhtml`

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
