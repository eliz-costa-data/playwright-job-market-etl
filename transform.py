import pandas as pd


def transform_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw job postings data: removes duplicates, strips extra whitespace,
    and flags whether salary information was disclosed.
    """
    if df.empty:
        return df

    # 1. Remove duplicate job listings based on title and company
    df = df.drop_duplicates(subset=["Job_Title", "Company"]).copy()

    # 2. Clean leading/trailing whitespace from text columns
    for col in ["Job_Title", "Company", "Location", "Salary"]:
        df[col] = df[col].astype(str).str.strip()

    # 3. Create a business flag indicating if the salary is disclosed
    df["Salary_Disclosed"] = df["Salary"].apply(
        lambda x: "No" if x == "Not Disclosed" else "Yes"
    )

    return df