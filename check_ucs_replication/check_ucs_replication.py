#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""UCS 網域控制站複寫狀態檢查（Nagios / NCPA 外掛）。

Version: 1.0
Author: Jason Cheng (Jason Tools) <jason@jason.tools>
https://github.com/jasoncheng7115/jt-lnms-plugins

同時檢查兩種複寫：
  1. UCS LDAP 複寫：Primary 的 notifier ID 與本機 listener 已處理的 ID 差距。
     大量 LDAP 變更時短暫落後是正常的，所以用狀態檔記錄 listener 上次前進的
     時間：落後且「多久沒有進度」超過門檻才告警。
  2. Samba AD DRS 複寫：samba-tool drs showrepl --json 的 repsFrom，
     看各分區的連續失敗次數與最後成功時間。

用法：
  check_ucs_replication.py [--lang zh-tw|en] [-w 分鐘] [-c 分鐘]
                           [--drs-warn 次數] [--drs-crit 次數] [--no-drs]

  --lang       輸出語言，zh-tw（預設）或 en
  -w / -c      LDAP 落後且沒有進度多少分鐘算 WARNING / CRITICAL（預設 10 / 30）
  --drs-warn   DRS 任一分區連續失敗幾次算 WARNING（預設 1）
  --drs-crit   DRS 任一分區連續失敗幾次算 CRITICAL（預設 3）
  --no-drs     不檢查 Samba DRS（沒裝 Samba AD 的主機用）

