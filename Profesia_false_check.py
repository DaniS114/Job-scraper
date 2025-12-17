import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import date

csv_path = "CSV/professia_jobs.csv"

df = pd.read_csv(csv_path)

# Csak nem aktív sorok
inactive_df = df[df["active"] == False]

for index, row in inactive_df.iterrows():

    url = row["url"]
    job_id = row["job_id"]

    print(f"Ellenőrzés: {job_id} | {url}")

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            df.at[index, "status"] = "expired"
            print("Nem elérhető az oldal")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # taken prompt keresése
        taken_box = soup.select_one("#detail > div.alert.alert-warning.alert-dismissible.fade.in")

        if taken_box:
            # van taken prompt
            df.at[index, "status"] = "taken"
            print("Taken (már nem aktív hirdetés)")
            continue

        #nincs taken prompt
        df.at[index, "active"] = True
        df.at[index, "status"] = "active"
        df.at[index, "last_seen"] = date.today().isoformat()
        print(f"Újra aktív a hirdetés — last_seen frissítve")

    except Exception as e:
        df.at[index, "status"] = "expired"
        print(f"Hiba: {e}")

# CSV mentése
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print("\nA státuszok frissítve.")
