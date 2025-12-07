import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    # Handle the case where the key is missing gracefully, or let it fail later
    pass

def get_model():
    return genai.GenerativeModel('gemini-2.0-flash')

def generate_user_response(rating, review):
    """
    Generates a friendly response to the user based on their rating and review.
    """
    if not API_KEY:
        return "Thank you for your feedback! (LLM API Key not configured)"

    try:
        model = get_model()
        prompt = f"""
        You are a customer service AI. A user has just submitted feedback.
        Rating: {rating}/5 Stars
        Review: "{review}"

        Write a short, friendly, and professional response to the user acknowledging their feedback.
        If the rating is low, be apologetic and promise improvement.
        If the rating is high, be appreciative.
        Keep it under 50 words.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Thank you for your feedback! (Error generating AI response: {str(e)})"

def analyze_submission(rating, review):
    """
    Analyzes the submission for the admin dashboard.
    Returns a tuple (summary, recommendations).
    """
    if not API_KEY:
        return "No API Key", "No API Key"

    try:
        model = get_model()
        prompt = f"""
        Analyze the following customer feedback:
        Rating: {rating}/5 Stars
        Review: "{review}"

        Provide two things separated by a pipe character (|):
        1. A concise 1-sentence summary of the review.
        2. A short, actionable business recommendation based on this feedback.

        Format: Summary | Recommendation
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if "|" in text:
            parts = text.split("|", 1)
            return parts[0].strip(), parts[1].strip()
        else:
            return text, "Check full review for details."
    except Exception as e:
        return "Error analyzing", f"Error: {str(e)}"
