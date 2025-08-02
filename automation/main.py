from api_client import ThurgauAPIClient, DataCleaner
from analyse import AnalyseC02Data
from bigquery_upload import BigQueryUploader
import os
from flask import Flask, request
import subprocess  # oder importiere direkt deine Analyse-Funktionen

app = Flask(__name__)

@app.route('/', methods=['POST'])
def trigger_job():
    print("🚀 Starte Pipeline... \n")

    # 1. API Daten laden und uuid / timestamp hinzufügen
    client = ThurgauAPIClient("https://data.tg.ch/api/records/1.0/search/")
    raw_df = client.fetch_data("div-energie-8")
    
    cleaner = DataCleaner()
    df_c02 = cleaner.add_uuid(raw_df)
    df_c02 = cleaner.add_timestamp(df_c02)

    # 2. Daten analysieren
    analyzer = AnalyseC02Data(df_c02)
    tables = analyzer.get_all_tables()

    # 3. Upload
    upload_dict={}
    for name, df in tables.items():
        upload_dict[name] = {
            "dataframe": df,
            "dataset": "energie_daten",
            "table": name
        }

    uploader = BigQueryUploader(project_id="c02-tg", credentials_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "secrets", "bigquery-service-account-c02-tg.json"))
    uploader.upload_to_bigquery(upload_dict)

    print("🏁 Pipeline abgeschlossen\n")
    
    return "Job gestartet", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
