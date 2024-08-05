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

from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup

def get_files(data_directory, date_today):
    """Get a list of files in the data_directory that contain the date_today in their name."""
    return [file for file in Path(data_directory).iterdir() if date_today in file.name]

def save_to_csv(df, output_file):
    """Save the data to a CSV file."""
    print(df.head())
    df.to_csv(output_file, index=False)
    print("CSV file saved successfully.")

def df_transform(data, date_today): #:TODO validar que esto si funciona bien 
    """Order and transform time column"""
    df = pd.DataFrame(data)
    df['time'] = df['time'].apply(lambda x: x if len(x.split()) == 2 else '0 minutes')
    df[["num", "long"]] = df["time"].str.split(" ", expand=True)
    df["time"] = df.apply(lambda row: time_to_hour(row, date_today), axis=1)
    df = df.drop(columns=["num", "long"])
    df = df.astype({"points": int})
    df = df.sort_values(["points", "time"], ascending=[False, True])
    return df

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

def time_to_hour(row, date_today):
    if row["long"] == "minutes":
        return pd.Timestamp(date_today) - pd.Timedelta(minutes=int(row["num"]))
    elif row["long"] == "hours":
        return pd.Timestamp(date_today) - pd.Timedelta(hours=int(row["num"]))
    elif row["long"] == "days" or row["long"] == "day":
        return pd.Timestamp(date_today) - pd.Timedelta(days=int(row["num"]))
    elif row["long"] == "months":
        return pd.Timestamp(date_today) - pd.Timedelta(days=int(row["num"]*30))
    elif row["long"] == "years":
        return pd.Timestamp(date_today) - pd.Timedelta(days=int(row["num"]*365))
    else:
        return pd.Timestamp(date_today)
    
def main():
    # Directory for data files
    project_directory = Path(__file__).resolve().parent.parent
    data_directory = project_directory / 'data'

    # Ensure the 'data' directory exists
    if not data_directory.exists():
        print(f"The directory {data_directory} does not exist.")
        return

    # Read date_today from the temporary file
    temp_file = Path(__file__).resolve().parent / 'date_today.txt'
    with temp_file.open('r') as f:
        date_today = f.read().strip()

    # Use date_today in the script
    print(f"Date today is: {date_today}")

    files = get_files(data_directory, date_today)
    all_data = []
    for file in files:
        file_data = parse_html_file(file)
        all_data.extend(file_data)

    # Save the DataFrame to a CSV file
    output_file = data_directory / f'hacker_news_news_{date_today}.csv'
    final_df = df_transform(all_data, date_today)
    save_to_csv(final_df, output_file)

if __name__ == "__main__":
    main()
