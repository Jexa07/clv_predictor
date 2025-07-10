import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# Load data
file = r"C:\Users\hp\OneDrive\Desktop\online_retail_II.xlsx"
df1 = pd.read_excel(file, sheet_name='Year 2009-2010')
df2 = pd.read_excel(file, sheet_name='Year 2010-2011')
df = pd.concat([df1, df2])

# Clean
df.dropna(subset=['Customer ID', 'InvoiceDate'], inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Customer ID'] = df['Customer ID'].astype(str)
df['TotalPrice'] = df['Quantity'] * df['Price']

# RFM features
ref_date = df['InvoiceDate'].max()
rfm = df.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (ref_date - x.max()).days,
    'Invoice': 'nunique',
    'TotalPrice': 'sum',
    'Country': 'first'
}).reset_index()
rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'Country']

# Encode country
country_map = {country: i for i, country in enumerate(rfm['Country'].unique())}
rfm['CountryCode'] = rfm['Country'].map(country_map)
pickle.dump(country_map, open('models/country_map.pkl', 'wb'))

# Train model
X = rfm[['Recency', 'Frequency', 'CountryCode']]
y = rfm['Monetary']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open('models/rfm_model.pkl', 'wb'))

# Export top customers
rfm['PredictedCLV'] = model.predict(X)
top = rfm[['CustomerID', 'Country', 'PredictedCLV']].sort_values(by='PredictedCLV', ascending=False)
top.to_csv('data/top_customers.csv', index=False)