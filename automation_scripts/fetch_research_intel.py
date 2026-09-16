import os
import requests
from datasets import load_dataset

print("[*] Initializing Academic & Instruction Threat Intel Downloader...")

# Target output files setup
kb_directory = r"D:\advanced_gpt\knowledge_base"
instruction_output = os.path.join(kb_directory, "instruction_tuning_intel.txt")
advbench_output = os.path.join(kb_directory, "safety_bypass_intel.txt")

# 1. Fetching Trendyol Cybersecurity Instruction Dataset Sample
try:
    print("[*] Connecting to Trendyol Cybersecurity Instruction Dataset...")
    # Using the official open-access identifier path
    dataset = load_dataset("Trendyol/Cybersecurity-Instruction-Tuning-Dataset", split="train", streaming=True)
    iterator = iter(dataset)
    compiled_instructions = []
    
    print("[*] Parsing structured security instruction pairs...")
    for i in range(30):
        try:
            record = next(iterator)
            q = record.get("instruction", record.get("prompt", "Security Query"))
            a = record.get("output", record.get("response", "Analysis"))
            compiled_instructions.append(f"--- INSTRUCTION PAIR #{i+1} ---\nQ: {q}\nA: {a}\n")
        except StopIteration:
            break
            
    with open(instruction_output, "w", encoding="utf-8") as f:
        f.write("\n".join(compiled_instructions))
    print(f"[+] Success! Trendyol cybersecurity data stored in: {instruction_output}")
except Exception as e:
    print(f"[-] Trendyol dataset download encountered an issue: {str(e)}")

# 2. Fetching AdvBench Prompts (Safety Benchmarks) from Open Repository
try:
    print("[*] Connecting to AdvBench Raw Asset Repository...")
    # Direct raw GitHub URL for safety research baseline text
    advbench_url = "https://raw.githubusercontent.com/llm-attacks/llm-attacks/main/data/advbench/harmful_behaviors.csv"
    response = requests.get(advbench_url, timeout=15)
    
    if response.status_code == 200:
        with open(advbench_output, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[+] Success! AdvBench safety baselines stored in: {advbench_output}")
    else:
        print(f"[-] AdvBench retrieval failed with HTTP status: {response.status_code}")
except Exception as e:
    print(f"[-] AdvBench automation encountered an issue: {str(e)}")