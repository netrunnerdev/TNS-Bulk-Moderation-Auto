## Trust & Safety Bulk Moderation Automation Pipeline

## The Business Problem
In Trust & Safety operations, human reviewers often face massive queues of reported content. Manually reviewing every benign or highly abusive comment leads to reviewer fatigue, high operational costs, and slower response times for critical safety violations.

## The Solution
This project is an automated Python data pipeline designed to pre-screen reported content queues using generative AI, allowing human moderators to focus only on nuanced or ambiguous cases. 

The script ingests a raw CSV of user reports and processes them through the **OpenAI Moderation API**. 
* **Zero-Tolerance Violations** (e.g., severe hate speech, credible threats) are tagged for automated enforcement (`Auto-Ban`).
* **Ambiguous or Benign Content** is tagged for human escalation (`Human Review`).

## How It Works
1. **Data Ingestion:** Uses `pandas` to load a queue of reported comments.
2. **API Integration:** Iterates through the data and securely passes text payloads to the `openai.moderations` endpoint.
3. **Decision Routing:** Parses the API's JSON response and applies a boolean flag to route the action.
4. **Data Export:** Outputs a cleaned, structured CSV ready to be uploaded back into a T&S enforcement platform or visualized in a SQL/Tableau dashboard.

## Tech Stack
* **Language:** Python
* **Data Manipulation:** Pandas
* **Integrations:** OpenAI API
* **Environment:** GitHub Codespaces / python-dotenv
