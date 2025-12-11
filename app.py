from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from langchain_pinecone import PineconeVectorStore
from src.config import Config
from src.helper import download_embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from src.prompt import system_prompt
import uuid


Config.validate()


PINECONE_API_KEY = Config.PINECONE_API_KEY
GEMINI_API_KEY = Config.GEMINI_API_KEY

templates = Jinja2Templates(directory="templates")

# Intialize FastAPI app
app = FastAPI(title="Medical Chatbot",version="0.0.0")

# Store for session-based chat histories (resets on server restart)
chat_histories = {}

# Intialize embedding model
print("Loading the Embedding model...")
embeddings = download_embeddings()

# Connect to existing Pinecone index
index_name = Config.PINECONE_INDEX_NAME
print(f"Connecting to PineCone index: {index_name}")
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Creating retriever from vector store
retriever = docsearch.as_retriever(
    search_type=Config.SEARCH_TYPE,
    search_kwargs={"k":Config.RETRIEVAL_K}
)

# Initialize Google Gemini chat model
print("Initializing Gemini model...")
llm = ChatGoogleGenerativeAI(
    model=Config.GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=Config.LLM_TEMPERATURE,
    convert_system_message_to_human=True
)

# Create chat prompt template with memory
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

# Create the question-answer chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Create the RAG chain
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Function to get chat history for a session
def get_chat_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

# Function to maintain conversation window buffer (keep last 5 messages)
def manage_memory_window(session_id: str, max_messages: int = 10):
    """Keep only the last max_messages (5 pairs = 10 messages)"""
    if session_id in chat_histories:
        history = chat_histories[session_id]
        if len(history.messages) > max_messages:
            # Keep only the last max_messages
            history.messages = history.messages[-max_messages:]

print("Intialized Medical Chabot successfuly!")
print("Vector Store connected")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the chatbot interface"""
    # Clear all old sessions to prevent memory overflow
    chat_histories.clear()
    
    # Generate a new session ID for each page load
    session_id = str(uuid.uuid4())
    return templates.TemplateResponse("index.html", {"request": request, "session_id": session_id})

@app.post("/get", response_class=JSONResponse)
async def chat(msg: str = Form(...), session_id: str = Form(...)):
    """Handle chat messages and return AI responses with conversation memory"""
    try:
        # Get chat history for this session
        history = get_chat_history(session_id)
        
        # Invoke the RAG chain with the user's message and chat history
        response = rag_chain.invoke({
            "input": msg,
            "chat_history": history.messages
        })
        
        # Extract the answer from the response
        answer = response.get("answer", "I'm sorry, I couldn't process your request.")
        
        # Add the conversation to history
        history.add_user_message(msg)
        history.add_ai_message(answer)
        
        # Manage memory window to keep only last 5 conversation pairs (10 messages)
        manage_memory_window(session_id, max_messages=10)
        
        return JSONResponse(content={"response": answer})
    
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return JSONResponse(
            content={"response": "I apologize, but I encountered an error. Please try again."},
            status_code=500
        )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)