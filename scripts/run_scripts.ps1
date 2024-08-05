# Cambia al directorio del proyecto
Set-Location -Path "C:\Users\user\Documents\Code_New\Web-Scrapper\Scrapping-ycombinator"

# Asegúrate de que el directorio 'data' exista
$dataDir = "C:\Users\user\Documents\Code_New\Web-Scrapper\Scrapping-ycombinator\data"
if (-Not (Test-Path -Path $dataDir)) {
	New-Item -ItemType Directory -Path $dataDir
}

# Ejecuta los scripts usando poetry
poetry run python .\src\hacker_news_scrapper.py
poetry run python .\src\hacker_news_table_extracter.py

# Se ejecuta con: .\run_scripts.ps1 (parado desde scripts)