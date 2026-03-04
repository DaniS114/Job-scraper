import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from datetime import date
import time

# Beállítások
text_folder = "Raw text"
csv_folder = "CSV"
os.makedirs(text_folder, exist_ok=True)
os.makedirs(csv_folder, exist_ok=True)
csv_path = os.path.join(csv_folder, "profession_jobs.csv")

base_url = "https://www.profession.hu/allasok/it-programozas-fejlesztes"
headers = {"User-Agent": "Mozilla/5.0"}

# CSV betöltése vagy létrehozása
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=[
        "job_id", "title", "company", "url",
        "first_seen", "last_seen", "active", "status", "description"
    ])

today = date.today().isoformat()
found_ids = []

# Lapozás
page_num = 1
while True:
    url = f"{base_url}/{page_num},10"
    print(f"\nFeldolgozás: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Hiba az oldal lekérésénél: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    job_items = soup.select("li.advertisement-result-list-item")
    if not job_items:
        print("Nincs több oldal.")
        break

    print(f"Hirdetések találtak az oldalon: {len(job_items)}")

    for job in job_items:
        job_id = job.get("data-prof-id")
        job_url = job.get("data-link")
        title = job.get("data-item-name")
        company = job.get("data-item-brand")
        found_ids.append(job_id)

        text_path = os.path.join(text_folder, f"{job_id}.txt")
        job_text = ""

        # Hirdetés szöveg mentése TXT-be
        if not os.path.exists(text_path):
            try:
                job_response = requests.get(job_url, headers=headers, timeout=10)
                if job_response.status_code == 200:
                    job_soup = BeautifulSoup(job_response.text, "html.parser")
                    
                    all_details = []

                    job_details = job_soup.select_one("ul.job-details-list")
                    if job_details:
                        all_details.append(job_details.get_text(separator="\n", strip=True))

                    job_details2 = job_soup.select_one(".side-box-about-the-job")
                    if job_details2:
                        all_details.append(job_details2.get_text(separator="\n", strip=True))

                    job_description = job_soup.select_one('section[aria-labelledby="job-description"], .custom-template, #adv, #sablon, .job-ad__body')
                    if job_description:
                        for trash in job_description(["style", "script"]):
                            trash.decompose()
                        all_details.append(job_description.get_text(separator="\n", strip=True))

                    job_text = "\n\n".join(all_details)

                    if job_text:
                        with open(text_path, "w", encoding="utf-8") as f:
                            f.write(job_text.strip())
                        print(f"Mentve: {text_path}")
                    else:
                        print(f"Nincs szöveg: {job_url}")
                else:
                    print(f"Hirdetés nem elérhető: {job_url}")

            except requests.RequestException as e:
                print(f"Hiba lekéréskor ({job_url}): {e}")

            time.sleep(0.1)
        else:
            try:
                with open(text_path, "r", encoding="utf-8") as f:
                    job_text = f.read()
                print(f"Már létező TXT hirdetés: {text_path}")
            except Exception as e:
                print(f"Nem sikerült beolvasni {text_path}: {e}")
                job_text = ""
        
        # CSV-be szánt verzió (egy sorba tördelve)
        job_text_csv = job_text.replace("\n", " ").replace("\r", " ").strip()

        # CSV frissítés
        if job_id in df["job_id"].astype(str).values:
            df.loc[df["job_id"].astype(str) == job_id,
                   ["last_seen", "active", "status", "description"]] = [
                       today, True, "active", job_text_csv
                   ]
            print(f"CSV frissítve: {job_id}")
        else:
            df.loc[len(df)] = [
                job_id, title, company, job_url,
                today, today, True, "active", job_text_csv
            ]

    page_num += 1
    time.sleep(0.1)

# Inaktiválás kezelése
if found_ids:
    df.loc[~df["job_id"].astype(str).isin(found_ids), ["active", "status"]] = [False, "inactive"]
    print(f"\nInaktív hirdetések frissítve.")

# CSV mentés
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print("\nKÉSZ! Az adatbázis és a TXT-k frissítve lettek.")
