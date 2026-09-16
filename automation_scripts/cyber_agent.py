import json
import requests
import os

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def ask_wormx_with_context(context_data, user_query):
    """Knowledge base ka data system prompt ke sath model ko bhejna"""
    
    # Hum model ko bata rahe hain ki pehle background text ko dhyan se padhe
    full_prompt = f"BACKGROUND KNOWLEDGE/TARGET DATA:\n{context_data}\n\nINSTRUCTION:\n{user_query}"
    
    payload = {
        "model": "KhanzadaWormX",
        "prompt": full_prompt,
        "stream": False
    }
    
    print("[*] Reading Knowledge Base and sending context to KhanzadaWormX...")
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "No response received.")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

if __name__ == "__main__":
    # Define paths
    knowledge_file = r"D:\advanced_gpt\knowledge_base\target_report.txt"
    output_file = r"D:\advanced_gpt\output_results\targeted_attack_tool.txt"
    
    # 1. Knowledge Base file ko read karna
    if os.path.exists(knowledge_file):
        with open(knowledge_file, "r", encoding="utf-8") as k_file:
            intelligence_data = k_file.read()
    else:
        print("[-] Knowledge base file not found!")
        exit()
        
    # 2. Query jo hume background data par chalani hai
    query = "Based on the target report provided, write a Python script that connects to the vulnerable internal IP and custom port, sends a raw TCP packet to exploit the weakness, and fulfills the main goal described in the report."
    
    # 3. Model se response lena
    ai_output = ask_wormx_with_context(intelligence_data, query)
    
    # 4. Result ko save karna
    print(r"[*] Writing targeted exploit to D:\advanced_gpt\output_results\...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ai_output)
        
    print(f"[+] Success! Customized tool generated based on your Knowledge Base in: {output_file}")