# Remote Data Jobs ETL Pipeline

Automated end-to-end ETL (Extract, Transform, Load) pipeline built in Python to collect real-time remote data job listings, clean the dataset, and store the results in multiple analytical formats.

## Architecture Flow

text
[RemoteOK Website] 
       │
       ▼ (Playwright + BeautifulSoup)
[Raw Data Extraction] 
       │
       ▼ (Pandas Cleaning & Business Rules)
[Transformed DataFrame] 
       │
       ├──► Excel Report (.xlsx)
       ├──► Parquet File (.parquet)
       ├──► SQLite Database (.db)
       └──► Execution Logs (.txt)


## Key Features
* *Dynamic Web Scraping:* Uses Playwright and BeautifulSoup to handle JavaScript-rendered job boards and extract job titles, companies, locations, and salary ranges.
* *Data Cleaning & Enrichment:* Removes duplicate postings, normalizes text fields, and creates a Salary_Disclosed business flag using Pandas.
* *Multi-Format Storage:* Exports formatted spreadsheets with auto-adjusted column widths (OpenPyXL), compressed Parquet files, and a SQLite database ready for SQL queries.
* *Modular Structure & Logging:* Separated into extract.py, transform.py, load.py, and main.py with timestamped execution logs.

## Technologies Used
* *Python 3*
* *Playwright & BeautifulSoup4*
* *Pandas & OpenPyXL*
* *SQLite3*