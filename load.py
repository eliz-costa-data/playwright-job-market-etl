import pandas as pd
import sqlite3
from datetime import datetime


def log_progress(message: str, log_file: str = "pipeline_log.txt") -> None:
    """Appends a timestamped progress message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} : {message}\n")


from openpyxl.utils import get_column_letter

def load_to_excel(df: pd.DataFrame, excel_path: str) -> None:
    """Saves the cleaned DataFrame to an Excel file with exact max column widths."""
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Jobs")
        worksheet = writer.sheets["Jobs"]
        for idx, col in enumerate(df.columns, 1):
            exact_max = max(df[col].astype(str).map(len).max(), len(col))
            worksheet.column_dimensions[get_column_letter(idx)].width = exact_max + 1


def load_to_parquet(df: pd.DataFrame, parquet_path: str) -> None:
    """Saves the cleaned DataFrame to a Parquet file for analytics."""
    df.to_parquet(parquet_path, index=False)


def load_to_db(df: pd.DataFrame, db_name: str, table_name: str) -> None:
    """Loads the cleaned DataFrame into a SQLite database table."""
    with sqlite3.connect(db_name) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)