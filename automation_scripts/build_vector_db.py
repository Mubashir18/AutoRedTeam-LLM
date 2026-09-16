import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("[*] Initializing Master Vector Database Pipeline...")

# Configuration of strict D-Drive storage paths
kb_dir = r"D:\advanced_gpt\knowledge_base"
db_dir = r"D:\advanced_gpt\chroma_db_storage"

# Initialize Persistent Local ChromaDB Client
db_client = chromadb.PersistentClient(path=db_dir)

# Create or get a unified collection for cybersecurity assets
# Using a baseline distance metric (cosine similarity) for analytical searches
try:
    collection = db_client.get_or_create_collection(name="cybersec_intelligence_pool")
    print("[+] Successfully connected to Persistent ChromaDB Collection.")
except Exception as e:
    print(f"[-] Database collection initialization failed: {str(e)}")
    exit()

# Text Splitter configuration to break heavy documents into 700 character chunks with 100 character overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)

def ingest_file_to_vector_db(file_name, source_tag):
    file_path = os.path.join(kb_dir, file_name)
    if not os.path.exists(file_path):
        print(f"[-] Source file missing: {file_name}. Skipping ingestion.")
        return
        
    print(f"[*] Reading and chunking telemetry data from: {file_name}...")
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    # Splitting into lightweight logical chunks
    chunks = text_splitter.split_text(raw_text)
    print(f"[+] Total chunks generated from {file_name}: {len(chunks)}")
    
    # Ingesting documents programmatically into ChromaDB disk storage
    print(f"[*] Indexing chunks into ChromaDB under metadata source: '{source_tag}'...")
    for idx, chunk in enumerate(chunks):
        chunk_id = f"{source_tag}_chunk_{idx}"
        collection.add(
            documents=[chunk],
            metadatas=[{"source": source_tag}],
            ids=[chunk_id]
        )
    print(f"[+] Successfully indexed {file_name} to persistent local database storage.")

if __name__ == "__main__":
    # Ingesting the highly critical datasets compiled in previous steps
    print("\n--- Starting Phase 1 Ingestion (Core Threat Intelligence) ---")
    ingest_file_to_vector_db("cve_threat_intel.txt", "HuggingFace_ThreatIntel")
    ingest_file_to_vector_db("darkweb_fraud_intel.txt", "Fenrir_CyberExploits")
    ingest_file_to_vector_db("instruction_tuning_intel.txt", "Trendyol_InstructionTuning")
    ingest_file_to_vector_db("safety_bypass_intel.txt", "AdvBench_SafetyBypass")
    
    print("\n[+] Master Ingestion Process Completed! Data is persistent inside D:\\advanced_gpt\\chroma_db_storage.")