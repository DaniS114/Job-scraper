import pandas as pd

# Olvasd be mindkettőt
eredeti = pd.read_csv('hianyzo_hirdetesek.csv')
kesz = pd.read_csv('profesia_gemini_tisztitott2.csv')

# Nézzük meg a darabszámot
print(f"Eredeti: {len(eredeti)}")
print(f"Kész: {len(kesz)}")

# Keressük meg a hiányzókat a job_id alapján (feltéve, hogy egyediek)
hiányzó_idk = set(eredeti['job_id']) - set(kesz['job_id'])
print(f"Hiányzó hirdetések száma: {len(hiányzó_idk)}")

# Mentsük ki a hiányzókat egy külön listába, hogy csak azokat kelljen újrafuttatni
missing_df = eredeti[eredeti['job_id'].isin(hiányzó_idk)]
missing_df.to_csv('hianyzo_hirdetesek2.csv', index=False)
print("A hiányzó sorok mentve: hianyzo_hirdetesek.csv")
