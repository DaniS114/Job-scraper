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
csv_path = os.path.join(csv_folder, "professia_jobs.csv")

base_url = "https://www.profesia.sk/praca/informacne-technologie/"

#CSV betöltése vagy létrehozása
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=[
        "job_id", "title", "company", "url", "first_seen",
        "last_seen", "active", "status", "description"
    ])

today = date.today().isoformat()
found_ids = []

#Lapozás
page_num = 1
while True:
    if page_num == 1:
        url = base_url
    else:
        url = f"{base_url}?page_num={page_num}"

    print(f"\nFeldolgozás: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Hiba a oldal lekérésénél: HTTP {response.status_code}.")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    job_items = soup.find_all("li", class_="list-row")
    if not job_items:
        print("Nincs több oldal.")
        break

    print(f"Hirdetések ezen az oldalon: {len(job_items)}")

    for job in job_items:
        h2_tag = job.find("h2")
        if not h2_tag:
            continue

        link_tag = h2_tag.find("a")
        if not link_tag or "href" not in link_tag.attrs:
            continue

        job_url = "https://www.profesia.sk" + link_tag["href"]
        href_part = link_tag["href"].split("/")[-1].split("?")[0]
        job_id = href_part.lstrip("O")  # eltávolítja az 'O'-t, ha van
        found_ids.append(job_id)

        title = link_tag.get_text(strip=True)
        company_tag = job.find("span", class_="employer")
        company = company_tag.get_text(strip=True) if company_tag else "N/A"

        text_path = os.path.join(text_folder, f"{job_id}.txt")
        job_text = ""

        if not os.path.exists(text_path):
            try:
                job_response = requests.get(job_url, timeout=10)
                if job_response.status_code == 200:
                    job_soup = BeautifulSoup(job_response.text, "html.parser")
                    detail_main = job_soup.find("main", id="detail")
                    if detail_main:
                        job_text = detail_main.get_text(separator="\n", strip=True)
                        with open(text_path, "w", encoding="utf-8") as f:
                            f.write(job_text)
                        print(f"Mentve új hirdetés: {text_path}")
                    else:
                        print(f"Nincs #detail a hirdetésben: {job_url}")
                else:
                    print("Hirdetés oldal nem elérhető")
            except requests.RequestException as e:
                print(f"Hiba lekéréskor ({job_url}): {e}")
            time.sleep(0.1)
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
                job_id, title, company, job_url, today, today, True, "active", job_text_csv
            ]

    page_num += 1
    time.sleep(0.2)

#Inaktiválás: amit most nem talált meg
if found_ids:
    df.loc[~df["job_id"].astype(str).isin(found_ids), ["active", "status"]] = [False, "inactive"]
else:
    print("Nincs hirdetést a lapozás során.")

#CSV mentés
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print("\nKÉSZ! CSV és TXT fájlok frissítve.")
