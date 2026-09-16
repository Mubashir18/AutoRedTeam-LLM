import chromadb
import requests
import json
import os
import sys
import time

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DB_DIR = r"D:\advanced_gpt\chroma_db_storage"
COLLECTION_NAME = "cybersec_intelligence_pool"
ACTUAL_MODEL_NAME = "KhanzadaWormX"
HISTORY_FILE = r"D:\advanced_gpt\automation_scripts\chat_sessions.json"

# Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def init_db():
    try:
        db_client = chromadb.PersistentClient(path=DB_DIR)
        return db_client.get_collection(name=COLLECTION_NAME)
    except Exception:
        return None

def get_db_context(collection, query_text):
    if collection is None: return ""
    try:
        # 🛠️ LOW-CPU OPTIMIZATION 1: n_results ko 2 se kam karke 1 kar diya
        # Is se database se sirf 1 hi sab se important chunk load hoga, CPU par load 50% kam hoga
        results = collection.query(query_texts=[query_text], n_results=1)
        return "\n\n".join(results['documents'][0]) if results and results['documents'] else ""
    except Exception:
        return ""

def load_all_sessions():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_all_sessions(sessions):
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"{RED}[-] Storage Error: {str(e)}{RESET}")

def main():
    # 🛠️ LOW-CPU OPTIMIZATION 2: Python script ko Windows par 'Below Normal' priority de dein
    # Is se PC lag nahi hoga aur background mein doosre kaam smoothly chalte rahenge
    if os.name == 'nt':
        try:
            import win32process, win32api, win32con
            pid = win32api.GetCurrentProcessId()
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
            win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
        except ImportError:
            pass # Agar library nahi bhi hai toh normal chalega

    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{GREEN}====================================================")
    print(f"         T0r_root_access_v1 - ECO-CPU ENGINE         ")
    print(f"===================================================={RESET}")
    
    collection = init_db()
    if collection:
        print(f"{GREEN}[+] CHROMADB CONNECTED & VECTOR SEARCH READY{RESET}")
    else:
        print(f"{RED}[-] ChromaDB Offline. Running in standard model mode.{RESET}")

    print(f"{YELLOW}System Commands: 'new' (Nayi Chat) | 'list' (Saved Chats) | 'exit' (Quit){RESET}\n")

    sessions_db = load_all_sessions()
    current_chat_id = f"chat_{int(time.time())}"
    if current_chat_id not in sessions_db:
        sessions_db[current_chat_id] = []
        save_all_sessions(sessions_db)

    print(f"{CYAN}[*] Eco-Session Initialized: {current_chat_id}{RESET}\n")
    http_session = requests.Session()

    while True:
        try:
            current_messages = sessions_db[current_chat_id]
            user_input = input(f"{GREEN}[{current_chat_id}] T0r_root_access_v1 >> {RESET}").strip()
            
            if not user_input:
                continue

            if user_input.lower() == 'new':
                current_chat_id = f"chat_{int(time.time())}"
                sessions_db[current_chat_id] = []
                save_all_sessions(sessions_db)
                print(f"\n{CYAN}[*] Allocating Nayi Chat -> {current_chat_id}{RESET}\n")
                continue

            if user_input.lower() == 'list':
                print(f"\n{YELLOW}========== SAVED CHATS STORAGE =========={RESET}")
                for cid in sessions_db.keys():
                    msg_count = len(sessions_db[cid])
                    marker = " <-- (ACTIVE)" if cid == current_chat_id else ""
                    print(f" {GREEN}[ID]: {cid} {RESET}({msg_count} messages){marker}")
                print(f"{YELLOW}========================================={RESET}")
                
                target_id = input(f"{CYAN}Enter Chat ID to switch: {RESET}").strip()
                if target_id in sessions_db:
                    current_chat_id = target_id
                    print(f"\n{GREEN}[+] Switched Successfully to: {current_chat_id}{RESET}\n")
                else:
                    print(f"\n{RED}[-] Invalid ID. Resuming current session.{RESET}\n")
                continue

            if user_input.lower() in ['exit', 'quit']:
                print(f"\n{GREEN}[*] Session Terminated. Saved JSON state.{RESET}")
                break

            print(f"\n{CYAN}[*] Querying local text context...{RESET}")
            context = get_db_context(collection, user_input)
            
            print(f"{CYAN}[*] Routing payload via optimized thread pool...{RESET}\n")
            print(f"{GREEN}--- RESPONSE ---")

            # 🛠️ LOW-CPU OPTIMIZATION 3: History window ko sirf aakhri 4 messages (2 turns) tak restrict kiya
            # Is se prompt chhota rahega aur CPU crash ya overheat nahi hoga
            recent_messages = current_messages[-4:] if len(current_messages) > 4 else current_messages

            history_context = ""
            if recent_messages:
                history_context = "\n".join([f"User: {m['content']}" if m['role']=='user' else f"Assistant: {m['content']}" for m in recent_messages])

            full_prompt = f"RAG CONTEXT:\n{context}\n\n[PAST CHAT HISTORY]:\n{history_context}\n\nCURRENT USER INPUT:\n{user_input}"
            
            # 🛠️ LOW-CPU OPTIMIZATION 4: Ollama runtime options override
            # num_predict ko restrict kiya aur threads ko auto balance par set kiya
            payload = {
                "model": ACTUAL_MODEL_NAME, 
                "prompt": full_prompt, 
                "stream": True,
                "options": {
                    "num_predict": 256,   # Jawab ki lambai ko limits mein rakhega taaki CPU heavy generation lambi na khiche
                    "num_ctx": 2048       # Total memory area limit taaki RAM crash na ho
                }
            }
            
            assistant_response = ""
            with http_session.post(OLLAMA_API_URL, json=payload, stream=True, timeout=None) as res:
                if res.status_code == 200:
                    for line in res.iter_lines():
                        if line:
                            decoded_line = json.loads(line.decode('utf-8'))
                            token = decoded_line.get("response", "")
                            sys.stdout.write(f"{GREEN}{token}")
                            sys.stdout.flush()
                            assistant_response += token
                    print(f"\n========================================{RESET}\n")
                    
                    sessions_db[current_chat_id].append({"role": "user", "content": user_input})
                    sessions_db[current_chat_id].append({"role": "assistant", "content": assistant_response})
                    save_all_sessions(sessions_db)
                else:
                    print(f"\n{RED}[-] Execution Matrix Error: {res.status_code}{RESET}\n")
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n{RED}[-] Exception Trace: {str(e)}{RESET}\n")

if __name__ == "__main__":
    main()