import streamlit as st
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from pathlib import Path
from router import router

faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faqs_path)


def ask(query):
    route = router(query).name
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    else:
        # Default fallback or better error message
        return sql_chain(query) # Fallback to SQL if unsure, or "I didn't understand that."


st.set_page_config(
    page_title="E-Commerce AI Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main chat styling */
    .stChatMessage {
        background-color: #f8f9fa; 
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stChatMessage[data-testid="user-message"] p {
        color: white !important;
    }
    
    /* Assistant message styling - darker background for better link visibility */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #2d3748;
        color: #e2e8f0;
    }
    
    .stChatMessage[data-testid="assistant-message"] p {
        color: #e2e8f0 !important;
    }
    
    /* Link styling - highly visible */
    .stChatMessage a {
        color: #63b3ed !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        padding: 2px 6px;
        border-radius: 4px;
        background-color: rgba(99, 179, 237, 0.15);
        transition: all 0.2s ease;
    }
    
    .stChatMessage a:hover {
        color: #90cdf4 !important;
        background-color: rgba(99, 179, 237, 0.25);
        text-decoration: underline !important;
    }
    
    /* Title styling */
    h1 {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Caption styling */
    .stCaptionContainer {
        text-align: center;
        color: #718096;
        font-size: 1.1rem;
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        border-top: 2px solid #e2e8f0;
        padding-top: 1rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.title("💡 How to Use")
    st.markdown("""
    ### Ask Questions About:
    
    **🛍️ Products**
    - "Show me Nike shoes under 5000"
    - "Find shoes with rating above 4.5"
    - "What Puma shoes are available?"
    
    **ℹ️ Policies**
    - "What is the return policy?"
    - "Do you accept online payment?"
    - "How to track my order?"
    
    ### Features:
    ✨ Real-time database search  
    🤖 AI-powered responses  
    📊 Filtered by price & rating  
    🔗 Direct product links
    """)
    
    st.divider()
    st.caption("Powered by Groq & Llama 3.3")

st.title("🛍️ E-Commerce Chat-Bot")
st.caption("Ask me about shoes, prices, or return policies!")



query = st.chat_input("Write your query")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role":"user", "content":query})

    response = ask(query)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


