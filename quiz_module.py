import re
import json
import google.generativeai as genai


def clean_json_block(text):
    # Remove Markdown ```json code fences
    return re.sub(r"```(?:json)?\n(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

        prompt = f"""
        ...
        """

        response = model.generate_content(prompt)

        # Debug output
        print("Gemini Response:")
        print(response.text)

        quiz_text = response.text.strip()

        cleaned_text = clean_json_block(quiz_text)

        return json.loads(cleaned_text)

    except Exception as e:
        print("Quiz Error:", e)   # Debug output
        return [{"error": str(e)}]