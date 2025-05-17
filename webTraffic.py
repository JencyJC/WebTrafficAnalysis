import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import seaborn as sns

# Use seaborn style
sns.axes_style(style="whitegrid")

# Load environment variables from .env file
load_dotenv()


# MySQL connection details from .env
db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
    'autocommit': True
}


# Connect to MySQL
conn = mysql.connector.connect(**db_config)


# Read Excel files
df_webAnalysis = pd.read_excel("WebAnalysis.xlsx")


# Step 2: Insert data into existing MySQL tables
cursor = conn.cursor()

# Insert data into MySQL table
for _, row in df_webAnalysis.iterrows():
    cursor.execute("""
    INSERT INTO web_traffic (session_id, user_id, timestamp, page_url, source, medium, device, region, bounce, session_duration)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
       (row['session_id'],
        row['user_id'],
        row['timestamp'],
        row['page_url'],
        row['source'],
        row['medium'],
        row['device'],
        row['region'],
        row['bounce'],
        row['session_duration']
    ))

conn.commit()
print("Data successfully inserted!")

# to check 1st 5 data from sql
# query = "SELECT * FROM web_traffic"
# df = pd.read_sql(query, conn)
# print(df.head())


# Assuming 'timestamp' column exists and needs to be converted to datetime

df_webAnalysis['timestamp'] = pd.to_datetime(df_webAnalysis['timestamp'])  # if not already datetime
df_webAnalysis['date'] = df_webAnalysis['timestamp'].dt.date


# 1. Daily Unique Sessions

daily_visits = df_webAnalysis.groupby('date')['session_id'].nunique()

plt.figure(figsize=(12, 5))
plt.plot(daily_visits.index, daily_visits.values, marker='o', linestyle='-')
plt.title("Daily Unique Sessions", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Number of Unique Sessions", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



# 2. Web Traffic Trend with Moving Avg
# Anomaly Detection using 7-day Rolling Average 

rolling_mean = daily_visits.rolling(window=7).mean()

plt.figure(figsize=(12, 5))
plt.plot(daily_visits.index, daily_visits.values, label='Actual Sessions', color='blue')
plt.plot(rolling_mean.index, rolling_mean.values, label='7-Day Moving Average', color='orange', linestyle='--')
plt.title("Web Traffic Trend with 7-Day Moving Average", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Number of Sessions", fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 3. Daily Bounce Rate (%) over time
bounce_rate = df_webAnalysis.groupby('date')['bounce'].mean() * 100

plt.figure(figsize=(12, 5))
plt.plot(bounce_rate.index, bounce_rate.values, color='purple', marker='o')
plt.title("Daily Bounce Rate (%)", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Bounce Rate (%)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 4. Bounce Rate by Device Type – Bar Chart
# Group and calculate bounce rate
bounce_by_device = df_webAnalysis.groupby('device').agg(
    total_sessions=('session_id', 'count'),
    bounces=('bounce', 'sum')
)
bounce_by_device['bounce_rate (%)'] = (bounce_by_device['bounces'] / bounce_by_device['total_sessions']) * 100

# Plot
plt.figure(figsize=(8, 5))
plt.bar(bounce_by_device.index, bounce_by_device['bounce_rate (%)'], color='tomato')
plt.title('Bounce Rate by Device Type')
plt.xlabel('Device Type')
plt.ylabel('Bounce Rate (%)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()



#5. Average Session Duration by Region – Horizontal Bar Chart
# Group and calculate average session duration

avg_duration_region = df_webAnalysis.groupby('region')['session_duration'].mean().sort_values()

# Plot
plt.figure(figsize=(9, 5))
plt.barh(avg_duration_region.index, avg_duration_region.values, color='skyblue')
plt.title('Average Session Duration by Region')
plt.xlabel('Average Duration (seconds)')
plt.ylabel('Region')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


cursor.close()
conn.close()


