import streamlit as st
import chromadb
import requests
import json
import base64
import os

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DB_DIR = r"D:\advanced_gpt\chroma_db_storage"
SVG_PATH = r"D:\advanced_gpt\automation_scripts\dadasdasdasas.svg"
BG_IMG_PATH = r"D:\advanced_gpt\automation_scripts\WormGPT.jpg"

st.set_page_config(page_title="T0r_Worm_X Engine", layout="centered")

def get_base64_encoded_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

bg_base64 = get_base64_encoded_image(BG_IMG_PATH)

# Using standard replacement to prevent Python f-string bracket parsing bugs
style_template = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

.stApp {
    background: linear-gradient(rgba(15, 15, 16, 0.88), rgba(15, 15, 16, 0.94)), url('data:image/jpeg;base64,BG_REPLACE') !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    color: #00FF66 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.block-container {
    max-width: 760px !important;
    padding-top: 5rem !important;
    padding-bottom: 4rem !important;
}

.kwx-header {
    display: flex !important;
    align-items: center !important;
    gap: 16px !important;
    margin-bottom: 2rem !important;
}

.kwx-logo-container {
    width: 50px !important;
    height: 50px !important;
    display: inline-block !important;
}

/* Force SVG paths to take pure hacker green color */
.kwx-logo-container svg, .kwx-logo-container svg path {
    fill: #00FF66 !important;
    width: 50px !important;
    height: 50px !important;
}

/* Title is now pure High-Contrast Green */
.kwx-title {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 500 !important;
    color: #00FF66 !important;
    letter-spacing: -0.02em !important;
    margin: 0 !important;
    line-height: 1 !important;
    text-shadow: 0 0 10px rgba(0, 255, 102, 0.4) !important;
}

.kwx-status {
    display: flex;
    gap: 20px;
    margin-bottom: 2.5rem;
    flex-wrap: wrap;
}

.kwx-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #00FF66 !important;
    font-weight: bold;
    letter-spacing: 0.05em;
}

.kwx-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00FF66;
    box-shadow: 0 0 10px #00FF66;
}

.stTextArea textarea {
    background-color: rgba(26, 26, 28, 0.85) !important;
    color: #FFFFFF !important;
    border: 1px solid #00FF66 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 14px 16px !important;
}

.stTextArea textarea:focus {
    border-color: #00FF66 !important;
    box-shadow: 0 0 10px rgba(0, 255, 102, 0.3) !important;
}

.stButton > button {
    background-color: #00FF66 !important;
    color: #0F0F10 !important;
    border: 1px solid #00FF66 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    font-weight: bold !important;
    padding: 8px 24px !important;
    float: right !important;
    box-shadow: 0 0 12px rgba(0, 255, 102, 0.4) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background-color: #00CC52 !important;
    box-shadow: 0 0 20px #00FF66 !important;
    color: #000000 !important;
}

.kwx-response-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #00FF66;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 2.5rem;
    margin-bottom: 8px;
}

.kwx-response {
    background-color: rgba(10, 10, 12, 0.9) !important;
    border: 1px solid #00FF66 !important;
    border-radius: 10px;
    padding: 24px;
    font-family: 'DM Mono', monospace;
    font-size: 0.9rem;
    color: #00FF66 !important;
    line-height: 1.7;
    white-space: pre-wrap;
    box-shadow: inset 0 0 10px rgba(0, 255, 102, 0.1);
}

.stSpinner > div {
    border-top-color: #00FF66 !important;
}

#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
"""
final_style = style_template.replace("BG_REPLACE", bg_base64)
st.markdown(final_style, unsafe_allow_html=True)

if 'db_collection' not in st.session_state:
    try:
        db_client = chromadb.PersistentClient(path=DB_DIR)
        st.session_state.db_collection = db_client.get_collection(name="cybersec_intelligence_pool")
    except Exception:
        st.session_state.db_collection = None

def get_db_context(query_text):
    if st.session_state.db_collection is None:
        return ""
    try:
        results = st.session_state.db_collection.query(query_texts=[query_text], n_results=3)
        chunks = []
        if results and 'documents' in results and results['documents']:
            for sub in results['documents']:
                chunks.extend(sub)
        return "\n\n".join(chunks)
    except Exception:
        return ""

svg_html = ""
if os.path.exists(SVG_PATH):
    with open(SVG_PATH, "r", encoding="utf-8") as f:
        svg_html = f.read()

# Safe rendering of logo and green title
header_html = f"""
<div class="kwx-header">
    <div class="kwx-logo-container">{svg_html}</div>
    <span class="kwx-title">T0r_Worm_X</span>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

db_ok = st.session_state.db_collection is not None
db_label = "CHROMADB CONNECTED" if db_ok else "CHROMADB OFFLINE"

st.markdown(f"""
<div class="kwx-status">
    <span class="kwx-badge"><span class="kwx-dot"></span>MODEL ONLINE</span>
    <span class="kwx-badge"><span class="kwx-dot" style="background:{'#00FF66' if db_ok else '#FF3333'}; box-shadow: 0 0 8px {'#00FF66' if db_ok else '#FF3333'};"></span>{db_label}</span>
    <span class="kwx-badge"><span class="kwx-dot"></span>VECTOR SEARCH READY</span>
</div>
""", unsafe_allow_html=True)

user_input = st.text_area("", placeholder="Message T0r_Worm_X...", height=130, label_visibility="collapsed")
run_clicked = st.button("Run")

if run_clicked:
    if user_input.strip():
        context = get_db_context(user_input)
        st.markdown('<div class="kwx-response-label">Response</div>', unsafe_allow_html=True)
        
        response_placeholder = st.empty()
        full_prompt = f"BACKGROUND CONTEXT FROM VECTOR DATASET:\n{context}\n\nUSER INPUT:\n{user_input}"
        payload = {"model": "T0r_Worm_X", "prompt": full_prompt, "stream": True}
        
        collected_response = ""
        try:
            with requests.post(OLLAMA_API_URL, json=payload, stream=True, timeout=120) as res:
                if res.status_code == 200:
                    for line in res.iter_lines():
                        if line:
                            decoded_line = json.loads(line.decode('utf-8'))
                            token = decoded_line.get("response", "")
                            collected_response += token
                            response_placeholder.markdown(f'<div class="kwx-response">{collected_response}▒</div>', unsafe_allow_html=True)
                    response_placeholder.markdown(f'<div class="kwx-response">{collected_response}</div>', unsafe_allow_html=True)
                else:
                    response_placeholder.markdown(f'<div class="kwx-response">Error executing stream matrix: {res.status_code}</div>', unsafe_allow_html=True)
        except Exception as e:
            response_placeholder.markdown(f'<div class="kwx-response">Connection Failed: Stream Interface Timeout. Build logs: {str(e)}</div>', unsafe_allow_html=True)
    else:
        st.error("Matrix execution string cannot be empty.")