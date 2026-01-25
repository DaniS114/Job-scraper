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
csv_path = os.path.join(csv_folder, "jofogas_jobs.csv")

base_url = "https://allas.jofogas.hu/magyarorszag/it-telekommunikacio/magyarorszag"
headers = {"User-Agent": "Mozilla/5.0"}

#CSV betöltése vagy létrehozása
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=[
        "job_id", "title", "company", "url",
        "first_seen", "last_seen", "active", "status", "description"
    ])

today = date.today().isoformat()
found_ids = []

#Lapozás
page_num = 1
while True:
    url = f"{base_url}?o={page_num}"
    print(f"\nFeldolgozás: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Hiba az oldal lekérésénél: HTTP {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    
    job_items = soup.select("h3.item-title a.subject")
    if not job_items:
        print("Nincs több oldal.")
        break

    print(f"Hirdetések ezen az oldalon: {len(job_items)}")

    for job in job_items:
        job_url = job["href"]
        job_id = job_url.split("_")[-1].replace(".htm", "")
        title = job.get_text(strip=True)
        company = "N/A" # nincs mindenhol megadva
        found_ids.append(job_id)

        text_path = os.path.join(text_folder, f"{job_id}.txt")
        job_text = ""

        #Lekérés és szöveg kinyerés
        if not os.path.exists(text_path):
            try:
                job_response = requests.get(job_url, headers=headers, timeout=10)
                if job_response.status_code == 200:
                    job_soup = BeautifulSoup(job_response.text, "html.parser")

                    # Fő leírás
                    description = job_soup.find("div", {"data-testid": "real-estate-product-description-collapse"})
                    if description:
                        p = description.find("p")
                        if p:
                            job_text += p.get_text(strip=True) + "\n"

                    # Információk
                    properties = job_soup.find("div", id="ad-information-card")
                    if properties:
                        job_text += properties.get_text(separator="\n", strip=True) + "\n"

                    # Elvárások
                    reqs = job_soup.find("div", {"data-testid": "properties-container"})
                    if reqs:
                        for param in reqs.find_all("div", recursive=False):
                            caption = param.find("span")
                            value = param.find("h6")
                            line = (caption.get_text(strip=True) if caption else '') + (value.get_text(strip=True) if value else '')
                            line = line.strip()

                            if line:
                                job_text += line + "\n"

                    # Mentés TXT-be
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

            time.sleep(0.2)
        else:
            #meglévő leírás beolvasása
            try:
                with open(text_path, "r", encoding="utf-8") as f:
                    job_text = f.read()
                print(f"Már létezik: {text_path}")
            except Exception as e:
                print(f"Nem sikerült beolvasni {text_path}: {e}")
                job_text = ""
        job_text_csv = job_text.replace("\n", " ").replace("\r", " ").strip()
        
        #CSV frissítése
        if job_id in df["job_id"].astype(str).values:
            # már létezik
            df.loc[df["job_id"].astype(str) == job_id, ["last_seen", "active", "status", "description"]] = [
                       today, True, "active", job_text_csv
                   ]
        else:
            # új hirdetés
            df.loc[len(df)] = [
                job_id, title, company, job_url,
                today, today, True, "active", job_text_csv
            ]

    page_num += 1
    time.sleep(0.3)

# --- Inaktiválás ---
if found_ids:
    df.loc[~df["job_id"].astype(str).isin(found_ids),
           ["active", "status"]] = [False, "inactive"]

# --- CSV mentés ---
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print("\nKÉSZ! CSV és TXT fájlok frissítve!")
