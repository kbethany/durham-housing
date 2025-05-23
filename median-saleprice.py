# explore_data.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("Metro_median_sale_price_uc_sfr_month.csv", encoding='latin1', low_memory=False)

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
                  var_name='Date', value_name='MedianSalePrice')

# Convert 'Date' from string to datetime (pandas handles m/d/yy)
df_long['Date'] = pd.to_datetime(df_long['Date'], format='ISO8601')

#Filter state or cities if needed
state = ['NC']
df_filtered = df_long[df_long['StateName'].isin(state)]
# Example: Median for all NC cities per month
nc_statewide = df_long.groupby('Date')['MedianSalePrice'].median().reset_index()

cities = ['Durham, NC', 'Raleigh, NC', 'Greensboro, NC', 'Charlotte, NC' ]
df_filtered = df_long[df_long['RegionName'].isin(cities)]
#cities_of_interest = ['Raleigh', 'Charlotte', 'Durham']
#df_filtered = df_long[df_long['RegionName'].isin(cities_of_interest)]

# Plotting
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_filtered, x='Date', y='MedianSalePrice', hue='RegionName')
plt.title('Median Sale Price Over Time')
plt.xlabel('Date')
plt.ylabel('Mean Sale Price')
plt.xticks(rotation=45)
plt.tight_layout()

# Save figure
plt.savefig("median-sales-price.png", dpi=300)

print("📊 Saved visualization as median-sales-price.png")