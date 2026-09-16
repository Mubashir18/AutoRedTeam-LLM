import os
from datasets import load_dataset

print("[*] Initializing Live Cyber Threat Intelligence Downloader...")

# Target folder configuration
kb_directory = r"D:\advanced_gpt\knowledge_base"
output_file_path = os.path.join(kb_directory, "cve_threat_intel.txt")

try:
    print("[*] Connecting to Hugging Face Threat Intel Dataset...")
    # Loading the active and valid threat intelligence dataset
    dataset = load_dataset("reloading0101/threat-intelligence-dataset", split="train", streaming=True)
    
    iterator = iter(dataset)
    threat_profiles = []
    
    print("[*] Fetching and parsing raw threat campaign intelligence logs...")
    # Extracting top 15 highly complex technical threat campaigns
    for i in range(15):
        try:
            record = next(iterator)
            # Formatting the data structurally
            campaign_name = record.get("Campaign", "Unknown Campaign")
            actor = record.get("Threat Actor", "Unknown Actor")
            analysis = record.get("Campaign Analysis", str(record))
            
            profile = f"--- THREAT INTEL RECORD #{i+1} ---\nCAMPAIGN: {campaign_name}\nACTOR: {actor}\nANALYSIS:\n{analysis}\n"
            threat_profiles.append(profile)
        except StopIteration:
            break

    print(f"[*] Compiling data and exporting to: {output_file_path}")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(threat_profiles))
        
    print("[+] Success! Live cyber threat intelligence has been successfully injected into your Knowledge Base.")

except Exception as e:
    print(f"[-] Data fetching failed: {str(e)}")