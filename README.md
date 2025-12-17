# Profesia IT Job Scraper & Gemini Analyzer

The projects plan is to scrape IT job advertisements from Slovak/Hungarian sites and extract structured information from the job descriptions using Google's Gemini AI.

---

## Features

- **Web Scraper**  
  - Scrapes all IT job listings from multiple pages 
  - Saves full job descriptions in individual `.txt` files (for backup)
  - Tracks job availability with `active` and `status` fields and updates `last_seen` date.

- **Gemini AI Analyzer**  
  - Uses Google Gemini AI (`gemini-2.5-flash-lite`) to extract structured job information

---

## Usage

- **V1.0**  
 Run `Profesia_scraper.py` then `Profesia_false_check.py`. Output is in `CSV` folder.

---
