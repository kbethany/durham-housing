# explore_data.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("Metro_new_con_mean_sale_price_uc_sfr_month.csv", encoding='latin1', low_memory=False)

# Shape of the data (rows, columns)
print("Shape of the dataset:", df.shape)

# Column names
print("\nColumn names:")
print(df.columns.tolist())

# First few rows
print("\nSample rows:")
print(df.head())

# Summary of each column
print("\nInfo:")
print(df.info())

# Count of missing values
print("\nMissing values (top 15):")
print(df.isnull().sum().sort_values(ascending=False).head(15))


# Columns to keep fixed
id_vars = ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']

# Columns to melt (all date columns)
value_vars = df.columns.difference(id_vars)

# Melt to long format
df_long = df.melt(id_vars=id_vars, value_vars=value_vars,
                  var_name='Date', value_name='MeanSalePrice')

# Convert 'Date' from string to datetime (pandas handles m/d/yy)
df_long['Date'] = pd.to_datetime(df_long['Date'], format='ISO8601')

#Filter state or cities if needed
state = ['NC']
df_filtered = df_long[df_long['StateName'].isin(state)]

#Calculate statewide mean
state_avg = df_filtered.groupby('Date')['MeanSalePrice'].mean().reset_index()
state_avg['RegionName'] = 'NC Average'  # So we can plot it like a city
state_avg['StateName'] = 'NC'
state_avg['RegionID'] = None
state_avg['SizeRank'] = None
state_avg['RegionType'] = 'Statewide'

state_avg = state_avg[df_filtered.columns]

# Append NC average to df_filtered
df_filtered = pd.concat([df_filtered, state_avg], ignore_index=True)

# Filter for selected cities + state average
cities = ['Durham, NC', 'Raleigh, NC', 'NC Average']
df_filtered = df_filtered[df_filtered['RegionName'].isin(cities)]

# Plotting
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_filtered, x='Date', y='MeanSalePrice', hue='RegionName')
plt.title('Mean New Construction Sale Price')
plt.xlabel('Year')
plt.ylabel('Mean Sale Price')
plt.xticks(rotation=45)
from matplotlib.ticker import FuncFormatter

# Format y-axis as currency
formatter = FuncFormatter(lambda x, _: f'${x:,.0f}')
plt.gca().yaxis.set_major_formatter(formatter)

import matplotlib.dates as mdates

# Set x-axis major ticks to quarterly
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.tight_layout()


import plotly.express as px

# Plotly expects tidy (long) format, which you already have in df_filtered
fig = px.line(
    df_filtered,
    x='Date',
    y='MeanSalePrice',
    color='RegionName',
    title='Mean New Construction Sale Price',
    labels={'MeanSalePrice': 'Mean Sale Price', 'Date': 'Date'},
)

# Format y-axis as currency
fig.update_yaxes(tickprefix="$", separatethousands=True)

# Optional: customize layout further
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Mean Sale Price',
    legend_title='Region',
    hovermode='x unified',
    template='plotly_white',
    height=500,
)

fig.show()



# Save figure
plt.savefig("new-construction-mean-saleprice.png", dpi=300)

print("📊 Saved visualization as new-construction-mean-saleprice.png")