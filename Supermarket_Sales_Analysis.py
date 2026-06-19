import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Set visualization style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 1. GENERATE DATA
np.random.seed(42)
n_rows = 500

data = {
    'Invoice_ID': [f"INV-{i:04d}" for i in range(1, n_rows + 1)],
    'Branch': np.random.choice(['A', 'B', 'C'], n_rows),
    'Customer_Type': np.random.choice(['Member', 'Normal'], n_rows),
    'Gender': np.random.choice(['Male', 'Female'], n_rows),
    'Product_Line': np.random.choice(['Electronic accessories', 'Fashion accessories', 
                                      'Food and beverages', 'Health and beauty', 
                                      'Home and lifestyle', 'Sports and travel'], n_rows),
    'Unit_Price': np.round(np.random.uniform(10, 100, n_rows), 2),
    'Quantity': np.random.randint(1, 10, n_rows),
    'Payment': np.random.choice(['Cash', 'Credit card', 'E-wallet'], n_rows),
    'Rating': np.round(np.random.uniform(4, 10, n_rows), 1),
    'Date': [datetime.date(2026, 1, 1) + datetime.timedelta(days=int(np.random.randint(0, 90))) for _ in range(n_rows)],
    'Time': [f"{np.random.randint(10, 21)}:{np.random.randint(0, 60):02d}" for _ in range(n_rows)]
}
df = pd.DataFrame(data)

# 2. DATA CLEANING & FEATURE ENGINEERING
df['Tax'] = np.round(df['Unit_Price'] * df['Quantity'] * 0.05, 2)
df['Total'] = np.round((df['Unit_Price'] * df['Quantity']) + df['Tax'], 2)
df['Date'] = pd.to_datetime(df['Date'])
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour

# 3. VISUALIZATIONS
# Plot 1: Revenue by Product Line (Fixed palette warning)
plt.figure()
product_sales = df.groupby('Product_Line')['Total'].sum().sort_values(ascending=False).reset_index()
sns.barplot(x='Total', y='Product_Line', data=product_sales, hue='Product_Line', palette='viridis', legend=False)
plt.title('Total Revenue by Product Line')
plt.xlabel('Total Sales ($)')
plt.ylabel('Product Category')
plt.tight_layout()
plt.savefig('revenue_by_product.png') 
plt.show()

# Plot 2: Payment Preferences
plt.figure()
sns.countplot(x='Payment', hue='Customer_Type', data=df, palette='pastel')
plt.title('Payment Method Preference by Customer Type')
plt.xlabel('Payment Method')
plt.ylabel('Transaction Count')
plt.tight_layout()
plt.savefig('payment_preferences.png')
plt.show()

# 4. PRINT METRICS REPORT
print("\n--- Business Insights Summary ---")
print(f"Total Revenue Generated: ${df['Total'].sum():,.2f}")
print(f"Average Order Value (AOV): ${df['Total'].mean():,.2f}")
print(f"Average Customer Rating: {df['Rating'].mean():.2f}/10\n")