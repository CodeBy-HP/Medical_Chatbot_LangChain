from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from langchain_pinecone import PineconeVectorStore
from src.config import Config
from src.helper import download_embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt


Config.validate()


PINECONE_API_KEY = Config.PINECONE_API_KEY
GEMINI_API_KEY = Config.GEMINI_API_KEY

templates = Jinja2Templates(directory="templates")

# Intialize FastAPI app
app = FastAPI(title="Medical Chatbot",version="0.0.0")

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

# Create chat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Create the question-answer chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Create the RAG chain
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

print("Intialized Medical Chabot successfuly!")
print("Vector Store connected")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    pass

@app.post("/get")
async def chat(msg: str = Form(...)):
    pass

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)