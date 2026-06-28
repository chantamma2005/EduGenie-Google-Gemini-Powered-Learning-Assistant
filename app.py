from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

# -----------------------------
# Configure Gemini API
# -----------------------------
genai.configure(api_key="AQ.Ab8RN6I1DGYlJ8CAi2R4Y0awL7A7epr6HfyPbs6dJ4BS8P7d1A")

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title="EduGenie Learning Assistant",
    version="1.0"
)

# Static and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# -----------------------------
# Gemini Helper Function
# -----------------------------
def ask_gemini(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"


# -----------------------------
# Home Page
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
       "index.html",
     {"request": request}
    )
@app.get("/")
def home():
    return {
        "message": "EduGenie API is Running"
    }

# -----------------------------
# Question Answering
# -----------------------------
@app.get("/qa")
async def question_answer(question: str = Query(...)):
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
@app.get("/learn/recommendations")
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