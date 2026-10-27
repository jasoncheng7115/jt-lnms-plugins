[English](README.md) | 繁體中文

# jt-lnms-plugins

自行開發的 LibreNMS / Nagios 相容監控外掛集中處。每支外掛一個資料夾，資料夾名稱就是外掛名稱，裡面放外掛本體與 `README.md`（用途、安裝位置、參數、輸出範例、LibreNMS 設定方式）。

## 外掛清單

| 外掛 | 版本 | 執行位置 | 平台 | 用途 |
|---|---|---|---|---|
| [check_ncpa_short](check_ncpa_short/) | v1.0 | LibreNMS 主機 | bash | 包裝 `check_ncpa`，只保留第一行，避免 NCPA `logs` 的長輸出被當成效能資料 |
| [check_files](check_files/) | v1.0 | 受監測主機（NCPA） | Windows PowerShell | 檔案/資料夾是否存在、數量上下限、最新檔案的時數 |
| [check_file_count](check_file_count/) | v1.0 | 受監測主機（NCPA） | Windows CMD | 資料夾內有檔案就 CRITICAL（待處理佇列應為空） |
| [check_ucs_rep](check_ucs_rep/) | v1.1 | 受監測主機（NCPA） | UCS，Python 3 | UCS LDAP 複寫進度＋Samba AD DRS 複寫失敗次數 |
| [check_docker](check_docker/) | v1.1 | 受監測主機（NCPA） | Linux，Python 3 | 依重新啟動政策與健康檢查判斷容器狀態 |
| [check_graylog_if](check_graylog_if/) | v1.2 | LibreNMS 主機 | bash | Graylog 最近 5 分鐘的索引失敗 |
| [check_graylog_journal](check_graylog_journal/) | v1.1 | LibreNMS 主機 | bash | Graylog Journal 使用率 |
| [check_pmg_queue](check_pmg_queue/) | v1.0 | LibreNMS 主機 | Python 3 | Proxmox Mail Gateway 的 Postfix 佇列筆數 |
| [check_pve_cephosd](check_pve_cephosd/) | v1.1 | LibreNMS 主機 | Python 3 | Proxmox VE 節點上 down 的 Ceph OSD |
| [check_udp_nmap](check_udp_nmap/) | v1.1 | LibreNMS 主機 | bash＋nmap | UDP 連接埠是否在聽 |
| [check_diff_webhtml](check_diff_webhtml/) | v1.1 | LibreNMS 主機 | bash | 網頁內容是否被改動（已由 check_webdiff 取代） |
| [check_extip](check_extip/) | v1.0 | LibreNMS 主機 | Python 3 | 對外 IP 是否變更：多個服務投票、CIDR、DDNS 主機名稱、備援線路、IPv6（取代 check_ext_ip） |
| [check_webdiff](check_webdiff/) | v1.0 | LibreNMS 主機 | Python 3 | 網頁竄改偵測：排除動態內容、連抓兩次濾掉亂數、外部主機追蹤、必須/不得出現的文字（取代 check_diff_webhtml） |
| [check_ollama](check_ollama/) | v1.0 | LibreNMS 主機 | Python 3 | Ollama 已載入的模型、VRAM、卸載倒數 |
| [check_strata](check_strata/) | v1.0 | LibreNMS 主機 | Python 3 | Strata LLM 推論 API 狀態、排隊數、上一筆請求效能 |
| [check_comfyui](check_comfyui/) | v1.1 | LibreNMS 主機 | Python 3 | ComfyUI 狀態、使用的模型、VRAM、排隊數、上一張圖 |
| [check_pyhs](check_pyhs/) | v1.1 | LibreNMS 主機 | Python 3 | TP-Link Kasa 6 孔智慧延長線各插座用電 |

check_graylog_*、check_pmg_queue、check_pve_cephosd、check_udp_nmap、check_diff_webhtml 原本放在 https://github.com/jasoncheng7115/it-scripts/tree/master/nagios_plugons ；同一處的 check_ext_ip 由重新撰寫的 check_extip 取代。

相關文章：

- LibreNMS 以 NCPA 監測 Windows 11：https://blog.jason.tools/2026/10/librenms-ncpa-windows.html
- LibreNMS 以 NCPA 監測 Linux 主機：https://blog.jason.tools/2026/10/librenms-ncpa-linux.html

## 共通慣例

- **結束碼**依 Nagios 慣例：0 OK、1 WARNING、2 CRITICAL、3 UNKNOWN
- **輸出一行**：`狀態 - 訊息 | 效能資料`。LibreNMS 會把 `|` 之後解析成效能資料存進 RRD/InfluxDB，所以 `|` 之後只能放 `'label'=值;warn;crit;min;max` 格式，不要在後面接說明文字
- **NCPA 外掛目錄**：Linux `/usr/local/ncpa/plugins/`、Windows `C:\Program Files\Nagios\NCPA\plugins\`。NCPA 依副檔名決定執行方式（`.py` 用系統的 `python3`、`.ps1` 用 `powershell -ExecutionPolicy Bypass -File`），外掛逾時預設 59 秒（`plugin_timeout`）
- **NCPA 的執行身分**：Linux 是 `nagios`（`ncpa.cfg` 的 `[general]` `uid/gid`），Windows 是 LocalSystem。需要 root 的指令用 sudoers 只開放那一行，外掛內部 `sudo -n` 呼叫，不要用 `run_with_sudo` 讓整支外掛取得 root
- **LibreNMS 端**呼叫 NCPA 外掛：Check Type 選 `ncpa`，Parameters 寫 `-t 'your-token' -M 'plugins/<檔名>' -a '<外掛參數>'`，不要寫 `-H`（LibreNMS 會自己帶）
- **LibreNMS 主機上的外掛**放 `/usr/lib/nagios/plugins/`，檔名要以 `check_` 開頭，Check Type 會顯示成去掉前綴的名稱
- 有語系的外掛提供 `--lang zh-tw|en`，預設 zh-tw

## 新增外掛

1. 建一個與外掛同名的資料夾（不含副檔名），放外掛本體
2. 寫 `README.md`（英文，預設）與 `README_zh-TW.md`（繁體中文）：標題帶版本號，內容有用途、需求、安裝位置與權限、參數、輸出範例、LibreNMS Parameters 範例、已知問題、作者、授權
3. 範例一律用虛構資料（`example.com`、`192.168.1.x`、`your-token`），不要放實際主機名稱、IP、容器名稱、網域
4. 外掛開頭加 `SPDX-License-Identifier: AGPL-3.0-or-later`
5. 更新本頁與英文版的外掛清單（含版本）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](LICENSE)。
