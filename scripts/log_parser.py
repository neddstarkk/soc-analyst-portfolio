import sys

def parse_log(file_path):
    # Define our SQL Injection signatures
    # Note: ' OR ' with spaces reduces false positives compared to just 'OR'
    keywords = {"UNION", "SELECT", "' OR '", "'1'='1", "DROP TABLE", "INSERT INTO"}

    print(f"[*] Scanning {file_path} for SQL Injection attempts...")
    print("-" * 50)

    try:
        with open(file_path, "r") as f:
            for line in f:
                # Check if any keyword exists in the line
                if any(keyword in line for keyword in keywords):
                    # Extract the IP (The first chunk of text before the first space)
                    attacker_ip = line.split(' ')[0]
                    
                    print(f"[!] ALERT: SQL Injection Detected")
                    print(f"    Source IP: {attacker_ip}")
                    print(f"    Raw Log:   {line.strip()}")
                    print("-" * 50)
                    
    except FileNotFoundError:
        print(f"[X] Error: The file '{file_path}' was not found.")

if __name__ == "__main__":
    parse_log("dummy_access.log")