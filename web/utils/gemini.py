import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

# Use an available model from your list
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-001")

def generate_weekly_wrapup(diary_text, goal_text):
    prompt = f"""
    Weekly Diary Wrap-up:

    Diary Entries for the Week:
    {diary_text}

    My Goals:
    {goal_text}

    Please:
    - Summarize the diary entries.
    - Analyze how well I followed my goals.
    - Suggest improvements or tips if I fell short.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"
