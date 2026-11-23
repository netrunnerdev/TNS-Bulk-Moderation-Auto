import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (your API key)
load_dotenv()

# Initialize the OpenAI client 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_policy_violation(text):
    """Sends text to OpenAI API and routes using custom T&S confidence bands."""
    try:
        response = client.moderations.create(input=text)
        result = response.results[0]
        scores = result.category_scores
        
        # Pull the highest risk score across our core policy areas
        max_risk_score = max(
            scores.hate,
            scores.violence,
            scores.harassment,
            scores.self_harm
        )
        
        # 1. THE RED ZONE (>= 85% confidence): Undeniable severe harm -> Instant Ban
        if max_risk_score >= 0.85:
            return "Auto-Ban"
        
        # 2. THE GRAY ZONE (15% to 84% confidence): Idioms, gaming slang, or borderline toxicity -> Human Queue
        if max_risk_score >= 0.15:
            return "Human Review"
            
        # 3. THE GREEN ZONE (< 15% confidence): Benign content -> Instant Clear
        return "Auto-Clear"
        
    except Exception as e:
        print(f"API Error on text: {text}. Error: {e}")
        return "Error - Send to Human"

def run_pipeline():
    """Loads data, runs the AI checks, and saves the results."""
    print("1. Loading reported comments...")
    df = pd.read_csv("reported_comments.csv")
    print(f"Loaded {len(df)} items in the queue.")

    print("2. Running text through ML Moderation API...")
    # This applies the function above to every row in our CSV
    df['Automated_Action'] = df['comment_text'].apply(check_policy_violation)

    print("3. Exporting processed queue...")
    df.to_csv("processed_comments.csv", index=False)
    print("Done! Check processed_comments.csv for the results.")

# This triggers the whole script to run!
run_pipeline()