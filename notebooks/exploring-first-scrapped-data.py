import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

# Set the seaborn style
sns.set(style="whitegrid")

# Read the CSV file into a DataFrame
data = pd.read_csv('c:/Users/user/Documents/Code_New/Web-Scrapper/Scrapping-ycombinator/data/hacker_news_news_20240814.csv')

# elimina todos los registros que teinen menso de 100 points
data = data[data['points'] >= 250]
print("\n", "Cantidad de news: " ,data.shape)

# Create a histogram of the scores
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

sns.histplot(data=data, x='points', bins=10, ax=ax1) # , stat='probability'
ax1.set_xlabel('Score')
ax1.set_ylabel('Proportion')
ax1.set_title('Histogram of News Scores (Proportion)')

# Create a histogram of the scores, grouped by date
data['time'] = pd.to_datetime(data['time'])
data['date_only'] = data['time'].dt.date
grouped_data = data.groupby('date_only')['points'].count()

sns.barplot(x=grouped_data.index, y=grouped_data.values, ax=ax2)
ax2.set_xlabel('Date')
ax2.set_ylabel('Count')
ax2.set_title('Histogram of News Scores by Date')
ax2.set_xticklabels(grouped_data.index, rotation=45)

plt.tight_layout()
plt.show()