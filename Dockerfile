# Basis-Image mit Python
FROM python:3.11-slim

# Arbeitsverzeichnis auf /code setzen
WORKDIR /code

# Kopiere alles (inkl. automation/, secrets/, etc.)
COPY . .

# Installiere Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Führe das Skript aus
CMD ["python", "automation/main.py"]
