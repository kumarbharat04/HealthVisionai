import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key="AIzaSyAqOCQYzpSie5j3YeCdyAU0iozTv-lTkKo")

# Load the Gemini Model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Generate chatbot response with context
def get_bot_response(user_input):
    try:
        prompt = (
            "You are HealthVisionAI, a supportive and empathetic mental health assistant. "
            "You help users express emotions, reduce stress, and stay positive. "
            "Respond in an encouraging, gentle tone. Suggest breathing, journaling, or self-care practices. "
            "⚠️ Never give diagnosis or medication advice.\n\n"
            f"User: {user_input}\n"
            "AI:"
        )

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("⚠️ Gemini API Error:", e)
        return "⚠️ Sorry, something went wrong. Please try again later."
