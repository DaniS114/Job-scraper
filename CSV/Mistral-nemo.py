import ollama
import json
import pandas as pd
from tqdm import tqdm # Progress barhoz: pip install tqdm

def process_description(job_text):
    model_name = "mistral-nemo" 

    system_prompt = """
    You are a professional HR data extraction assistant. 
    Your task is to analyze the provided job description and extract information in ENGLISH.
    If the input text is in another language, translate the extracted information to English.
    
    You MUST return ONLY a valid JSON object.
    Use exactly these keys:
    "Job Title", "Location", "Salary", "Language Requirements", "Education Requirements", 
    "Programming Languages", "Required Software / Tools", "Work Arrangement", 
    "Job Type", "Experience Level", "Company Name"

    Guidelines:
    - If a value is not mentioned, use null.
    - Salary: amount + currency + gross/net (e.g., "3000 EUR gross")
    - Language Requirements: Language + level as a list.
    -"Job Type" Full-time/Short-term/Half-Time
    -"Work Arrangement" On-site/Home-Office/Hybrid/On-site with home office.
    -"Education Requirements" Basic/University + degree+ field.
    -"Language Requirements" Language+level
    -"Location" City Name
    """

    try:
        response = ollama.generate(
            model=model_name,
            system=system_prompt,
            prompt=f"Extract info: {job_text}",
            format="json",
            options={"temperature": 0}
        )
        return json.loads(response['response'])
    except Exception as e:
        print(f"Error processing row: {e}")
        return {}

def main():
    input_file = 'professia_jobs.csv'
    output_file = 'structured_jobs.csv'

    # CSV beolvasása
    df = pd.read_csv(input_file).head(100)
    
    # Csak azokat a mezőket tartjuk meg, amiket kértél + a description az LLM-nek
    keep_columns = ['job_id', 'url', 'first_seen', 'last_seen','active', 'description']
    df = df[keep_columns]

    structured_data = []

    print(f"\nProcessing {len(df)} jobs with Ollama...")
    
    # tqdm mutatja a haladást a terminálban
    for index, row in tqdm(df.iterrows(), total=len(df)):
        extracted = process_description(row['description'])
        
        # Alapadatok + kinyert adatok összefésülése
        combined_row = {
            'job_id': row['job_id'],
            'url': row['url'],
            'first_seen': row['first_seen'],
            'last_seen': row['last_seen'],
            'active': row['active'],
            **extracted # Ez kibontja a JSON kulcsokat oszlopokká
        }
        structured_data.append(combined_row)

    # Új DataFrame létrehozása és mentése
    output_df = pd.DataFrame(structured_data)
    
    # A listákat (pl. Programming Languages) alakítsuk stringgé, hogy a CSV ne törjön meg
    for col in output_df.columns:
        if output_df[col].apply(lambda x: isinstance(x, list)).any():
            output_df[col] = output_df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

    output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Done! Saved to {output_file}")

if __name__ == "__main__":
    main()
