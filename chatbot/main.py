import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = FastAPI()

# Correct CORS (do NOT use full path)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # PyCharm internal server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# HTML templates folder
templates = Jinja2Templates(directory="templates")

# Memory store
user_memory = {}


# Model for incoming message
class UserMessage(BaseModel):
    message: str
    session_id: str | None = "default_user"


# Serve HTML page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Chat API endpoint
@app.post("/chat")
async def chat_bot(user_message: UserMessage):

    text = user_message.message.lower()
    session = user_message.session_id

    if session not in user_memory:
        user_memory[session] = {"name": None}

    memory = user_memory[session]

    # STEP 1: greeting → ask name
    if memory["name"] is None and text in ["hi", "hello", "hey"]:
        return {"reply": "Hello! What is your name?"}

    # STEP 2: store name
    if memory["name"] is None:
        name = user_message.message.strip().title()
        memory["name"] = name
        return {
            "reply": f"Good, {name}. How can I help you?\n"
        }


    # STEP 3: normal OpenAI conversation after name is known
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are chatting with {memory['name']}. Be friendly."},
                {"role": "user", "content": user_message.message}
            ]
        )
        return {"reply": response.choices[0].message["content"]}

    except Exception as e:
        return {"error": str(e)}
