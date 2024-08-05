import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("../data/hacker_news_news_20240805.csv")

# Remove "ago" from the time column
df["time"] = df["time"].str.replace(" ago", "")

# Convert the time column to datetime
df_grouped = df[["time", "points"]].groupby(df["time"]).count().sort_values(by="points", ascending=False)
print("Tabla de frecuencia","\n",df_grouped.head())

# split the column time
df[["num", "long"]] = df["time"].str.split(" ", expand=True)
print("\n", "split time", "\n", df[["num", "long"]].head())

print("\n", "Unique longs: ", df["long"].unique())

# Create a function to convert the convination between num and long and the current time in datetime
def time_to_hour(row):
    if row["long"] == "minutes":
        return pd.Timestamp.now() - pd.Timedelta(minutes=int(row["num"]))
    elif row["long"] == "hours":
        return pd.Timestamp.now() - pd.Timedelta(hours=int(row["num"]))
    elif row["long"] == "days" or row["long"] == "day":
        return pd.Timestamp.now() - pd.Timedelta(days=int(row["num"]))
    elif row["long"] == "months":
        return pd.Timestamp.now() - pd.Timedelta(days=int(row["num"]*30))
    elif row["long"] == "years":
        return pd.Timestamp.now() - pd.Timedelta(days=int(row["num"]*365))
    else:
        return pd.Timestamp.now()

# Apply the function to the dataframe
df["time_hour"] = df.apply(time_to_hour, axis=1)
print("\n", "time_hour", "\n", df["time_hour"].head())


### 


# Plot the number of points by time
plt.scatter(df_grouped.index, df_grouped["points"]/df_grouped["points"].sum())
plt.xlabel("Time")
plt.ylabel("Points")
plt.title("Number of Points by Time")
plt.xticks(rotation=90)  # Rotate x-axis labels vertically

# Add grid
plt.grid(True)

# Add other visual elements
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.tight_layout()

plt.show()