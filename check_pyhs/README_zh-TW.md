[English](README.md) | 繁體中文

# check_pyhs v1.1

檢查 TP-Link Kasa 6 孔智慧延長線（HS300 這類每孔都有電量計的型號）各插座的即時用電，可對功率、電壓、電流設門檻。透過 `pyhs100` 指令讀取裝置狀態，解析 `== Current State ==` 區段。

安裝在 LibreNMS 主機的 `/usr/lib/nagios/plugins/check_pyhs`。

## 需求

- Python 3
- `pyhs100` 指令（`pip install pyHS100`，目前裝的是 0.3.5.2）

注意：pyHS100 已停止維護，後繼專案是 `python-kasa`（指令 `kasa`），輸出格式不同，換套件要一起改這支外掛。

## 參數

| 參數 | 說明 |
|---|---|
| `-H` | 延長線的 IP（LibreNMS 會自動帶） |
| `--plug` | 插座編號 1～6；不給就列出全部插座 |
| `-w` / `-c` | 門檻，逗號分隔。`指標:值` 套用到所有插座，`plug<編號>:指標:值` 只套用到該插座；達到（≥）就告警 |
| `--show-device-name` | 輸出加上裝置名稱 |

指標名稱就是裝置回傳的欄位，例如 `power_mw`（毫瓦）、`voltage_mv`（毫伏）、`current_ma`（毫安）、`total_wh`（累計瓦時）。

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_pyhs`，Check Type 選 `pyhs`，每個插座一筆：

```text
--plug 2 -c power_mw:230000
```

上面是第 2 孔功率達到 230 W 就 CRITICAL。

## 輸出範例

```text
OK - Plug 2 (NAS) |voltage_mv=110512 current_ma=812 power_mw=85230;;230000.0 total_wh=15320
CRITICAL - Plug 2 (NAS) - Alert on: power_mw=231200 |voltage_mv=110230 current_ma=2105 power_mw=231200;;230000.0 total_wh=15322
CRITICAL - Cannot connect to 192.168.1.30
```

不給 `--plug` 時，第一行是總結、每個插座一行狀態，效能資料集中在最後一行，欄位名稱加上 `plug<編號>_` 前置字串：

```text
OK - Status for all plugs:
Plug 1 (Router): OK
Plug 2 (NAS): OK
...
| plug1_voltage_mv=110512 plug1_current_ma=72 plug1_power_mw=4043 plug1_total_wh=463 plug2_voltage_mv=110288 ...
```

## 版本紀錄

- **v1.1**（2026/10/27）：全部插座模式的效能資料改成只在最後一行輸出一次（`plug<編號>_` 前置字串），LibreNMS 才能正確解析；改用 `pyhs100` 的結束碼判斷錯誤，stderr 只有警告時不再誤判 CRITICAL；插座名稱依清單順序讀取，沒有自訂名稱的插座也抓得到；執行逾時 30 秒；檢查 `--plug` 範圍
- **v1.0**（2025/02/08）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
