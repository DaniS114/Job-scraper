import ollama
import json
import pandas as pd
from tqdm import tqdm
import time

def process_description(job_text, retries=2, timeout_seconds=30):
    model_name = "llama3.1"

    system_prompt = """
    You are an expert HR information extraction system.

    Your task is to extract structured data from job descriptions.

    The input may be noisy, unstructured, multilingual (Slovak, Hungarian, English).
    You MUST extract ONLY relevant job-related information and IGNORE irrelevant text.

    ---------------------------------
    CRITICAL BEHAVIOR RULES:

    - Focus ONLY on:
      requirements, responsibilities, benefits, job details
    - IGNORE:
      GDPR text, company marketing, long introductions, legal disclaimers

    - If multiple sections exist:
      PRIORITIZE sections like:
      "Requirements", "We expect", "Candidate should have",
      "Požiadavky", "Elvárások"

    ---------------------------------
    OUTPUT RULES:

    1. Return ONLY valid JSON
    2. No explanations
    3. Missing values → null

    4. Use EXACTLY these keys:
    "Location",
    "Salary",
    "Language Requirements",
    "Suitable for",
    "Programming Languages",
    "Required Software / Tools",
    "Work Arrangement",
    "Job Type",
    "Experience Level"

    ---------------------------------
    EXTRACTION RULES:

    LOCATION:
    - Extract city only

    SALARY:
    - Convert to format:
      "2000 EUR gross/month"

    LANGUAGES:
    - Use CEFR levels if possible
    - Format:
      ["English: B2"]

    Suitable for:
      "stredoškolské s maturitou" → "High School with Diploma"
      "nadstavbové/vyššie odborné vzdelanie" → "Post-secondary / Higher Vocational"
      "vysokoškolské I. stupňa" → "Bachelor"
      "vysokoškolské II. stupňa" → "Master"
      "vysokoškolské III. stupňa" → "PhD"

    PROGRAMMING LANGUAGES:
    - Only real programming languages

    TOOLS:
    - Frameworks, tools, platforms, applications

    WORK ARRANGEMENT:
    - One of:
      "On-site"
      "Home-Office"
      "Hybrid"
      "On-site with home office"

    JOB TYPE:
    - One of:
      "Full-time"
      "Short-term"
      "Half-time"

    EXPERIENCE:
    - Format:
      "0-1 years"
      "1-3 years"
      "3-5 years"
      "5+ years"

    ---------------------------------

    IMPORTANT:
    - Do NOT guess
    - If unsure → null

    ---------------------------------

    EXAMPLE:

    {
        "Location": "Bratislava",
        "Salary": "2000 EUR gross/month",
        "Language Requirements": ["English: B2"],
        "Education Requirements": ["Bachelor", "Master"]
        "Programming Languages": ["Python", "SQL"],
        "Required Software / Tools": ["Docker", "AWS"],
        "Work Arrangement": "Hybrid",
        "Job Type": "Full-time",
        "Experience Level": "3-5 years"
    }
    """


    for attempt in range(retries + 1):
        try:
            response = ollama.generate(
                model=model_name,
                system=system_prompt,
                prompt=f"Extract structured data from this job description:\n{job_text}\n\nReturn JSON:",
                format="json",
                options={"temperature": 0},
                timeout=timeout_seconds 
            )

            return json.loads(response['response'])

        except Exception as e:
            if attempt < retries:
                print(f"\n[Hiba] Időtúllépés vagy hiba. Újrapróbálkozás ({attempt + 1}/{retries})...")
                time.sleep(2) 
                continue
            else:
                print(f"\n[Hiba] Sikertelen feldolgozás 3 próbálkozás után: {e}")
                return {}

def main():
    input_file = 'professia_jobs.csv'
    output_file = 'profesia_llama.csv'

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Hiba: A '{input_file}' nem található.")
        return

    keep_columns = ['job_id','title','company', 'url', 'first_seen', 'last_seen','active', 'description']
    df = df[[col for col in keep_columns if col in df.columns]]

    structured_data = []

    print(f"\nProcessing {len(df)} jobs with Ollama (with timeout and retries)...")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        extracted = process_description(row['description'])

        combined_row = {
            'job_id': row.get('job_id'),
            'title': row.get('title'),
            'company': row.get('company'),
            'url': row.get('url'),
            'first_seen': row.get('first_seen'),
            'last_seen': row.get('last_seen'),
            'active': row.get('active'),
            **extracted
        }

        structured_data.append(combined_row)

    output_df = pd.DataFrame(structured_data)

    for col in output_df.columns:
        if output_df[col].apply(lambda x: isinstance(x, list)).any():
            output_df[col] = output_df[col].apply(
                lambda x: ", ".join(map(str, x)) if isinstance(x, list) else x
            )

    output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Done! Saved to {output_file}")

if __name__ == "__main__":
    main()
