def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

# Data
df = pd.DataFrame({
    'Age': [25, 45, 35, 50, 23],
    'Income': [50000, 120000, 80000, 110000, 75000]
})

# Standardization
df_standardized = df.copy()
df_standardized[['Age', 'Income']] = StandardScaler().fit_transform(df[['Age', 'Income']])

# Normalization
df_normalized = df.copy()
df_normalized[['Age', 'Income']] = MinMaxScaler().fit_transform(df[['Age', 'Income']])

print("Standardized:\\n", df_standardized, "\\n")
print("Normalized:\\n", df_normalized)
    '''
    print(code)