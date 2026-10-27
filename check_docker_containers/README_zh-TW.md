[English](README.md) | 繁體中文

# check_docker_containers v1.0

NCPA 外掛（Python 3）：透過 Docker Engine API（`/var/run/docker.sock`）檢查容器狀態。不需要 `docker` 指令或額外套件，只用標準函式庫。

## 判斷規則

| 狀況 | 結果 |
|---|---|
| 重新啟動政策是 `always`、`unless-stopped`、`on-failure`，卻沒在執行 | CRITICAL |
| 重新啟動政策是 `no` 而且已停止 | 視為已停用，略過（例如保留回復用的舊容器） |
| 健康檢查 `unhealthy` | CRITICAL |
| 健康檢查 `starting` | WARNING |
| 正在反覆重新啟動，或重新啟動次數 ≥ `--restart-warn` | WARNING |
| `--require` 指定的容器不存在 | CRITICAL |
| 連不到 Docker API | UNKNOWN |

## 安裝

```bash
sudo install -m 755 check_docker_containers.py /usr/local/ncpa/plugins/
sudo usermod -aG docker nagios
sudo systemctl restart ncpa     # 讓 nagios 的新群組生效
```

注意：**docker 群組的權限等同 root**，能存取 `docker.sock` 就能啟動特權容器。只在內部管理用、只允許監控主機連 NCPA 的環境這樣做；安全要求較高的環境，改用只開放唯讀 API（containers）的 Docker socket proxy，再用 `--socket` 指過去（proxy 要提供 Unix socket）。

## 參數

| 參數 | 預設 | 說明 |
|---|---|---|
| `--lang` | `zh-tw` | 輸出語言，`zh-tw` 或 `en` |
| `--require` | — | 必須存在的容器，逗號分隔；列在這裡的容器就算政策是 `no` 也會檢查 |
| `--exclude` | — | 不檢查的容器，逗號分隔 |
| `--restart-warn` | 5 | 重新啟動次數達到幾次算 WARNING |
| `--socket` | `/var/run/docker.sock` | Docker API 的 Unix socket |

## LibreNMS 設定

Check Type 選 `ncpa`：

```text
-t 'your-token' -M 'plugins/check_docker_containers.py' -a "--require web,db,auth"
```

## 輸出範例

```text
OK - 容器全部正常（執行中 4）; 略過已停用 web-old | running=4;;;0;4 problems=0;;;0
CRITICAL - db 沒在執行（exited）; auth 不存在; 執行中 2/4 | running=2;;;0;4 problems=2;;;0
WARNING - web 已重啟 7 次; 執行中 4/4 | running=4;;;0;4 problems=1;;;0
```

## 限制

- 容器名稱取 `Names` 的第一個
- 每個容器各呼叫一次 inspect API，容器很多時注意 NCPA 的外掛逾時（預設 59 秒）

## 作者

- Jason Cheng（Jason Tools）
- jason@jason.tools
- 部落格：https://blog.jason.tools
- GitHub：https://github.com/jasoncheng7115

## 授權

GNU Affero General Public License v3.0 或更新版本（AGPL-3.0-or-later），全文見 [LICENSE](../LICENSE)。