結束碼：0 OK、1 WARNING、2 CRITICAL、3 UNKNOWN
"""
import argparse
import json
import os
import subprocess
import sys
import time

GET_NOTIFIER_ID = "/usr/share/univention-directory-listener/get_notifier_id.py"
LISTENER_ID_FILE = "/var/lib/univention-directory-listener/notifier_id"
FAILED_LDIF = "/var/lib/univention-directory-replication/failed.ldif"
STATE_FILE = "/var/tmp/check_ucs_replication.state"
SAMBA_TOOL = "/usr/bin/samba-tool"

OK, WARNING, CRITICAL, UNKNOWN = 0, 1, 2, 3
STATUS_WORD = {OK: "OK", WARNING: "WARNING", CRITICAL: "CRITICAL", UNKNOWN: "UNKNOWN"}

MSG = {
    "zh-tw": {
        "ldap_ok": "LDAP 複寫同步（{lid}/{nid}）",
        "ldap_lag_new": "LDAP 落後 {lag} 筆（{lid}/{nid}），處理中",
        "ldap_lag": "LDAP 落後 {lag} 筆（{lid}/{nid}），已 {mins} 分鐘沒有進度",
        "ldap_ahead": "LDAP listener ID 大於 notifier ID（{lid}/{nid}），請檢查",
        "failed_ldif": "有複寫失敗的變更待處理（failed.ldif）",
        "nid_err": "無法取得 Primary 的 notifier ID：{err}",
        "lid_err": "無法讀取本機 listener ID：{err}",
        "drs_ok": "Samba DRS 正常（{n} 個分區）",
        "drs_fail": "Samba DRS {nc} 從 {dsa} 連續失敗 {cnt} 次（{msg}）",
        "drs_err": "無法取得 Samba DRS 狀態：{err}",
        "drs_skip": "略過 Samba DRS",
    },
    "en": {
        "ldap_ok": "LDAP replication in sync ({lid}/{nid})",
        "ldap_lag_new": "LDAP behind by {lag} ({lid}/{nid}), processing",
        "ldap_lag": "LDAP behind by {lag} ({lid}/{nid}), no progress for {mins} min",
        "ldap_ahead": "LDAP listener ID ahead of notifier ID ({lid}/{nid}), check needed",
        "failed_ldif": "Failed replication changes pending (failed.ldif)",
        "nid_err": "Cannot get notifier ID from Primary: {err}",
        "lid_err": "Cannot read local listener ID: {err}",
        "drs_ok": "Samba DRS OK ({n} partitions)",
        "drs_fail": "Samba DRS {nc} from {dsa}: {cnt} consecutive failure(s) ({msg})",
        "drs_err": "Cannot get Samba DRS status: {err}",
        "drs_skip": "Samba DRS skipped",
    },
}


def run(cmd, timeout=30):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout).strip().splitlines()[-1] if (p.stderr or p.stdout).strip() else "rc=%d" % p.returncode)
    return p.stdout


def short_nc(dn):
    """DC=DomainDnsZones,DC=example,DC=com -> DomainDnsZones；網域本身 -> Domain"""
    first = dn.split(",")[0].split("=", 1)[-1]
    return "Domain" if dn.upper().startswith("DC=") and not dn.upper().startswith(("DC=DOMAINDNSZONES", "DC=FORESTDNSZONES")) else first


def check_ldap(args, t):
    """回傳 (狀態, 訊息, perfdata)"""
    try:
        nid = int(run([GET_NOTIFIER_ID]).strip())
    except Exception as e:  # noqa: BLE001
        return CRITICAL, t["nid_err"].format(err=e), ""
    try:
        with open(LISTENER_ID_FILE) as f:
            lid = int(f.read().strip())
    except Exception as e:  # noqa: BLE001
        return CRITICAL, t["lid_err"].format(err=e), ""

    lag = nid - lid
    perf = "ldap_lag=%d;;;0" % max(lag, 0)
    now = time.time()

    # 狀態檔只記「開始落後的時間」；追上就清掉
    state = {}
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
    except Exception:  # noqa: BLE001
        pass

    if os.path.exists(FAILED_LDIF) and os.path.getsize(FAILED_LDIF) > 0:
        return CRITICAL, t["failed_ldif"], perf

    if lag < 0:
        return WARNING, t["ldap_ahead"].format(lid=lid, nid=nid), perf

    if lag == 0:
        if state:
            try:
                os.remove(STATE_FILE)
            except OSError:
                pass
        return OK, t["ldap_ok"].format(lid=lid, nid=nid), perf

    # 落後中：listener ID 有前進就代表還在消化，從現在重新計時；
    # 沒前進才沿用上次的起算時間，所以「分鐘數」= listener 卡住多久
    since = state["since"] if state.get("lid") == lid and "since" in state else now
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({"since": since, "lid": lid}, f)
    except OSError:
        pass

    mins = int((now - since) // 60)
    if mins == 0:
        return OK, t["ldap_lag_new"].format(lag=lag, lid=lid, nid=nid), perf
    msg = t["ldap_lag"].format(lag=lag, lid=lid, nid=nid, mins=mins)
    if mins >= args.critical:
        return CRITICAL, msg, perf
    if mins >= args.warning:
        return WARNING, msg, perf
    return OK, msg, perf


def check_drs(args, t):
    if args.no_drs:
        return OK, t["drs_skip"], ""
    try:
        cmd = [SAMBA_TOOL, "drs", "showrepl", "--json"]
        if os.geteuid() != 0:
            cmd = ["sudo", "-n"] + cmd
        data = json.loads(run(cmd, timeout=60))
    except Exception as e:  # noqa: BLE001
        return CRITICAL, t["drs_err"].format(err=e), ""

    worst, msgs, total_fail = OK, [], 0
    reps = data.get("repsFrom", [])
    for r in reps:
        cnt = int(r.get("consecutive failures", 0))
        total_fail += cnt
        if cnt <= 0:
            continue
        st = CRITICAL if cnt >= args.drs_crit else (WARNING if cnt >= args.drs_warn else OK)
        if st == OK:
            continue
        worst = max(worst, st)
        dsa = r.get("DSA", "?").split("\\")[-1]
        msgs.append(t["drs_fail"].format(nc=short_nc(r.get("NC dn", "?")), dsa=dsa, cnt=cnt,
                                         msg=r.get("last attempt message", "")))
    perf = "drs_failures=%d;%d;%d;0" % (total_fail, args.drs_warn, args.drs_crit)
    if worst == OK:
        return OK, t["drs_ok"].format(n=len(reps)), perf
    return worst, "; ".join(msgs), perf


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--lang", default="zh-tw", type=str.lower, choices=["zh-tw", "en"])
    ap.add_argument("-w", "--warning", type=int, default=10, help="LDAP lag minutes for WARNING")
    ap.add_argument("-c", "--critical", type=int, default=30, help="LDAP lag minutes for CRITICAL")
    ap.add_argument("--drs-warn", type=int, default=1)
    ap.add_argument("--drs-crit", type=int, default=3)
    ap.add_argument("--no-drs", action="store_true")
    try:
        args = ap.parse_args()
    except SystemExit:
        sys.exit(UNKNOWN)
    t = MSG[args.lang]

    try:
        s1, m1, p1 = check_ldap(args, t)
        s2, m2, p2 = check_drs(args, t)
    except Exception as e:  # noqa: BLE001
        print("UNKNOWN - %s" % e)
        sys.exit(UNKNOWN)

    status = max(s1, s2)
    perf = " ".join(p for p in (p1, p2) if p)
    print("%s - %s; %s | %s" % (STATUS_WORD[status], m1, m2, perf))
    sys.exit(status)


if __name__ == "__main__":
    main()
