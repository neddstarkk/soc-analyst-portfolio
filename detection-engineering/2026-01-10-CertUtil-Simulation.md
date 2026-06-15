# Purple Team Report: CertUtil Download (T1105)
**Date:** 2026-01-10
**Technique:** MITRE T1105 (Ingress Tool Transfer)
**Test Status:** 🛡️ BLOCKED (Prevention Success)

## 1. Simulation Details
**Command Executed:**
`certutil.exe -urlcache -split -f https://www.google.com/robots.txt %TEMP%\atomic_test.txt`

**Intent:**
Mimic the behavior of Volt Typhoon actors who use `certutil` to download payloads (like web shells) bypassing standard browser controls.

## 2. Prevention Evidence
**Outcome:** The command failed with "Access is denied."
**Security Control:** Microsoft Defender Antivirus (Real-time Protection).

**Defender Logs (Protection History):**
* **Action:** Blocked
* **Threat Name:** Trojan:Win32/Ceprolad.A
* **Target Process:** `certutil.exe`

## 3. Analysis & Recommendation
**Security Posture:** **Strong.**
The system correctly identified the abuse of a legitimate binary (`certutil`) for network connections. No manual intervention was required.

**Adversary Perspective:**
Since `certutil` is blocked, an attacker would likely pivot to alternative LOLBins such as:
1.  `bitsadmin.exe`
2.  `curl.exe` (if Windows 10/11)
3.  PowerShell `Invoke-WebRequest`

**Recommendation:**
No changes needed for CertUtil. Recommend testing `bitsadmin` next to see if coverage is consistent across other binaries.