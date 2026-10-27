[English](README.md) | 繁體中文

# check_ncpa_short v1.0

`check_ncpa` 的包裝外掛：只保留第一行輸出（狀態＋效能資料），結束碼照原樣傳回。

## 為什麼需要

NCPA `logs` 模組（Windows 事件記錄）會在第一行的 `|` 之後再接每一筆事件的明細。LibreNMS 把 `|` 之後全部當成效能資料解析，事件明細寫不進 RRD，InfluxDB 也會報 `missing field key`，服務的 `service_ds` 會被塞滿垃圾欄位。

`processes` 模組的長輸出在 `|` 之前，不受影響，照用 `ncpa` 即可。

## 安裝（LibreNMS 主機）

```bash
sudo install -m 755 check_ncpa_short /usr/lib/nagios/plugins/check_ncpa_short
```

前提是 `/usr/lib/nagios/plugins/check_ncpa` 已經存在。

## LibreNMS 設定

Check Type 選 `ncpa_short`，Parameters 與 `ncpa` 完全相同：

```text
-t 'your-token' -M 'logs' -q 'name=Security,event_id=4625,logged_after=1h' -w 5 -c 20
```

已經用 `ncpa` 建過、`service_ds` 被污染的服務，改 Check Type 之後要把 `service_ds` 清成 `{}`，否則舊欄位還在。

## 輸出範例

```text
OK: Security has 0 logs, Total Count has 0 logs (Time range - last 1 hour) | 'Security'=0;5;20; 'Total Count'=0;5;20;
```

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
