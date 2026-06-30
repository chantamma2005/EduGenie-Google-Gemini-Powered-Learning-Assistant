from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google import genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# -----------------------------
# Configure Gemini API
# -----------------------------
client = genai.Client(api_key="AQ.Ab8RN6KNJ4tOjVv2ZOsXZE6Ki2XO38CwYYBywEGm3Myb6I2dHA")

def ask_gemini(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini Error: {e}"

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class QARequest(BaseModel):
    question: str

class RequestData(BaseModel):
    text: str


# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
# -----------------------------
# Question Answering
# -----------------------------
@app.post("/qa")
async def question_answer(data: QARequest):

    question = data.question

    prompt = f"""
You are an educational AI assistant.

Answer the following question clearly and accurately.

Question:
{question}
"""

    answer = ask_gemini(prompt)

    return {
        "question": question,
        "answer": answer
    }

# -----------------------------
# Concept Explanation
# -----------------------------
@app.post("/explain")
async def explain(request: Request):

    data = await request.json()

    topic = data.get("topic")

    if not topic:
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide a topic."}
        )

    prompt = f"""
Explain the following topic in simple language suitable for students.

Topic:
{topic}
"""

    explanation = ask_gemini(prompt)

    return {
        "topic": topic,
        "explanation": explanation
    }


# -----------------------------
# Text Summarization
# -----------------------------
@app.post("/summarize")
async def summarize(request: Request):

    data = await request.json()

    text = data.get("text")

    if not text:
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide text."}
        )

    prompt = f"""
Summarize the following educational content in concise bullet points.

Content:
{text}
"""

    summary = ask_gemini(prompt)

    return {
        "summary": summary
    }


# -----------------------------
# Quiz Generation
# -----------------------------
@app.post("/quiz")
async def quiz(request: Request):

    data = await request.json()

    text = data.get("text")

    if not text:
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide text."}
        )

    prompt = f"""
Create exactly 5 multiple-choice questions.

Each question must have:

Question:
A.
B.
C.
D.

Correct Answer:

Content:
{text}
"""

    quiz = ask_gemini(prompt)

    return {
        "quiz": quiz
    }


# -----------------------------
# Learning Recommendation
# -----------------------------
@app.post("/learn/recommendations")
async def learning_path(topic: str = Query(...)):

    prompt = f"""
Create a personalized learning roadmap for:

{topic}

Include:

1. Beginner Concepts

2. Intermediate Concepts

3. Advanced Concepts

4. Practice Projects

5. Learning Resources

6. Estimated Learning Time
"""

    recommendation = ask_gemini(prompt)

    return {
        "topic": topic,
        "recommendation": recommendation
    }