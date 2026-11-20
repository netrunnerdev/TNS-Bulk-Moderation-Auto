import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (your API key)
load_dotenv()

# Initialize the OpenAI client 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_policy_violation(text):
    """Sends text to OpenAI Moderation API and returns the action."""
    try:
        # Call the OpenAI Moderation endpoint 
        response = client.moderations.create(input=text)
        
        # The API returns a boolean 'flagged' status if it violates policies
        is_flagged = response.results[0].flagged
        
        return "Auto-Ban" if is_flagged else "Human Review"
    
    except Exception as e:
        print(f"API Error on text: {text}. Error: {e}")
        return "Error - Send to Human"

def run_pipeline():
    print("1. Loading reported comments...")
    df = pd.read_csv("reported_comments.csv")
    print(f"Loaded {len(df)} items in the queue.")

    print("2. Running text through ML Moderation API...")
    # Apply our checking function to every comment in the CSV
    df['Automated_Action'] = df['comment_text'].apply(check_policy_violation)

    print("3. Exporting processed queue...")
    df.to_csv("processed_comments.csv", index=False)
    print("Done! Check processed_comments.csv for the results.")

if __name__ == "__main__":
    run_pipeline()
