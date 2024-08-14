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
poetry run python .\src\ollama-test-01.py
# Se ejecuta con: .\run_scripts.ps1 (parado desde scripts)


############################################################################################################


# # Cambia al directorio del proyecto
# Set-Location -Path "C:\Users\user\Documents\Code_New\Web-Scrapper\Scrapping-ycombinator"

# # Asegúrate de que el directorio 'data' exista
# $dataDir = "C:\Users\user\Documents\Code_New\Web-Scrapper\Scrapping-ycombinator\data"
# if (-Not (Test-Path -Path $dataDir)) {
# 	New-Item -ItemType Directory -Path $dataDir
# }

# # Calcula el tiempo de ejecución
# $executionTime = Measure-Command {
# 	# Ejecuta los scripts usando poetry
# 	poetry run python .\src\hacker_news_scrapper.py
# 	poetry run python .\src\hacker_news_table_extracter.py
# 	poetry run python .\src\ollama-test-01.py
# }

# # Convierte el tiempo de ejecución a minutos
# $executionTimeMinutes = $executionTime.TotalMinutes

# # Imprime el tiempo de ejecución en la consola
# Write-Host "Tiempo: $executionTimeMinutes minutos"