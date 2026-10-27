[English](README.md) | 繁體中文

# check_pve_cephosd v1.1

檢查 Proxmox VE 指定節點上的 Ceph OSD 狀態：以 API Token 呼叫 `GET /api2/json/nodes/<節點>/ceph/osd`，找出該節點底下狀態不是 `up` 的 OSD。

原本放在 https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons ，v1.1 起在本 repo 維護。

## 需求

Python 3、`requests`、`urllib3`（Debian/Ubuntu：`apt install python3-requests`）。

PVE 端建立唯讀的 API Token，例如帳號 `monitoring@pve`、Token ID `mon`，給 `PVEAuditor` 角色。

## 參數

| 參數 | 說明 |
|---|---|
| `-H` | PVE 主機（LibreNMS 會自動帶；連接埠固定 8006） |
| `--node_name` | 要檢查的節點名稱 |
| `--user` | 帳號＠realm |
| `--token_id` / `--token_secret` | API Token |
| `-c` | down 的 OSD 達到幾個算 CRITICAL；1 個以上但未達門檻是 WARNING |
| `-d` | 除錯：印出該節點所有 OSD 的 JSON |

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_pve_cephosd`，Check Type 選 `pve_cephosd`，每個節點一筆：

```text
--node_name pve01 --user monitoring@pve --token_id mon --token_secret 'your-token-secret' -c 1
```

## 輸出範例

```text
OK - All 4 OSDs are up | 'osd_down'=0;;1;0 'osd_total'=4;;;0
CRITICAL - 1 OSD(s) (osd.3) are down | 'osd_down'=1;;1;0 'osd_total'=4;;;0
OK - No OSDs found under node pve04 | 'osd_down'=0;;1;0 'osd_total'=0;;;0
```

## 注意事項

- `-c 1` 時不會出現 WARNING（down 1 個就是 CRITICAL）
- 不驗證 PVE 的 TLS 憑證

## 版本紀錄

- **v1.1**（2026/10/27）：加上效能資料（down 與總數）；OK 訊息顯示 OSD 數量，節點底下沒有 OSD 時另外註明；API 逾時 30 秒；說明文字的範例檔名修正
- **v1.0**（2024/03/01）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
