import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (your API key)
load_dotenv()

# Initialize the OpenAI client 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_policy_violation(text):
    """Sends text to OpenAI API and routes based on confidence scores."""
    try:
        response = client.moderations.create(input=text)
        result = response.results[0]
        
        # 1. THE RED ZONE: OpenAI is absolutely certain it's a severe violation
        if result.flagged:
            return "Auto-Ban"
        
        # 2. THE GRAY ZONE: Pull the raw decimal scores (0.0 to 1.0) to find edge cases
        # We will check 'hate' and 'violence' as our primary risk categories
        hate_score = result.category_scores.hate
        violence_score = result.category_scores.violence
        
        # If the AI is more than 20% confident it might be abusive, flag for human review
        if hate_score >= 0.20 or violence_score >= 0.20:
            return "Human Review"
            
        # 3. THE GREEN ZONE: The AI is highly confident the text is safe
        return "Auto-Clear"
        
    except Exception as e:
        print(f"API Error on text: {text}. Error: {e}")
        return "Error - Send to Human"
