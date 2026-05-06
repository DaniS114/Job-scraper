# Job Scraper and Analyzer

Ez a projekt informatikai álláshirdetések automatizált gyűjtésére, feldolgozására és elemzésére készült.  
A rendszer web scraping segítségével álláshirdetéseket gyűjt különböző állásportálokról, majd a hirdetések szöveges leírását mesterséges intelligencia segítségével strukturált adatformátumba alakítja. Az így kapott adatok később statisztikai elemzésre és grafikonok készítésére használhatók.

A projekt célja annak vizsgálata, hogy az informatikai álláshirdetésekben milyen technológiák, programozási nyelvek, nyelvi követelmények, tapasztalati szintek és munkavégzési formák jelennek meg leggyakrabban.

## Fő funkciók

- álláshirdetések gyűjtése web scraping segítségével,
- hirdetések alapadatainak mentése CSV formátumban,
- hirdetések teljes szövegének mentése TXT fájlokba,
- mesterséges intelligencia alapú információkinyerés,
- Gemini API és lokálisan futtatott modellek támogatása,
- feldolgozott CSV fájlok egyesítése,
- adatok normalizálása,
- statisztikai kimutatások és grafikonok készítése.

## Használt technológiák

A projekt Python nyelven készült. A főbb használt könyvtárak:

- `requests` – weboldalak lekérésére,
- `beautifulsoup4` – HTML tartalom feldolgozására,
- `pandas` – CSV fájlok és táblázatos adatok kezelésére,
- `matplotlib` – grafikonok készítésére,
- `tqdm` – feldolgozási folyamat kijelzésére,
- `google-genai` – Gemini API használatához,
- `ollama` – lokális nyelvi modellek Pythonból történő futtatásához.

## Telepítés

### 1. Python telepítése

A projekt futtatásához Python szükséges.  
Ajánlott verzió: Python 3.10 vagy újabb.

Python letöltése:  
https://www.python.org/downloads/

A telepítés után ellenőrizhető:

```bash
python --version
```

### 2. Python könyvtárak telepítése

A szükséges könyvtárak telepíthetők a következő paranccsal:

```bash
pip install requests beautifulsoup4 pandas matplotlib tqdm google-genai ollama
```

### 3. Gemini API használata

A Gemini API használatához Google AI Studio API kulcs szükséges.

Google AI Studio:  
https://aistudio.google.com/

Az API kulcsot környezeti változóként kell beállítani.

Windows PowerShell-ben:

```powershell
$env:GEMINI_API_KEY="SAJAT_API_KULCS"
```

Linux / macOS alatt:

```bash
export GEMINI_API_KEY="SAJAT_API_KULCS"
```

### 4. Ollama telepítése lokális modellekhez

A lokális nyelvi modellek futtatásához Ollama szükséges.

Ollama letöltése:  
https://ollama.com/download

Telepítés után ellenőrizhető:

```bash
ollama --version
```

A használt modellek letöltése például:

```bash
ollama pull qwen2.5:7b-instruct
ollama pull mistral-nemo
ollama pull llama3.1
```

A lokális modellek futtatása több memóriát és számítási kapacitást igényelhet. Lassabb gépen a feldolgozás jelentősen hosszabb ideig tarthat.

## Projektstruktúra

A mellékelt projekt így épül fel:

```text
Job-scraper/
│
├── Profesia_scraper.py
├── Profesia_false_check.py
├── profession_scraper.py
├── cvonline_scraper.py
│
├── CSV/
│   ├── professia_jobs.csv
│   ├── profession_jobs.csv
│   ├── cvonline_jobs.csv
│   ├── Gemini_api.py
│   ├── LocalLM.py
│   └── Processed_csv/
│        ├── profesia_gemini.csv
│        ├── profession_gemini.csv
│        ├── cvonline_gemini.csv
│        └── ...
│
├── Analyze/
│   ├── Merge.py
│   ├── Analyzer.py
│   └── Analyzed/
│        ├── all_programming_languages.csv
│        ├── all_tools.csv
│        ├── all_human_languages.csv
│        ├── all_experience_levels.csv
│        ├── all_work_arrangement.csv
│        ├── all_job_types.csv
│        ├── all_locations.csv
│        ├── all_programming_languages.png
│        ├── all_tools.png
│        └── ... 
│
└── Raw text/
    ├── job_id_1.txt
    ├── job_id_2.txt
    └── ...
```

## Mappák szerepe

### Fő mappa

A fő mappában találhatók a scraping scriptek. Ezek felelősek az álláshirdetések begyűjtéséért az egyes állásportálokról.

### CSV mappa

A `CSV` mappa tartalmazza a scraperek kimeneteit, vagyis az állásportálokról kinyert alapadatokat CSV formátumban.

Ebben a mappában találhatók az AI-feldolgozást végző scriptek is:

- `Gemini_api.py` – Gemini API-val történő feldolgozás,
- `LocalLM.py` – lokális modellekkel történő feldolgozás.

Ezek kimenetei a `Processed_csv` mappába kerülnek.

### Processed_csv mappa

A `Processed_csv` mappa tartalmazza a mesterséges intelligencia által feldolgozott CSV fájlokat.

Ezek már strukturált adatokat tartalmaznak, például:

- munkavégzés helye,
- fizetés,
- nyelvi követelmények,
- programozási nyelvek,
- használt eszközök és technológiák,
- munkavégzés módja,
- tapasztalati szint.

