[English](README.md) | 繁體中文

# check_diff_webhtml v1.1

偵測網頁內容有沒有被改動：每次抓一次網址，與上一次抓到的內容比較字元數，不同就 CRITICAL。可用來發現首頁被置換、被植入內容這類異動。

原本放在 https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons ，v1.1 起在本 repo 維護。

## 需求

`curl`、`bc`、`diff`、`md5sum`。

## 參數

| 參數 | 說明 |
|---|---|
| `-H` | 網址，不含通訊協定，例如 `www.example.com/index.html`（LibreNMS 會自動帶裝置主機名稱） |
| `-S` | 用 https |
| `-k` | 不驗證憑證 |
| `-d` | 允許的字元數差異（增加或減少都算），差異在範圍內仍是 OK |
| `-P` | 持續告警：內容改變後保留原本的比較基準，持續回報 CRITICAL，直到用 `-A` 接受 |
| `-A` | 把目前內容設為新的比較基準（搭配 `-P`，手動執行） |

比較基準存在 `/var/tmp/check_diff_webhtml/<網址 md5>.previous`，重新開機也會保留；v1.0 放在 `/tmp` 的基準檔第一次執行時會自動搬過來。

沒加 `-P` 時，每次執行都把這次的內容當成下一次的基準，所以一次改動只會出現一輪 CRITICAL，要搭配告警通知。要「改了就一直亮紅燈，確認過才解除」就加 `-P`，確認後以 LibreNMS 的執行帳號手動跑一次加 `-A` 的指令：

```bash
sudo -u librenms /usr/lib/nagios/plugins/check_diff_webhtml -H www.example.com -S -A
```

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_diff_webhtml`，Check Type 選 `diff_webhtml`：

```text
-S
```

## 輸出範例

```text
OK: First time execution, no previous content to compare with (File size: 12.31KB)
OK: Content is unchanged (File size: 12.31KB)
CRITICAL: Content has changed. Difference in character count: 42 (Difference text is "3c3< <title>"...) (File size: 12.35KB, Previous file size: 12.31KB)
```

## 限制

- 只比字元數，內容改了但長度相同時偵測不到
- 動態網頁（含時間、隨機值、CSRF token）每次都會不同，不適用

## 版本紀錄

- **v1.1**（2026/10/27）：基準檔改放 `/var/tmp`（自動搬移舊檔）；`-d` 改比較絕對值，內容變少也會告警；新增 `-P`、`-A`；HTTP 錯誤（4xx、5xx）視為抓取失敗；curl 逾時 30 秒；差異摘要的截斷修正
- **v1.0**（2023/12/26）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
