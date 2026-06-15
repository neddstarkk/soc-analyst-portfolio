Incident Report: Big Fish in a Little Pond
**Date:** 2025-12-29
**Analyst:** Nedheesh Hasija
**Evidence:** 2024-09-04-traffic-analysis-exercise.pcap

## 1. Executive Summary
On 2024-09-04 at 17:35 UTC, a Windows host used by Andrew Fletcher showed signs of being infected with a Koi stealer malware. 

## 2. Victim Details
* **IP Address:** 172.17.0.99
* **MAC Address:** 183DA2B68DC4
* **Hostname:** DESKTOP-RNVO9AT
* **User Account:** afletcher
* **Name:** Andrew Fletcher

## 3. Technical Analysis
**Infection Vector:**
The PCAP does not indicate how the host was infected. If the windows host is a laptop, it is possible the corruption happened outside corporate networks.

**Alert Name:**  `ETPRO TROJAN Win32/Koi Stealer CnC Checkin (POST) M2`

However, we did find some http traffic to `www[.]bellantonicioccolato[.]it`. On searching google for this domain plus the word malware, we find sandbox analysis and other entries indicating malicious activity on this website associated with KoiLoader / KoiStealer malware. 

## 4. Indicators of Compromise (IOCs)
| Type | Value | Description |
| :--- | :--- | :--- |
| **IP** | `79[.]124[.]78[.]197` | IP associated with alert
| **URL** | `POST/index.php` / `POST/foots.php` | URLs generating the alert |