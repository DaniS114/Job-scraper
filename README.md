# Job Market Intelligence Scraper

A Python-based web scraping and data analysis tool designed to archive and analyze job advertisements from major Central European job boards. This project leverages **Local LLMs** to extract insights from job descriptions without compromising data privacy.



## Features

* **Supported job portals:** 
    * **Hungary**: [profession.hu](https://www.profession.hu), [jofogas.hu](https://www.jofogas.hu)
    * **Slovakia**: [profesia.sk](https://www.profesia.sk)
* **Data Archiving**: Automatically saves every job description into a raw `.txt` file for permanent backup, ensuring you have a record even after the ad expires.
* **AI-Powered Analysis**: Uses the **Mistral-Nemo** model running locally via **Ollama** to parse requirements, tech stacks, and benefits from unstructured text.
* **Structured Output**: Generates a comprehensive CSV database containing metadata (salary, location, company).
* **Privacy**: No job data is sent to external APIs; all processing happens on your local machine.

---

## Tech Stack

* **Language**: Python 3.x
* **Libraries**: `BeautifulSoup4`, `Requests`, `Pandas`
* **Local AI**: [Ollama](https://ollama.com/)
* **Model**: `mistral-nemo` (12B parameters, 8-9GB VRAM recommended)

---

## Project Structure

```text
├── CSV/                 # Scraped data in .csv file (profession_jobs.csv)
├── Raw text/            # Permanent backup of job descriptions (.txt)
└── scraper.py           # Scraping scripts
```
## How to run