from google.oauth2 import service_account
from pandas_gbq import to_gbq
import os

class BigQueryUploader:
    def __init__(self, project_id: str, credentials_path: str):
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)

    def upload_to_bigquery(self, tables: dict, if_exists: str = "replace"):
        """
        tables: dict im Format {
            "name1": {
                "dataframe": df,
                "dataset": "mein_dataset",
                "table": "meine_tabelle"
            },
            ...
        }
        """
        for name, config in tables.items():
            df = config["dataframe"]
            dataset = config["dataset"]
            table = config["table"]
            full_table_name = f"{dataset}.{table}"

            print(f"⬆️ Lade {name} hoch nach: {full_table_name}...")

            try:
                to_gbq(
                    dataframe=df,
                    destination_table=full_table_name,
                    project_id=self.project_id,
                    credentials=self.credentials,
                    if_exists=if_exists
                )
                print(f"✅ {name} erfolgreich hochgeladen.\n")
            except Exception as e:
                print(f"❌ Fehler beim Hochladen von {name}: {e}\n")