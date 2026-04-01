import json
import pandas as pd
from tqdm import tqdm
import time
from ollama import Client

# Kliens létrehozása 60 másodperces időkorláttal
client = Client(timeout=60.0)

def process_description(job_text, retries=1):
    model_name = "llama3.1"

    # A te eredeti system promptod
    system_prompt = """
    You are an expert HR information extraction system. Extract structured data from job descriptions.
    Return ONLY valid JSON. If a value is missing, use null.
    
    Keys to use EXACTLY:
    "Location", "Salary", "Language Requirements", "Education", 
    "Programming Languages", "Required Software / Tools", "Work Arrangement", 
    "Job Type", "Experience Level"

    Rules:
    - Location: City only.
    - Salary: Format "2000 EUR gross/month".
    - Languages: CEFR levels (e.g., ["English: B2"]).
    - Education: "High School with Diploma", "Bachelor", "Master", "PhD".
    - Work Arrangement: "On-site", "Home-Office", "Hybrid", "On-site with home office".
    - Job Type: "Full-time", "Short-term", "Half-time".
    - Experience Level: "0-1 years", "1-3 years", "3-5 years", "5+ years".
    """

    for attempt in range(retries + 1):
        try:
            response = client.generate(
                model=model_name,
                system=system_prompt,
                prompt=f"Extract structured data from this job description:\n{job_text}\n\nReturn JSON:",
                format="json",
                options={"temperature": 0}
            )

            data = json.loads(response['response'])
            
            # Ha lista érkezne vissza szótár helyett
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            return data

        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            else:
                return {}

def main():
    input_file = 'professia_jobs.csv'
    output_file = 'professia_llama.csv'

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Hiba: A '{input_file}' nem található.")
        return

    # Csak a szükséges oszlopok megtartása
    keep_columns = ['job_id','title','company', 'url', 'first_seen', 'last_seen','active', 'description']
    df = df[[col for col in keep_columns if col in df.columns]]

    structured_data = []

    print(f"\nProcessing {len(df)} jobs with Ollama (Llama 3.1)...")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        extracted = process_description(row['description'])

        # Biztonsági ellenőrzés a szótár típusra
        if not isinstance(extracted, dict):
            extracted = {}

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

        # MENTÉS 50 SORONKÉNT
        if (index + 1) % 50 == 0 or (index + 1) == len(df):
            temp_df = pd.DataFrame(structured_data)
            
            # Listák (pl. nyelvek) szöveggé alakítása vesszővel elválasztva
            for col in temp_df.columns:
                if temp_df[col].apply(lambda x: isinstance(x, list)).any():
                    temp_df[col] = temp_df[col].apply(
                        lambda x: ", ".join(map(str, x)) if isinstance(x, list) else x
                    )
            
            temp_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"\n Kész! Az eredmények mentve: {output_file}")

if __name__ == "__main__":
    main()
