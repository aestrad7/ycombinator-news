"""
This script scrapes data from HTML files and saves it in a CSV file.

Parameters:
- data_directory (str): The directory where the HTML files are located.
- date_today (str): The date used to filter the files.

Returns:
- None

Prints:
- The first few rows of the scraped data DataFrame.
- A success message after saving the DataFrame as a CSV file.
"""

import os
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup

import pandas as pd
from pathlib import Path

def get_files(data_directory, date_today):
    return [file for file in Path(data_directory).iterdir() if date_today in file.name]

def save_to_csv(data, output_file):
    """Save the data to a CSV file."""
    df = pd.DataFrame(data)
    print(df.head())
    df.to_csv(output_file, index=False)
    print("Archivo CSV guardado exitosamente.")

def main():
    # Directorio de consulta y guardado de datos
    project_directory = Path(__file__).resolve().parent.parent
    data_directory = project_directory / 'data'

    # Asegúrate de que el directorio 'data' exista
    if not data_directory.exists():
        print(f"El directorio {data_directory} no existe.")
        return

    # Leer date_today desde el archivo temporal
    temp_file = Path(__file__).resolve().parent / 'date_today.txt'
    with temp_file.open('r') as f:
        date_today = f.read().strip()

    # Usar date_today en el script
    print(f"Date today is: {date_today}")

    files = get_files(data_directory, date_today)
    for file in files:
        print(file)

if __name__ == "__main__":
    main()

def parse_html_file(file_path):
    """Parse the HTML file and extract news items."""
    data = []
    try:
        with file_path.open('r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        news_items = soup.find_all('tr', class_='athing')

        for item in news_items:
            titleline = item.find('span', class_='titleline')
            title_tag = titleline.find('a') if titleline else None
            title = title_tag.get_text() if title_tag else 'N/A'
            link = title_tag['href'] if title_tag else 'N/A'

            subtext = item.find_next_sibling('tr').find('td', class_='subtext')
            score_tag = subtext.find('span', class_='score')
            points = score_tag.get_text().split()[0] if score_tag else '0'

            time_tag = subtext.find('span', class_='age')
            time = time_tag.get_text() if time_tag else 'N/A'

            data.append({
                'title': title,
                'time': time,
                'link': link,
                'points': points
            })
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return data
import pandas as pd
from pathlib import Path

def get_files(data_directory, date_today):
    return [file for file in Path(data_directory).iterdir() if date_today in file.name]

def save_to_csv(data, output_file):
    """Save the data to a CSV file."""
    df = pd.DataFrame(data)
    print(df.head())
    df.to_csv(output_file, index=False)
    print("Archivo CSV guardado exitosamente.")

def main():
    # Directorio de consulta y guardado de datos
    project_directory = Path(__file__).resolve().parent.parent
    data_directory = project_directory / 'data'

    # Asegúrate de que el directorio 'data' exista
    if not data_directory.exists():
        print(f"El directorio {data_directory} no existe.")
        return

    # Leer date_today desde el archivo temporal
    temp_file = Path(__file__).resolve().parent / 'date_today.txt'
    with temp_file.open('r') as f:
        date_today = f.read().strip()

    # Usar date_today en el script
    print(f"Date today is: {date_today}")

    files = get_files(data_directory, date_today)
    for file in files:
        print(file)

if __name__ == "__main__":
    main()
import pandas as pd
from pathlib import Path

def get_files(data_directory, date_today):
    return [file for file in Path(data_directory).iterdir() if date_today in file.name]

def save_to_csv(data, output_file):
    """Save the data to a CSV file."""
    df = pd.DataFrame(data)
    print(df.head())
    df.to_csv(output_file, index=False)
    print("Archivo CSV guardado exitosamente.")

def main():
    # Directorio de consulta y guardado de datos
    project_directory = Path(__file__).resolve().parent.parent
    data_directory = project_directory / 'data'

    # Asegúrate de que el directorio 'data' exista
    if not data_directory.exists():
        print(f"El directorio {data_directory} no existe.")
        return

    # Leer date_today desde el archivo temporal
    temp_file = Path(__file__).resolve().parent / 'date_today.txt'
    with temp_file.open('r') as f:
        date_today = f.read().strip()

    # Usar date_today en el script
    print(f"Date today is: {date_today}")

    # Obtener la lista de archivos que contienen "20240804" en el nombre
    files = get_files(data_directory, date_today)

    all_data = []
    for file in files:
        file_data = parse_html_file(file)
        all_data.extend(file_data)

    # Guardar el DataFrame en un archivo CSV
    output_file = data_directory / f'hacker_news_news_{date_today}.csv'
    save_to_csv(all_data, output_file)

if __name__ == "__main__":
    main()
