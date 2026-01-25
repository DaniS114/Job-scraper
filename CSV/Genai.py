import os
import json
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

description = """
A munkatárstól elvárás, kreativitás, szorgalom, aktivitás, az új ismeretek befogadása. Bruttó bér: 400 000 Ft / hó Cím: Budapest ; II. kerület Kategória: Állásajánlatok, álláskeresés ; Állásajánlat ; IT / telekommunikáció Feladás dátuma: jan 22., 15:36 Üzleti felhasználó Elvárt végzettség: középiskola Cégnév: Rózsadomb Contact Kft Szükséges nyelvtudás: angol Jelentkezéshez szükséges dokumentumok: fényképes önéletrajz Munkakör megnevezése: Egyéb Tapasztalat: Pályakezdő Foglalkoztatás jellege: Teljes munkaidő
...
"""

# 1. Define the keys clearly in the prompt to ensure consistency for your CSV
prompt = f"""
Extract data from the job advertisement into a valid JSON object. Translate everything to english except names and titles.
Use exactly these keys:
- "Job Title"
- "Location" -city
- "Salary" - only number and EUR and brutto/netto
- "Language Requirements" language - level only
- "Education Requirements" 
- "Programming Languages"
- "Required Software / Tools"
- "Work Arrangement"
- "Job Type"
- "Experience Level" years for example or junior/senior...
- "Company Name"

For lists (like languages), use an array of strings.
If information is missing, use null.

Job advertisement text:
{description}
"""

# 2. Use configuration to force JSON MIME type
response = client.models.generate_content(
    model="models/gemini-2.5-flash-lite",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

print("RAW RESPONSE (Before cleaning):")
print(response.text)
'''
# 3. Clean the response text (remove ```json and ```)
cleaned_text = response.text.strip()
if cleaned_text.startswith("```json"):
    cleaned_text = cleaned_text[7:]
if cleaned_text.startswith("```"):
    cleaned_text = cleaned_text[3:]
if cleaned_text.endswith("```"):
    cleaned_text = cleaned_text[:-3]

cleaned_text = cleaned_text.strip()

try:
    data = json.loads(cleaned_text)
    print("\n✅ PARSED JSON SUCCESS:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # 4. PREPARE FOR CSV (Flatten lists)
    # Lists (like ['Python', 'Java']) break CSVs. Join them with commas.
    csv_row = {
        "Job Title": data.get("Job Title"),
        "Location": data.get("Location"),
        "Salary": data.get("Salary"),
        "Education Requirements": data.get("Education Requirements"),
        # Join lists into a single string for CSV cells:
        "Programming Languages": ", ".join(data.get("Programming Languages", [])or []),        
        "Language Requirements": ", ".join(data.get("Language Requirements", []) or []),
        "Company Name": data.get("Company Name")
    }
    
    print("\nExample CSV Row Dictionary:")
    print(csv_row)

except json.JSONDecodeError as e:
    print(f"❌ JSON Decode Error: {e}")
    print("Cleaned text was:", cleaned_text)
'''
