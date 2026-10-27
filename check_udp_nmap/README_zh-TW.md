[English](README.md) | 繁體中文

# check_udp_nmap v1.1

以 `nmap -sU` 檢查指定的 UDP 連接埠有沒有在聽，例如 SNMP 161、Syslog 514、NTP 123。UDP 沒有連線交握，一般的 TCP 檢查用不上。

原本放在 https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons ，v1.1 起在本 repo 維護。

## 需求

- `nmap`（`/usr/bin/nmap`）
- UDP 掃描要 root，所以 LibreNMS 的執行帳號要能 `sudo nmap`：

```text
librenms ALL=(root) NOPASSWD: /usr/bin/nmap
```

注意：**允許 sudo 執行 nmap 等同給 root**（nmap 可用 `--script` 執行任意 Lua）。只在 LibreNMS 主機本身受控的環境這樣做。

## 參數

| 參數 | 說明 |
|---|---|
| `-H` | 目標 IP（LibreNMS 會自動帶） |
| `-p` | UDP 連接埠 |
| `-s` | 嚴格模式：只有 `open` 算 OK，`open\|filtered` 算 CRITICAL |
| `-t` | nmap 的主機逾時秒數，預設 30 |

nmap 對 UDP 連接埠的判斷：

| nmap 狀態 | 意義 | 預設 | `-s` |
|---|---|---|---|
| `open` | 服務有回應 | OK | OK |
| `open\|filtered` | 沒有回應。Syslog、GELF 與大多數自訂的接收埠不回應空的探測封包，正常就是這個狀態 | OK | CRITICAL |
| `closed` | 收到 ICMP port unreachable，沒有程式在聽 | CRITICAL | CRITICAL |
| `filtered` | 收到其他 ICMP 錯誤 | CRITICAL | CRITICAL |

`open|filtered` 也可能是防火牆擋掉了 ICMP，所以預設模式只能確認「沒有明確關閉」。服務本身會回應的（SNMP、DNS、NTP）建議加 `-s`。

## LibreNMS 設定

放在 `/usr/lib/nagios/plugins/check_udp_nmap`，Check Type 選 `udp_nmap`：

```text
-p 161
```

## 輸出範例

```text
OK: 161/udp is listening.
OK: 514/udp is listening or filtered (nmap: open/filtered, no reply).
CRITICAL: 514/udp is not listening (closed).
CRITICAL: 161/udp did not reply (nmap: open/filtered).
UNKNOWN: No result for 161/udp on 192.168.1.30 (host down or timed out).
```

## 版本紀錄

- **v1.1**（2026/10/27）：輸出 nmap 實際判斷的狀態，`open|filtered` 不再因為字串含 `open` 被當成 `open`；新增 `-s` 嚴格模式；缺參數或 nmap 執行失敗回 UNKNOWN；`sudo -n` 避免等待密碼；主機逾時 `-t`；`-P0` 改為新寫法 `-Pn`
- **v1.0**

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
