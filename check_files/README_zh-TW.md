[English](README.md) | 繁體中文

# check_files v1.0

NCPA 的 Windows 外掛（PowerShell）：檢查檔案或資料夾是否存在，並可檢查符合條件的檔案數量與最新檔案的時數。NCPA 沒有內建檔案模組，備份檔、匯出檔這類檢查用它。

## 安裝（受監測的 Windows 主機）

複製到 `C:\Program Files\Nagios\NCPA\plugins\check_files.ps1`。NCPA 以 `powershell -ExecutionPolicy Bypass -File` 執行 `.ps1`，不必改系統的執行原則，也不必重新啟動 NCPA。

## 參數

| 參數 | 說明 |
|---|---|
| `-Path` | 必填，檔案或資料夾 |
| `-Filter` | 計數用的萬用字元，預設 `*`，例如 `*.bak` |
| `-MinCount` | 少於這個數量就 CRITICAL |
| `-MaxCount` | 多於這個數量就 CRITICAL |
| `-MaxAgeHours` | 最新的檔案超過這個時數就 CRITICAL |
| `-Recurse` | 計數時包含子資料夾 |

只給 `-Path` 時只檢查存在與否。路徑不存在是 CRITICAL，執行錯誤是 UNKNOWN。

## LibreNMS 設定

Check Type 選 `ncpa`：

```text
-t 'your-token' -M 'plugins/check_files.ps1' -a '-Path D:\Backup -Filter *.bak -MinCount 3'
-t 'your-token' -M 'plugins/check_files.ps1' -a '-Path D:\Backup -Filter *.bak -MaxAgeHours 24'
```

## 輸出範例

```text
OK: 3 file(s) matching *.bak in D:\Backup | 'count'=3;;;
CRITICAL: 3 file(s) matching *.bak in D:\Backup, newest file db-1.bak is 30.2 hours old | 'count'=3;;;
CRITICAL: D:\Backup not found
```

## 限制

- 時數看的是 `LastWriteTime`
- 數量與時數的異常一律回 CRITICAL，沒有 WARNING 等級

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
