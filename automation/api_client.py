import pandas as pd
import requests
from datetime import datetime
import uuid

class ThurgauAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_data(self, endpoint: str, max_records: int=1000) -> pd.DataFrame:
        params = {"dataset": endpoint, "rows": max_records}
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        records = [r["fields"] for r in data.get("records", [])]
        df = pd.DataFrame(records)
        print(f"Es wurden {len(df)} Datensätze vom Dataset '{endpoint}' geladen.\n")
        return df
    
class DataCleaner:
    """Utility class for cleaning and enriching datasets with additional columns."""

    @staticmethod
    def add_uuid(df: pd.DataFrame, uuid_column: str = "uuid") -> pd.DataFrame:
        """Add a unique UUID to each row."""
        df[uuid_column] = [str(uuid.uuid4()) for _ in range(len(df))]
        return df

    @staticmethod
    def add_timestamp(df: pd.DataFrame, ts_column: str = "loaded_at") -> pd.DataFrame:
        """Add a timestamp to each row."""
        df[ts_column] = datetime.now().strftime("%Y-%m-%d")
        return df