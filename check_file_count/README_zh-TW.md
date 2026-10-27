[English](README.md) | 繁體中文

# check_file_count v1.0

NCPA 的 Windows 外掛（純 CMD）：資料夾裡有檔案就 CRITICAL、沒有就 OK。用在「處理完就該清空」的資料夾，例如匯入佇列、待傳送區。只用 `dir` 與 `find`，不需要 PowerShell。

## 安裝（受監測的 Windows 主機）

複製到 `C:\Program Files\Nagios\NCPA\plugins\check_file_count.bat`。

檔案是純 ASCII、CRLF 換行，任何 Windows 字碼頁都能正確執行。

## 參數

第一個參數是要檢查的資料夾。計數包含子資料夾裡的檔案（`dir /s`），不算資料夾本身。

## LibreNMS 設定

Check Type 選 `ncpa`：

```text
-t 'your-token' -M 'plugins/check_file_count.bat' -a 'D:\Inbox'
```

## 輸出範例

```text
OK - no files in "D:\Inbox"
CRITICAL - 2 files found in "D:\Inbox"
CRITICAL - directory "D:\Inbox" does not exist or cannot be accessed
```

## 限制

- 沒有效能資料，也沒有門檻參數；需要數量上下限改用 [check_files](../check_files/)

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
