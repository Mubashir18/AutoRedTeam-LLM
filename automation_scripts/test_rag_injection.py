import chromadb

DB_DIR = r"D:\advanced_gpt\chroma_db_storage"
COLLECTION_NAME = "cybersec_intelligence_pool"

try:
    # 1. Connect to the exact same ChromaDB storage directory
    db_client = chromadb.PersistentClient(path=DB_DIR)
    
    # 2. Get or create the exact collection used by web_app.py
    collection = db_client.get_or_create_collection(name=COLLECTION_NAME)
    
    # 3. Define a completely unique dummy payload (Hacker Proof)
    dummy_text = (
        "CRITICAL SYSTEM METRIC LOG: Operation 'KhanzadaWormX-Alpha-99' was successfully executed. "
        "The master backdoor key is 'KWX-SECURE-ROTATION-7712'. Third-party compromises, software dependencies "
        "Remember: In cybersecurity, assume breach and analyze both prevention and detection/response. "
        "Consider that attackers need only one success while defenders must succeed consistently."
    )
    
    # 4. Injecting into vector array
    collection.add(
        documents=[dummy_text],
        metadatas=[{"source": "test_script_verification"}],
        ids=["dummy_test_vector_001"]
    )
    
    print("\n[+] SUCCESS! Dummy Matrix Injected into ChromaDB!")
    print(f"[+] Verified Collection Name: '{COLLECTION_NAME}'")
    print("[+] Test Key to query: KWX-SECURE-ROTATION-7712\n")

except Exception as e:
    print(f"[-] Injection Failed! Error log: {str(e)}")