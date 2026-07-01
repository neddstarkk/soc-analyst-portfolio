# Blue Team Report: DNS Tunneling and C2 Communication
**Date:** 2026-07-01
**Technique:** T1071.004 (Application Layer Protocol: DNS)

## Executive Summary

DNS is a protocol that resolves domain names to their corresponding IP addresses. Without the lookup services that this provides, it would be impossible to find anything on the internet. As such it is some of the most trusted traffic on the internet. However, since a domain name can be anything, there are very few restrictions that can be put on DNS traffic by a firewall. 

DNS tunneling takes advantage of this fact by using DNS commands to either send messages to malware via inbound DNS requests or by extracting sensitive files using outbound DNS requests. These requests are designed to go to attacker-controlled DNS servers, ensuring that they can receive and respond to requests in the corresponding replies. 

DNS tunneling attacks are simple to perform and numerous DNS tunneling toolkits exist. This makes it possible for even unsophisticated attackers to use this technique to sneak data past an organization's defenses. 

## What Does This Traffic Look Like

* **High-Entropy Subdomains:** Domain and subdomain strings appear as random, chaotic characters (e.g. ```dGhpcy1pcy1hLXRlc3Q=.attacker.com```). This randomness represents base32 or base64 encoded payloads
* **Unusually Long Domain Labels:** Attackers tend to push the limits of DNS specifications by packing maximum characters into the hostname and subdomain fields to send as much data as possible per packet
* **High Frequency & Volume:** A single compromised host will make a massive volume of continuous requests to a single domain name within a short amount of time
* **Uncommon DNS Record Types:** Tunneling traffic frequently utilizes non-standard or overly large resource records, such as TXT, NULL, MX, or CNAME, to pass larger data chunks than standard A (IPv4) queries allow

## How to Defend Against It

### Detection Techniques

* Payload Analysis: Inspect content of DNS requests and responses. Look for long subdomains, unusual query and record types, and non standard character sets
* Traffic Analysis: Evaluate volume and frequency of DNS requests. Tunneling generates heavy, persistent traffic because each query hold a small amount of data
* Domain Reputation: Check requested domain against threat intelligence databases to block known malicious or newly observed domains instantly
* Machine Learning: Establish a baseline of normal DNS behaviour using AI and ML. Then trigger alerts for anomalies like beaconing, spikes in data requests, or connections to suspicious top-level domains (TLD)

### Protection Techniques

* Enforce Internal Resolvers: Require all devices on the network to send DNS queries exclusively to designated, monitored internal DNS servers.
* Deploy DNS Firewalls: Utilize DNS firewalls and Response Policy Zones (RPZs) to intercept, filter, and automatically drop malicious DNS requests and responses
* Rate Limiting: Configure internal DNS resolvers to enforce strict limits on the size of DNS payloads and the number of queries a single client can make per second. 
* Block High-Risk TLDs: Restrict access to or closely monitor specific geographic locations and high-risk domain extensions often associated with malicious activity