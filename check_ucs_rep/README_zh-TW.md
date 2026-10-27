[English](README.md) | 繁體中文

# check_ucs_rep v1.1

NCPA 外掛（Python 3）：檢查 Univention Corporate Server（UCS）網域控制站的複寫狀態。

- **UCS LDAP 複寫**：比較 Primary 的 notifier ID 與本機 listener 已處理的 ID。大量 LDAP 變更時短暫落後是正常的，所以用狀態檔 `/var/tmp/check_ucs_rep.state` 記錄 listener 卡住的起始時間，**落後而且多久沒有進度**超過門檻才告警；`failed.ldif` 有內容直接 CRITICAL
- **Samba AD DRS 複寫**：`samba-tool drs showrepl --json` 的 repsFrom，看各分區的連續失敗次數

## 需求

- UCS（已在 UCS 5.2 使用）
- 系統的 `python3`，只用標準函式庫

## 安裝

```bash
sudo install -m 755 check_ucs_rep.py /usr/local/ncpa/plugins/
sudo install -m 440 sudoers-ncpa-ucs-rep /etc/sudoers.d/ncpa-ucs-rep
sudo visudo -c
```

`samba-tool drs showrepl` 要 root 才能執行，而 NCPA 以 `nagios` 身分執行外掛。sudoers 只開放 `samba-tool drs showrepl --json` 這一行（寫到完整參數，換參數就不行），外掛不是 root 時會自動改用 `sudo -n` 呼叫。不要用 NCPA 的 `run_with_sudo`，那會讓整支外掛以 root 執行。

沒有裝 Samba AD 的節點加 `--no-drs`，就不需要 sudoers。

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `--lang` | `zh-tw` | 輸出語言，`zh-tw` 或 `en` |
| `-w` / `-c` | 10 / 30 | LDAP 落後且沒有進度幾分鐘算 WARNING / CRITICAL |
| `--drs-warn` | 1 | DRS 任一分區連續失敗幾次算 WARNING |
| `--drs-crit` | 3 | DRS 任一分區連續失敗幾次算 CRITICAL |
| `--no-drs` | — | 不檢查 Samba DRS |

## LibreNMS 設定

Check Type 選 `ncpa`：

```text
-t 'your-token' -M 'plugins/check_ucs_rep.py' -a "--lang zh-tw"
```

## 輸出範例

```text
OK - LDAP 複寫同步（1234/1234）; Samba DRS 正常（5 個分區） | ldap_lag=0;;;0 drs_failures=0;1;3;0
WARNING - LDAP 落後 52 筆（1182/1234），已 12 分鐘沒有進度; Samba DRS 正常（5 個分區） | ldap_lag=52;;;0 drs_failures=0;1;3;0
CRITICAL - LDAP 複寫同步（1234/1234）; Samba DRS DomainDnsZones 從 DC01 連續失敗 3 次（...） | ldap_lag=0;;;0 drs_failures=3;1;3;0
```

## 版本紀錄

- **v1.1**（2026/10/27）：改名為 `check_ucs_rep.py`（原名 `check_ucs_replication.py`），功能不變；狀態檔改名，第一次執行時會自動搬移舊檔。升級時把外掛目錄裡的舊檔移走，LibreNMS Parameters 的 `-M` 改成新檔名；已經建立的 sudoers 檔不用改
- **v1.0**（2026/10/23）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
