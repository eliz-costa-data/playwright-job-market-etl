from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd


def extract_jobs(url: str) -> pd.DataFrame:
    """
    Opens the RemoteOK data jobs page using Playwright, waits for dynamic
    content to load, and extracts job title, company, location, and salary.
    """
    jobs_list = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            # Navigate to the target URL and wait until network traffic settles
            page.goto(url, wait_until="networkidle", timeout=60000)

            # Scroll down slightly to ensure lazy-loaded job rows render
            page.evaluate("window.scrollTo(0, 1500)")
            page.wait_for_timeout(2000)

            html_content = page.content()
            browser.close()

        soup = BeautifulSoup(html_content, "html.parser")
        job_rows = soup.find_all("tr", class_="job")

        for row in job_rows:
            title_tag = row.find("h2", itemprop="title")
            company_tag = row.find("h3", itemprop="name")
            location_tags = row.find_all("div", class_="location")

            title = title_tag.get_text(strip=True) if title_tag else None
            company = company_tag.get_text(strip=True) if company_tag else None

            # Extract location and salary if available inside location divs
            location = "Remote"
            salary = "Not Disclosed"
            for tag in location_tags:
                text = tag.get_text(strip=True)
                if "Upgrade to Premium" in text:
                    salary = "Not Disclosed"
                elif "$" in text or "€" in text:
                     salary = text
                elif text and "Contractor" not in text and "Part time" not in text:
                    location = text

            if title and company:
                jobs_list.append({
                    "Job_Title": title,
                    "Company": company,
                    "Location": location,
                    "Salary": salary
                })

    except Exception as e:
        print(f"Error during extraction: {e}")

    return pd.DataFrame(jobs_list)