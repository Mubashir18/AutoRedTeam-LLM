import os
from datasets import load_dataset

print("[*] Initializing High-Level Cyber Data Aggregator...")

# Target output file path
kb_directory = r"D:\advanced_gpt\knowledge_base"
intel_output = os.path.join(kb_directory, "darkweb_fraud_intel.txt")

try:
    print("[*] Accessing Cyber Operations & Offensive Knowledge Base...")
    # Loading a massive verified cybersecurity analysis dataset
    dataset = load_dataset("AlicanKiraz0/Cybersecurity-Dataset-Fenrir-v2.1", split="train", streaming=True)
    
    iterator = iter(dataset)
    compiled_data = []
    
    print("[*] Extracting high-risk attack matrices and system weaknesses...")
    # Extracting top 30 highly descriptive structural attack profiles
    for i in range(30):
        try:
            record = next(iterator)
            # Standard instruction-response format extraction
            instruction = record.get("instruction", "Offensive Objective")
            response_content = record.get("response", str(record))
            
            log_entry = f"--- CYBER EXPLOIT VECTOR #{i+1} ---\nOBJECTIVE: {instruction}\nTECHNICAL ANALYSIS:\n{response_content}\n"
            compiled_data.append(log_entry)
        except StopIteration:
            break

    print(f"[*] Writing analytical threat assets to: {intel_output}")
    with open(intel_output, "w", encoding="utf-8") as f:
        f.write("\n".join(compiled_data))
        
    print("[+] Success! Advanced critical datasets are successfully compiled in your Knowledge Base.")

except Exception as e:
    print(f"[-] Data aggregation encountered an error: {str(e)}")