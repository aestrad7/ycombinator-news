from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import pandas as pd
import matplotlib.pyplot as plt
from langchain_core.output_parsers import StrOutputParser

# Load the data
df = pd.read_csv("../data/hacker_news_news_20240806.csv")

# Convert the time column to datetime format
df['time'] = pd.to_datetime(df['time'])

# Filter data to keep only the last 2 days
df = df[df['time'] >= df['time'].max() - pd.Timedelta(days=2)]
print("Table data", "\n", df[['title', 'points', 'time']].head(), "\n", df.columns, "\n")

# Group data by time and sum the points
df_g = df[["points", "time"]].groupby('time').sum().reset_index()
print("Data grouped by time", "\n", df_g.head(), "\n")

# Create a list of strings with the top 5 news items based on points
top_5 = []
for index, row in df.nlargest(5, 'points').iterrows():
    top_5.append(f"{row['title']} url: {row['link']}")

# print("Top 5 news", top_5, "\n")

# Instantiate the language model
llm = Ollama(model="llama3:8b")

# Define prompts for generating tweets
prompts = [
    """
    You are an expert in music, startups and machine learning.
    Use the following context snippets to write a short piece of informative text that analyzes the impact, common opinions, and viewpoints on the news, based on the title and URL provided.    Focus on your experience and knowledge to talk about the key topics in the tweet.
    Use the URL keywords to complement the topic knowledge.
    Do not cite the URL.
    It doesn't matter if you don't understand the context, just write what you think is relevant.
    It doesn't matter if it doesn't have to do with music, startups or machine learning directly.
    Don't say 'As an expert in music startup' or anything related to that, you don't need to introduce yourself or your credentials.

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

import pandas as pd

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
df_responses.to_csv("../data/tweets.csv", index=False)


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