### Analyze mappa

Az `Analyze` mappában találhatók az elemzéshez kapcsolódó scriptek:

- `Merge.py` – a feldolgozott CSV fájlok egyesítésére szolgál,
- `Analyzer.py` – az adatok normalizálását, összesítését és vizualizációját végzi.

### Analyzed mappa

Az `Analyzed` mappa tartalmazza az elemzés eredményeit:

- összesítő CSV fájlokat,
- diagramokat PNG formátumban.

### Raw text mappa

A `Raw text` mappába kerülnek az álláshirdetések teljes szöveges leírásai TXT fájlokként.  
A fájlnevek az álláshirdetések egyedi azonosítója (`job_id`) alapján készülnek.

Ez azért hasznos, mert így a hirdetés teljes szövege akkor is visszakereshető marad, ha az eredeti álláshirdetés később már nem érhető el az adott portálon.

## Használat

### 1. Adatgyűjtés futtatása

A scraperek külön-külön futtathatók az egyes portálokhoz.

Példa:

```bash
python professia_scraper.py
```

```bash
python profession_scraper.py
```

```bash
python cvonline_scraper.py
```

A futtatás után létrejönnek vagy frissülnek a `CSV` mappában található CSV fájlok, valamint a `Raw text` mappában a hirdetések teljes szövegét tartalmazó TXT fájlok.

A `Profesia_false_check.py` kiegészítő scriptként volt használatos. Feladata, hogy a korábban inaktívként jelölt Profesia hirdetések URL-jeit újra ellenőrizze, és frissítse azok állapotát, azonban erre már nincs szükség.

### 2. Gemini API alapú feldolgozás

A Gemini API használata előtt be kell állítani a `GEMINI_API_KEY` környezeti változót.

Ezután futtatható:

```bash
python Gemini_api.py
```

A script beolvassa a scraping során létrehozott CSV fájlt, feldolgozza a hirdetések leírását, majd a strukturált adatokat a `Processed_csv` mappába menti.

### 3. Lokális modell alapú feldolgozás

A lokális feldolgozás előtt telepíteni kell az Ollamát, majd le kell tölteni a használni kívánt modellt.

Példa:

```bash
ollama pull qwen2.5:7b-instruct
```

Ezután futtatható:

```bash
python LocalLM.py
```

A használt modell a scriptben a `model_name` változó módosításával állítható be.

Példa:

```python
model_name = "qwen2.5:7b-instruct"
```

Másik modell használatához a változó értékét kell módosítani, például:

```python
model_name = "mistral-nemo"
```
### 4. Feldolgozott CSV fájlok másolása

Az elemzés előtt a `CSV/Processed_csv` mappából át kell másolni vagy át kell helyezni azokat a feldolgozott CSV fájlokat az `Analyze` mappába, amelyeket elemezni szeretnénk.

Például:

```text
CSV/Processed_csv/profesia_gemini.csv     ->  Analyze/profesia_gemini.csv
CSV/Processed_csv/profession_gemini.csv   ->  Analyze/profession_gemini.csv
CSV/Processed_csv/cvonline_gemini.csv     ->  Analyze/cvonline_gemini.csv
```

### 5. Feldolgozott CSV fájlok egyesítése

Az AI által feldolgozott CSV fájlok egyesítéséhez az `Analyze` mappában található `Merge.py` script futtatása szükséges.

```bash
python Merge.py
```

Ez létrehozza az egyesített adatállományt, például:

```text
all_jobs_with_source.csv
```

Ebben az állományban már szerepel a `source` oszlop is, amely megmutatja, hogy az adott hirdetés melyik portálról származik.

### 6. Elemzés és grafikonok készítése

Az elemzéshez az `Analyzer.py` script futtatása szükséges:

```bash
python Analyzer.py
```

A script elvégzi:

- az adatok normalizálását,
- gyakorisági kimutatások készítését,
- forrásonkénti összesítést,
- grafikonok generálását.

Az eredmények az `Analyzed` mappába kerülnek.

## Fontos megjegyzések

- A weboldalak HTML struktúrája idővel változhat, ezért előfordulhat, hogy a scraperek később módosítást igényelnek.
- A mesterséges intelligencia által előállított eredmények információs jellegűek, és kisebb pontatlanságokat tartalmazhatnak.
- A lokális modellek lassabban futnak, és nagyobb hardverigényük lehet.
- A Gemini API használatához internetkapcsolat és érvényes API kulcs szükséges.
- A lokális modellek használatához az Ollama telepítése és a modellek előzetes letöltése szükséges.

## Javasolt futtatási sorrend

```text
1. Scraper futtatása
2. Gemini vagy lokális AI feldolgozás
3. Az elemzendő CSV fájlok átmásolása
4. Feldolgozott CSV fájlok egyesítése
5. Elemzés és grafikonok generálása
```

## Projekt célja röviden

A projekt célja annak bemutatása, hogy web scraping és mesterséges intelligencia segítségével nagy mennyiségű informatikai álláshirdetés automatizáltan feldolgozható és elemezhető. Az így létrejött adathalmaz alkalmas munkaerőpiaci trendek vizsgálatára, valamint az informatikai területen történő sikeres elhelyezkedéshez szükséges készségek és technológiák azonosítására.

A projekt oktatási célból, szakdolgozat részeként készült.