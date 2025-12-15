from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from .database import init_db
from .graph import graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    try:
        init_db()
        print("Database initialized.")
    except Exception as e:
        print(f"Error initializing DB: {e}")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        
        input_message = HumanMessage(content=request.message)
        
        output = await graph.ainvoke({"messages": [input_message]}, config=config)
        
        last_message = output["messages"][-1]
        return {"response": last_message.content}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
