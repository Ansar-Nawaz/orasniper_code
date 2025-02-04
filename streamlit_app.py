import streamlit as st
from llama_index.core import VectorStoreIndex, Document
import fitz  # PyMuPDF for PDF processing

# Streamlit App Configuration
st.set_page_config(page_title="OraSniper - Oracle Error Chatbot", page_icon="🔍", layout="centered")

st.title("OraSniper - Oracle Error Chatbot 🔍💬")
st.info("Enter an Oracle error code (e.g., ORA-00942) to get details and solutions.", icon="ℹ️")

# Initialize chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I assist you with Oracle errors today?"}]

@st.cache_resource(show_spinner=False)
def load_pdf_data(pdf_path):
    """Extract text from the provided PDF."""
    doc = fitz.open(pdf_path)
    text_data = "\n".join([page.get_text("text") for page in doc])
    return text_data

# Load Oracle error messages from PDF
oracle_errors_text = load_pdf_data("./data/database-error-messages.pdf")

# Ensure text is wrapped in a Document object
documents = [Document(text=oracle_errors_text)]

# Create index from properly formatted documents
index = VectorStoreIndex.from_documents(documents)

# User input for error code
user_input = st.text_input("Enter Oracle error code:")

if user_input:
    query_engine = index.as_query_engine()
    response = query_engine.query(user_input)
    
    # Store messages in session
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": str(response)})

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
