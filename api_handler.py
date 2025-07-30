import pandas as pd
import requests
from io import StringIO
import re


def fetch_data_from_api(api_url: str) -> pd.DataFrame:
    try:
        # Handle Google Drive shared links
        if "drive.google.com" in api_url:
            # Extract file ID from various URL formats
            file_id_match = re.search(r"/d/([a-zA-Z0-9_-]+)", api_url)
            if not file_id_match:
                raise ValueError("Invalid Google Drive URL format.")
            file_id = file_id_match.group(1)
            direct_url = f"https://drive.google.com/uc?id={file_id}&export=download"
            response = requests.get(direct_url)
            response.raise_for_status()
            return pd.read_csv(StringIO(response.text))
        #I want to convert my csv file to api

        # Standard API URL
        response = requests.get(api_url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            json_data = response.json()
            df = pd.json_normalize(json_data)
            return df
        elif 'text/csv' in content_type or 'application/octet-stream' in content_type:
            return pd.read_csv(StringIO(response.text))
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
    
            
    except Exception as e:
        raise RuntimeError(f"API fetch failed: {e}")
