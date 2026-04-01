import os
import json
import pandas as pd
from tqdm import tqdm
from google import genai
from google.genai import types

#API kliens inicializálása környezeti változóból
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

def process_description_gemini(job_text, retries=1):
    """Feldolgozás Geminivel."""
    model_name = "models/gemini-2.5-flash-lite" 

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

    if not isinstance(job_text, str) or len(job_text) < 10:
        return {}

    for attempt in range(retries + 1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=f"{system_prompt}\n\nJob Description:\n{job_text[:8000]}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0
                )
            )
            return json.loads(response.text)
        except Exception:
            if attempt < retries:
                continue
            else:
                return {}

def main():
    input_file = 'professia_jobs.csv'

    output_folder = 'Processed_csv'
    output_filename = 'profesia_gemini.csv'    

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Mappa létrehozva: {output_folder}")
    output_file = os.path.join(output_folder, output_filename)
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Hiba: A '{input_file}' nem található.")
        return

    #Szükséges oszlopok megtartása
    keep_columns = ['job_id','title','company', 'url', 'first_seen', 'last_seen','active', 'description']
    df = df[[col for col in keep_columns if col in df.columns]]

    structured_data = []
    
    print(f"\nIndul a feldolgozás (4k RPM limit): {len(df)} hirdetés...")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        extracted = process_description_gemini(row['description'])

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
        
        #Biztonsági mentés 100 soronként
        if (index + 1) % 100 == 0:
            pd.DataFrame(structured_data).to_csv(output_file, index=False, encoding='utf-8-sig')

    # Végső formázás és mentés
    output_df = pd.DataFrame(structured_data)
    # Listák szöveggé alakítása vesszővel elválasztva
    for col in output_df.columns:
        if output_df[col].apply(lambda x: isinstance(x, list)).any():
            output_df[col] = output_df[col].apply(
                lambda x: ", ".join(map(str, x)) if isinstance(x, list) else x
            )

    output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nKÉSZ! Összesen {len(output_df)} hirdetés feldolgozva.")

if __name__ == "__main__":
    main()
