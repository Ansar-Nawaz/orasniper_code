import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
import fitz  # PyMuPDF for PDF processing

st.set_page_config(page_title="Oracle Error Chatbot", page_icon="🔍", layout="centered")

st.title("OraSniper - Oracle Error Chatbot 🔍💬")
st.info("Enter an Oracle error code (e.g., ORA-00942) to get details and solutions.", icon="ℹ️")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I assist you with Oracle errors today?"}]

@st.cache_resource(show_spinner=False)
def load_pdf_data(pdf_path):
    """Extract text from the provided PDF and return as a list of lines."""
    doc = fitz.open(pdf_path)
    text_data = []
    for page in doc:
        text_data.append(page.get_text("text"))
    return "\n".join(text_data)

# Load Oracle error messages from PDF
oracle_errors_text = load_pdf_data("./data/database-error-messages.pdf")

# Set up LlamaIndex with extracted text
documents = [oracle_errors_text]
index = VectorStoreIndex.from_documents(documents)

# User input
user_input = st.text_input("Enter Oracle error code:")

if user_input:
    query_engine = index.as_query_engine()
    response = query_engine.query(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
