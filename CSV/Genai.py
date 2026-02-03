import os
import json
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

description = """

Open positions About us Learn & Grow We offer Open positions Deutsche Telekom IT Solutions Slovakia Senior DevOps Engineer for PACCA program Place of work Košice Region, Slovakia, Košice region (Job with occasional home office) Contract type full-time Wage (gross) From 2 600 EUR/month Final salary is negotiable. We are offering base salary depending on seniority level and previous experience of candidate. In addition to base salary we provide variable part and other financial benefits. Purpose Senior DevOps Engineer is responsible for entire lifecycle of Continuous Integration/Continuous Deployment pipelines and Infrastructure as Code approaches. Takes account and defines automated configuration management, release management, build, test and deployment activities. Provides prototypes and concepts for further automation of assigned technology. PACCA program description: Our mission with PACCA (Patch Automation Change CapAbility) is to create transparency about the patch-status of the cloud and on-premises environments. For this purpose, we will centrally roll out and automate a workflow application named IBM Concert. Besides that, the overall area provides products, services, processes to ensure cloud deployments of Deutsche Telekom IT are secured by default with a reasonable effort. The main goal is to minimize the manual invest of enabling the Privacy and Security Assessment for the applications and data. What will you do? Designs, develops, tests and implements infrastructure for CI/CD pipelines and IaC. Support of complex projects with regard to drafting, development, deployment & quality assurance up to production. Continuous integration and continuous delivery. Develop and implement strategies for automated integration and delivery of cloud-related security requirements. Work closely with our cloud landing zones with DevOps teams as your stakeholders to innovate the process efficiency and performance of the software and system landscapes. Conducts of performance analyses and tunings, as well as error analyses and troubleshooting. Consults and implements new innovative technologies to satisfy innovation strategy. Creates concepts for further automation of services, processes and/or operating models. Continuously optimizes the development and system infrastructure. Provides consulting to project teams on areas of expertise also Prototypes/Proof of Concept solutions. You will succeed if you: have secondary education of Information technologies – Master have experiences with ICT System – 4 years have experience with Scripting (Bash, Python) – Expert have experience with Linux Operating System – Expert have experience with AWS / Azure – Intermediate have experience with Docker, K8S – Advanced have experience with Kubernetes / OpenShift – Advanced have experience with Git – Expert have experience with Jenkins / GitLab – Advanced have experience with Ansible – Advanced have experience with ELK / Prometheus / Icinga /  Jaeger / Grafana – Advanced have experience with Networking - Expert have experience with Security - Advanced are communicative, team player and have analytical thinking, training skills and presentation skills speak English – Upper intermediate (B2) have experiences with Agile Methodology, Scrum and SAFe Why should you choose us? We believe in balance between work and personal life. An attractive and extensive work-life balance portfolio guarantees lasting motivation for employees and thus a better quality of life, promotes physical and mental well-being and contributes to a positive work environment. All this with the aim of providing more freedom in reconciling work, career growth, private life and individual lifestyle. Therefore we offer to our employees over 25 different benefits to improve their personal and professional life in these areas: Financial benefits Benefits with focus on learning and development * Benefits with focus on health and sport * Benefits with focus on family and work - life balance Other benefits * For more information about our benefits click to Benefits . Benefits with * are applicable also to part-time positions. This information may be subject to changes and other internal rules. Wage (gross) From 2 600 EUR/month Final salary is negotiable. We are offering base salary depending on seniority level and previous experience of candidate. In addition to base salary we provide variable part and other financial benefits. Contact Contact person: Cecilia Kotercova E-mail: send CV Apply now Deutsche Telekom IT Solutions Slovakia Moldavská cesta 8B, 040 11 Košice www.deutschetelekomitsolutions.sk DL_TSSK_HR_Recruitment@t-systems.com Apply for a job Recommend job to a friend E-mail Facebook Viber Whatsapp ID: 5101495 Dátum zverejnenia: 4.11.2025 2025-11-04 lokalita: Košice region Pozícia: Database Administrator , Systems Administrator Spoločnosť: Deutsche Telekom IT Solutions Slovakia Základná zložka mzdy (brutto): 2 600 EUR/month
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
