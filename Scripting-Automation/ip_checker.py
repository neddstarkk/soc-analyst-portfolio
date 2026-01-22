import requests
import json
import sys

API_KEY = '86d7c6e38b52e29b6a0330f60874e516767fb2eab0f84b06af6a38e0ce6b907d435055ce1d7bee9f'
URL = 'https://api.abuseipdb.com/api/v2/check'

def get_ip_location(ip_address):
    # This API is free for non-commercial use
    response = requests.get(f"http://ip-api.com/json/{ip_address}")
    data = response.json()
    
    if data['status'] == 'success':
        return f"{data['country']} ({data['city']}) - ISP: {data['isp']}"
    else:
        return "Location Lookup Failed"

def check_ip(ip_address):
    print(f"Checking IP address: {ip_address}...")

    headers = {
        'Key': API_KEY,
        'Accept': 'application/json'
    }

    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': 90
    }

    try:
        response = requests.get(URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            abuse_confidence_score = data['data']['abuseConfidenceScore']
            total_reports = data['data']['totalReports']
            country_code = data['data']['countryCode']
            usage_type = data['data']['usageType']
            isp = data['data']['isp']
            domain = data['data']['domain']

            location_info = get_ip_location(ip_address)

            print("-" * 40)
            print(f"Abuse Confidence Score: {abuse_confidence_score}")
            print(f"Total Reports: {total_reports}")
            print(f"Country Code: {country_code}")
            print(f"Usage Type: {usage_type}")
            print(f"ISP: {isp}")
            print(f"Domain: {domain}")
            print(f"Location Info: {location_info}")

            if abuse_confidence_score > 0:
                print("\n[!] ALERT: This IP has been reported for malicious activity!")
            else:
                print("\n[!] CLEAN: No malicious reports found")
        else:
            print(f"[!] ERROR: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_ip = sys.argv[1]
        check_ip(target_ip)
    else:
        print("Usage: python ip_checker.py <IP_ADDRESS>")