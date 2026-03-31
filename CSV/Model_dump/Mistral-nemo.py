import ollama
import json
import pandas as pd
from tqdm import tqdm

def process_description(job_text):
    model_name = "mistral:7b-instruct" 

    system_prompt = """
    You are a professional HR data extraction assistant.

    Your task is to extract structured data from job descriptions and return it in STRICTLY STANDARDIZED format in ENGLISH.

    IMPORTANT:
    - If the input is not in English, translate extracted data to English.
    - Be consistent. Always use the SAME format for similar data.

    STRICT RULES:
    1. Return ONLY a valid JSON object.
    2. Do NOT include explanations or text outside JSON.
    3. If a value is missing, use null.

    4. Use EXACTLY these keys:
    "Location",
    "Salary",
    "Language Requirements",
    "Education Requirements",
    "Programming Languages",
    "Required Software / Tools",
    "Work Arrangement",
    "Job Type",
    "Experience Level",

    ------------------------
    FORMATTING RULES:

    SALARY:
    - Always format as: "MIN-MAX CURRENCY gross/month"
    - Example: "2000-2500 EUR gross/month"
    - If only one value: "5000 EUR gross/month"
    - If hourly: "2000 EUR/hour"
    - If not specified: null

    LANGUAGES:
    - Always list format: ["English: B2", "Hungarian: Native"]
    - Use CEFR levels if possible (A1–C2)
    - If unknown level: "English: Required"

    PROGRAMMING LANGUAGES:
    - Only real programming languages
    - Example: ["Python", "JavaScript"]

    TOOLS:
    - Software, frameworks, tools only
    - Example: ["Docker", "Git", "AWS"]

    WORK ARRANGEMENT:
    - ONLY one of:
      "On-site"
      "Home-Office"
      "Hybrid"
      "On-site with home office"

    JOB TYPE:
    - ONLY one of:
      "Full-time"
      "Short-term"
      "Half-time"

    EXPERIENCE LEVEL:
    - Format:
      "0-1 years"
      "1-3 years"
      "3-5 years"
      "5+ years"
    - If not clear → null



    LOCATION:
    - Only city name (e.g. "Budapest")

    ------------------------

    EXAMPLE OUTPUT:

    {
        "Job Title": "Software Engineer",
        "Location": "Budapest",
        "Salary": "500000-700000 HUF gross/month",
        "Language Requirements": ["English: B2"],
        "Education Requirements": "Bachelor | Computer Science",
        "Programming Languages": ["Python", "C++"],
        "Required Software / Tools": ["Git", "Docker"],
        "Work Arrangement": "Hybrid",
        "Job Type": "Full-time",
        "Experience Level": "3-5 years",
    }
    """

    try:
        response = ollama.generate(
            model=model_name,
            system=system_prompt,
            prompt=f"Extract info from this text: {job_text}\n\nJSON output:",
            format="json",
            options={"temperature": 0}
        )
        return json.loads(response['response'])
    except Exception as e:
        print(f"Error processing row: {e}")
        return {}

def main():
    input_file = 'professia_jobs.csv'
    output_file = 'mistral.csv'

    # CSV beolvasása
    df = pd.read_csv(input_file).head(10)
    
    keep_columns = ['job_id','title','company', 'url', 'first_seen', 'last_seen','active', 'description']
    df = df[keep_columns]

    structured_data = []

    print(f"\nProcessing {len(df)} jobs with Ollama...")
    
    # tqdm mutatja a haladást a terminálban
    for index, row in tqdm(df.iterrows(), total=len(df)):
        extracted = process_description(row['description'])
        
        # Alapadatok + kinyert adatok összefésülése
        combined_row = {
            'job_id': row['job_id'],
            'title': row['title'],
            'company': row['company'],
            'url': row['url'],
            'first_seen': row['first_seen'],
            'last_seen': row['last_seen'],
            'active': row['active'],
            **extracted
        }
        structured_data.append(combined_row)

    # Új DataFrame létrehozása és mentése
    output_df = pd.DataFrame(structured_data)
    
    # A listákat alakítsuk stringgé
    for col in output_df.columns:
        if output_df[col].apply(lambda x: isinstance(x, list)).any():
            output_df[col] = output_df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

    output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Done! Saved to {output_file}")

if __name__ == "__main__":
    main()
