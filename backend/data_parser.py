import pandas as pd
import pdfplumber
from io import BytesIO

def parse_file(file_bytes, filename):
    if filename.endswith(".csv"):
        return pd.read_csv(BytesIO(file_bytes))
    elif filename.endswith((".xls", ".xlsx")):
        return pd.read_excel(BytesIO(file_bytes))
    elif filename.endswith(".json"):
        return pd.read_json(BytesIO(file_bytes))
    elif filename.endswith(".pdf"):
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            tables = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    tables.append(pd.DataFrame(table[1:], columns=table[0]))
            if tables:
                return pd.concat(tables, ignore_index=True)
            else:
                raise ValueError("No table found in PDF.")
    else:
        raise ValueError("Unsupported file format")
