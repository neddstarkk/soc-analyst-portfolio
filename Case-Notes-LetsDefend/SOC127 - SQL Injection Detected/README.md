# Case Notes - SOC 127: SQL Injection Detected

Event Time: Mar, 07, 2024, 12:51 PM

Source Address: 118.194.247.28
Destination Address: 172.16.20.12
Destination Hostname: WebServer1000

Request URL: GET /?douj=3034%20AND%201%3D1%20UNION%20ALL%20SELECT%201%2CNULL%2C%27%3Cscript%3Ealert%28%22XSS%22%29%3C%2Fscript%3E%27%2Ctable_name%20FROM%20information_schema.tables%20WHERE%202%3E1--%2F%2A%2A%2F%3B%20EXEC%20xp_cmdshell%28%27cat%20..%2F..%2F..%2Fetc%2Fpasswd%27%29%23 HTTP/1.1 200 865

## Operational Playbook

### 1. Is the alert a true positive or a false positive? 

The alert triggered signifies SQL Injection Detected. Upon inspection of the Request URL, it is observed that SQL injection was indeed attempted by the presence of UNION SELECT ALL in the request URL. 

It seems to be a true positive but lets just check the source and destination devices anyway. 

The destination server seems to be the Atlanta server while the source seems to be outside the corporate environment. Going to investigate both of these IPs in more depth. 

### 2. Data Collection

118.194.247.28 - 10/91 security vendors flagged this IP address as malicious on virustotal

big red flag already. We already determined that the traffic is coming from outside the corporate environment from the internet. 

The source IP address is coming from China. 

172.16.20.12 - Atlanta Server 
Last Login: Nov, 10, 2023, 09:23 AM

### 3. Examine HTTP Traffic

Upon examining logs, I happened upon this following log:

```
118.194.247.28 - - [07/Mar/2024:12:53:09 +0000] "GET /index.php?id=1%20AND%20EXTRACTVALUE%287321%2CCONCAT%280x5c%2C0x716b6b7671%2C%28SELECT%20%28ELT%287321%3D7321%2C1%29%29%29%2C0x71707a6a71%29%29 HTTP/1.1" 200 865 "-" "sqlmap/1.7.2#stable (https://sqlmap.org)"
```

From this, I can determine that SQLMap was used as one of the attacker's tools to conduct recon and exploitation upon our webserver. 


### 4. Decision Making Factors

Based on my observation, I am making the decision that the traffic is Malicious. The attack vector of this malicious traffic is an SQL injection as a result of my investigation. The only justification for this apart from the malicious act of a threat actor could be a planned penetration test. 

However, there are no emails about any such plans, confirming this as the action of an external threat actor. The direction of this malicious traffic is Internet -> Company Network