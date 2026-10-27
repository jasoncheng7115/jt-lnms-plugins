# SPDX-License-Identifier: AGPL-3.0-or-later
# check_files.ps1 v1.0 : NCPA plugin, checks that a file/folder exists and how many items it holds
# Author: Jason Cheng (Jason Tools) <jason@jason.tools>
# https://github.com/jasoncheng7115/jt-lnms-plugins
# Exit codes follow Nagios: 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN
param(
    [Parameter(Mandatory = $true)][string]$Path,  # file or folder
    [string]$Filter = '*',                         # wildcard used for counting, e.g. *.bak
    [int]$MinCount = -1,                           # CRITICAL when fewer items than this
    [int]$MaxCount = -1,                           # CRITICAL when more items than this
    [int]$MaxAgeHours = -1,                        # CRITICAL when the newest item is older than this
    [switch]$Recurse                               # include subfolders when counting
)

try {
    if (-not (Test-Path -LiteralPath $Path)) {
        Write-Output "CRITICAL: $Path not found"
        exit 2
    }

    # Only an existence check
    if ($MinCount -lt 0 -and $MaxCount -lt 0 -and $MaxAgeHours -lt 0) {
        Write-Output "OK: $Path exists"
        exit 0
    }

    $items = @(Get-ChildItem -LiteralPath $Path -Filter $Filter -File -Recurse:$Recurse -ErrorAction Stop)
    $count = $items.Count
    $perf  = "| 'count'=$count;;;"
    $problems = @()

    if ($MinCount -ge 0 -and $count -lt $MinCount) { $problems += "expected at least $MinCount" }
    if ($MaxCount -ge 0 -and $count -gt $MaxCount) { $problems += "expected at most $MaxCount" }
    if ($MaxAgeHours -ge 0) {
        if ($count -eq 0) {
            $problems += "no file to check age"
        } else {
            $newest = ($items | Sort-Object LastWriteTime -Descending | Select-Object -First 1)
            $age = [math]::Round(((Get-Date) - $newest.LastWriteTime).TotalHours, 1)
            if ($age -gt $MaxAgeHours) { $problems += "newest file $($newest.Name) is $age hours old" }
        }
    }

    if ($problems.Count -gt 0) {
        Write-Output "CRITICAL: $count file(s) matching $Filter in $Path, $($problems -join ', ') $perf"
        exit 2
    }
    Write-Output "OK: $count file(s) matching $Filter in $Path $perf"
    exit 0
}
catch {
    Write-Output "UNKNOWN: $($_.Exception.Message)"
    exit 3
}
