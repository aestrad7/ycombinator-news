from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
import time

t= time.localtime()

#TODO: Cambiar la ruta de los archivos a relativas

# Read date_today from the temporary file
temp_file = Path(__file__).resolve().parent / 'date_today.txt'
with temp_file.open('r') as f:
    date_today = f.read().strip()

# Load the data
df = pd.read_csv(f"C:/Users/user/Documents/Code_New/Web-Scrapper/Scrapping-ycombinator/data/hacker_news_news_{date_today}.csv")

# Convert the time column to datetime format
df['time'] = pd.to_datetime(df['time'])

# Filter data to keep only the last 2 days
df = df[df['time'] >= df['time'].max() - pd.Timedelta(days=2)] #TODO: Evaluar distribucion de datos en time
print("Table data", "\n", df[['title', 'points', 'time']].head(), "\n", df.columns, "\n")

# Group data by time and sum the points
df_g = df[["points", "time"]].groupby('time').sum().reset_index()
print("Data grouped by time", "\n", df_g.head(), "\n")

# Create a list of strings with the top 5 news items based on points
top_5 = []
for index, row in df.nlargest(12, 'points').iterrows(): # 18 minutos por 12 news
    top_5.append(f"{row['title']} url: {row['link']}")

# print("Top 5 news", top_5, "\n")

# Instantiate the language model
llm = Ollama(model="llama3:8b")

# Define prompts for generating tweets
prompts = [
    """
    You are an expert in the music industry, startups, and machine learning, with aspirations of becoming a successful musician. You come across the following news article online. Using the context snippets provided (title), write a short, informative text that analyzes the impact, common opinions, and viewpoints on the news, focusing on key topics relevant to the analysis. Incorporate insights from your expertise to explore these topics.

    - Use keywords from the URL to complement your analysis.
    - Avoid directly citing the URL.
    - Ensure the text is cohesive and relevant to the context.
    - Maintain focus on the provided news and its broader implications.
    - Do not explicitly reference your background or expertise within the text.

    Title: {Title}
    URL: {URL}
    ANSWER:
    """
]
    # Write in spanish.

prompt = PromptTemplate.from_template(prompts[0])

def context_split(news_item):
    parts = news_item.split(" url: ")
    return {"Title": parts[0], "URL": parts[1]}

# Generate tweets for each prompt using the language model
responses = []
data = []  # List to store data for DataFrame

for news_item in top_5:
    try:
        context = context_split(news_item)
        print("Context:", "\n", context["Title"], "\n", context["URL"], "\n")
        response = llm.invoke(prompt.format(**context))
        responses.append(response)
        print("Generated tweets:", response, "\n")
        print("\n","time spent: ", (time.mktime(time.localtime()) - time.mktime(t)) / 60)
        
        # Append data to the list
        data.append({
            "context_title": context["Title"],
            "context_url": context["URL"],
            "response": response
        })
    except ValueError as e:
        print(f"Error processing news item: {e}")

# Convert the list to a DataFrame
df_responses = pd.DataFrame(data)

# Display the DataFrame
print(df_responses)

# Save the DataFrame to a CSV file
df_responses.to_csv("C:/Users/user/Documents/Code_New/Web-Scrapper/Scrapping-ycombinator/data/tweets.csv", index=False)
print("\n","time spent: ", (time.mktime(time.localtime()) - time.mktime(t)) / 60)

# # Optional: Visualize points vs time
# plt.figure(figsize=(10, 5))
# plt.scatter(df_g['time'], df_g['points'] / df_g['points'].sum())
# plt.title("Points vs Time")
# plt.xlabel("Time")
# plt.ylabel("Points")
# plt.xticks(rotation=90)  # Rotate x-axis labels vertically

# # Add grid
# plt.grid(True)

# # Add other visual elements
# plt.axhline(0, color='black', lw=0.5)
# plt.axvline(0, color='black', lw=0.5)
# plt.tight_layout()

# plt.show()