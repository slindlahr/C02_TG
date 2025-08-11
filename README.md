# 🏗️ CO₂ Analyse & Upload – GCP Case Study

## 🔧 Architekturentscheidung und Begründung

### Verwendete Google Cloud Services

| Dienst              | Zweck                                 | Warum gewählt                                               |
|---------------------|----------------------------------------|-------------------------------------------------------------|
| **Cloud Run Service**        | Hoster für Python-API-Logik           | - Vollständig verwaltet<br>- Skaliert automatisch<br>- Einfach via HTTP triggerbar |
| **Cloud Scheduler**  | Automatisierung des Trigger-Vorgangs  | - Cron-ähnlich<br>- Zuverlässig<br>- Native Authentifizierung mit Cloud Run |
| **BigQuery**         | Datenziel / Cloud Data Warehouse      | - Hochperformantes SQL-Backend<br>- Kein Infrastruktur-Overhead<br>- Ideal für Analysezwecke |
| **Docker**           | Verpackung & Transport der App        | - Portabel<br>- Einheitlich über lokale und Cloud-Umgebung |

---

### ✅ Vorteile dieses Designs

- **Kosteneffizient**: Keine laufenden Ressourcen außerhalb der Ausführung.
- **Einfach skalierbar**: Cloud Run kümmert sich um Skalierung.
- **Trennung von Logik und Trigger**: Bessere Wartbarkeit.
- **Manuell und automatisch ausführbar**, ideal für hybride Nutzung.
- **Portabel** durch containerisierte App-Struktur (Docker).

---

### ⚠️ Nachteile & Alternativen

| Alternative                    | Nachteile im Vergleich                                   |
|-------------------------------|----------------------------------------------------------|
| **Cloud Functions**           | Eingeschränkteres Laufzeitverhalten, schwierigeres Debugging |
| **VM + Cronjob**              | Overhead für Wartung, geringere Skalierbarkeit           |
| **Composer (Airflow)**        | Overkill für einfachen täglichen Task, aufwendiger Setup |
| **Pub/Sub Trigger**           | Für einfache Zeitsteuerung unnötig komplex               |

---

### 🔁 Verbesserungsmöglichkeiten (Next Iteration)

- ✅ **Logging mit Google Cloud Logging** statt `print()`  
- ✅ **Secrets Manager verwenden** statt JSON-Datei im Image  
- ✅ **Monitoring mit Alerts**, z. B. bei Upload-Fehlschlägen  
- ✅ **Tests und Linting automatisieren**, z. B. mit GitHub Actions  
- ✅ **Parametrisierte Zeiträume über Cloud Run Argumente (Query-Params)**

---

## 📁 Projektstruktur

```bash
C02_TG/
│
├── automation/               # Haupt-Pipeline
│   ├── main.py               # Einstiegspunkt (von Cloud Run ausgeführt)
│   ├── api_client.py         # API-Fetch & Datenbereinigung
│   ├── analyse.py            # Tabellen-Erstellung aus Rohdaten
│   ├── bigquery_upload.py    # Upload-Logik für BQ
│   └── requirements.txt      # Python-Abhängigkeiten
│
├── secrets/                  # (lokal vorhanden) BigQuery JSON Credential
│
├── Dockerfile                # Container-Bauplan
└── README.md                 # Diese Datei
```

---

## ⚙️ Ausführung

### Manuelle Ausführung über Cloud Scheduler:
```
https://console.cloud.google.com/cloudscheduler?project=c02-tg&inv=1&invt=Ab5Hjg
```

### Automatische Ausführung:
Täglich über **Cloud Scheduler**, geplant um **08:00 Uhr (CET)**  
Zeitplan:  
```cron
0 8 * * *
```

---

## 📒 Hinweise zur lokalen Entwicklung

- Die App kann lokal über Docker ausgeführt werden:
```bash
docker build -t c02-analysis .
docker run -p 8080:8080 c02-analysis
```

- Es existiert ein separates **Jupyter Notebook**, mit dem dieselbe Logik lokal getestet und schrittweise ausgeführt werden kann. (z. B. für Debugging oder Exploration)

---

## 🧠 Überblick Klassen & Funktionen

| Klasse/Funktion          | Zweck |
|--------------------------|-------|
| `ThurgauAPIClient`       | Lädt Daten von der offiziellen API |
| `DataCleaner`            | Ergänzt UUID und Zeitstempel |
| `AnalyseC02Data`         | Erstellt strukturierte DataFrames für BigQuery |
| `BigQueryUploader`       | Lädt Tabellen in BigQuery hoch |
| `main.py` (Flask App)    | HTTP-Endpunkt, triggert gesamten Prozess |

---

## ⏱️ Zeiträume anpassen

- Aktuell lädt das Skript **alle verfügbaren Daten bei jedem Lauf**.
- In zukünftigen Iterationen kann der Zeitraum dynamisch gestaltet werden, z. B. über Query-Parameter an den Cloud Run Endpoint oder durch Vergleich mit bestehenden Daten in BigQuery.

---

**Autor:** Sebastian Lindlahr  
**Projekt:** CO₂ Analyse Thurgau – GCP Case Study  
