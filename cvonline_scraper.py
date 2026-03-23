import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd
from datetime import date

#Beállítások
text_folder = "Raw text"
csv_folder = "CSV"
os.makedirs(text_folder, exist_ok=True)
os.makedirs(csv_folder, exist_ok=True)
csv_path = os.path.join(csv_folder, "cvonline_jobs.csv")

base_url = "https://www.cvonline.hu/hu/allashirdetesek/it-informatika-0"
headers = {"User-Agent": "Mozilla/5.0"}

# CSV betöltése vagy létrehozása
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=[
        "job_id", "title", "company", "url", "first_seen",
        "last_seen", "active", "status", "description"
    ])

today = date.today().isoformat()
found_ids = []

# Lapozás
page_num = 0
while True:
    url = base_url if page_num == 0 else f"{base_url}?page={page_num}"
    print(f"\nFeldolgozás: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Hiba az oldal lekérésénél: HTTP {response.status_code}.")
            break
    except Exception as e:
        print(f"Kapcsolati hiba: {e}")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    job_items = soup.find_all("article", class_="node--job-per-template")
    if not job_items:
        print("Nincs több oldal vagy üres az oldal.")
        break

    print(f"Hirdetések az oldalon: {len(job_items)}")

    for job in job_items:
        job_id_2 = job.get("id")
        if not job_id_2:
            continue
        job_id = job_id_2.replace("node-", "").strip()
        found_ids.append(job_id)

        title_tag = job.find("h2", class_="node__title")
        a_tag = title_tag.find("a")
        title = a_tag.get_text(strip=True)
        job_url = a_tag["href"]

        company_tag = job.find("span", class_="recruiter-company-profile-job-organization")
        company = company_tag.get_text(strip=True) if company_tag else "N/A"

        text_path = os.path.join(text_folder, f"{job_id}.txt")
        job_text = ""

        if not os.path.exists(text_path):
            try:
                job_response = requests.get(job_url, headers=headers, timeout=10)
                if job_response.status_code == 200:
                    job_soup = BeautifulSoup(job_response.text, "html.parser")

                    #Leírások kinyerése és egybefűzése
                    desc_parts = []
                    
                    pot_selectors = [
                        '.markup_desc', 
                        '.unique_template', 
                        '.field--name-body .field__item', 
                        '.field--name-field-job-requirements .field__item', 
                        '.field--name-field-job-benefits .field__item',
                        '.field--name-field-job-description .field__item'
                    ]
                    
                    for selector in pot_selectors:
                        elements = job_soup.select(selector)
                        for element in elements:                                
                            text = element.get_text(separator="\n", strip=True)
                            if text and text not in desc_parts:
                                desc_parts.append(text)

                    job_text = "\n\n".join(desc_parts).strip()


                    if job_text:
                        with open(text_path, "w", encoding="utf-8") as f:
                            f.write(job_text)
                        print(f"Mentve új hirdetés: {text_path}")
                    else:
                        print(f"Nem található leírás: {job_url}")

                else:
                    print(f"Hirdetés oldal hiba: {job_response.status_code}")
            except Exception as e:
                print(f"Hiba a hirdetés feldolgozásakor ({job_url}): {e}")
            
            time.sleep(0.3)
        else:
            try:
                with open(text_path, "r", encoding="utf-8") as f:
                    job_text = f.read()
                print(f"Már létezik: {job_id}")
            except Exception as e:
                print(f"Beolvasási hiba {text_path}: {e}")
                job_text = ""


        job_text_csv = job_text.replace("\n", " ").replace("\r", " ").strip()

        # CSV frissítése
        job_id_str = str(job_id)
        if job_id_str in df["job_id"].astype(str).values:
            df.loc[df["job_id"].astype(str) == job_id_str, 
                   ["last_seen", "active", "status", "description"]] = [today, True, "active", job_text_csv]
        else:
            df.loc[len(df)] = [
                job_id, title, company, job_url,
                today, today, True, "active", job_text_csv
            ]

    page_num += 1
    time.sleep(0.1)

# Inaktiválás kezelése
if found_ids:
    found_ids_str = [str(fid) for fid in found_ids]
    df.loc[~df["job_id"].astype(str).isin(found_ids_str), ["active", "status"]] = [False, "inactive"]

# CSV mentés
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print("\nKÉSZ! Az adatbázis és a TXT-k frissítve lettek.")
