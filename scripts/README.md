# Scripts
Utility scripts built to automate repetitive SOC analyst tasks. Each script targets a specific investigative workflow.


## ip_checker.py

**Purpose**: Automates IP reputation lookup during alert triage by querying AbuseIPDB and ip-api.com in a single run.

### What it does:

* Queries AbuseIPDB for abuse confidence score, total reports, ISP, usage type, and domain
* Enriches the result with geolocation data (country, city, ISP) via ip-api.com
* Flags IPs with any abuse reports with a clear [!] ALERT output

**Use case**: During alert triage, instead of manually checking an IP across two platforms, run this once and get a consolidated verdict in seconds.

**Usage:**

```
python ip_checker.py <IP_ADDRESS>
```

**Dependencies:** ```requests``` - install via ```pip install requests```
**Note:** Replace the ```API_KEY``` value with your own AbuseIPDB key before use. The hardcoded key in this file has been rotated.

## log_parser.py

**Purpose**: Scans web server access logs for SQL injection attempts using keyword signature matching.

### What it does:

* Detects common SQLi patterns: UNION, SELECT, ' OR ', '1'='1, DROP TABLE, INSERT INTO
* Extracts and prints the source IP, alert type, and raw log line for each hit
* Designed to run against any standard Apache/Nginx access log format

**Use case:** Quick first-pass triage on access logs when a WAF alert fires or during an investigation into suspicious web traffic — surfaces attacker IPs without loading the full log into a SIEM.
**Usage:**
```
python log_parser.py
```

Point it at your own log file by modifying the ```parse_log()``` call at the bottom, or extend it to accept a file path argument via ```sys.argv```.
**Dependencies:** None — standard library only.

> *These scripts are built for defensive, educational use in SOC and detection workflows.*