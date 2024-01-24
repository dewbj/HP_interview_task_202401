from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List, Optional, AsyncGenerator

import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app=FastAPI(docs_url = None, redoc_url = None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="view")

class Message(BaseModel):
    content: str
    model: Optional[str] = "gpt-4-1106-preview"

async def get_ai_response(message: str, gpt_model: str) -> AsyncGenerator[str, None]:

    client = AsyncOpenAI()

    response = await client.chat.completions.create(
        model = gpt_model,
        messages=[
            {
                "role": "user",
                "content": message,
            },
        ],
        stream=True,
        temperature=0.1
    )

    all_content = ""
    async for chunk in response:
        yield chunk.choices[0].delta.content or ""

@app.get("/hp")
async def hp(request: Request):
    response = templates.TemplateResponse("hp.html", {"request": request})
    return response

@app.post("/hp")
async def hp(request: Request, message: Message):
    model = message.model
    prompt = message.content
    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local("./index/landscaping_insight_report", embeddings)
    retriever = db.as_retriever()
    retrieved_docs = retriever.invoke(
        prompt
    )
    question = "Please answer the question: " + prompt + ". According to: " + retrieved_docs[0].page_content
    generator = get_ai_response(question, model)

    return StreamingResponse(generator, media_type="text/event-stream")