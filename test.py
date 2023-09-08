import pandas as pd

# Create an example DataFrame
data = {'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

# Add an empty column named 'NewColumn'
df['NewColumn'] = None  # You can also use np.nan or ''

# Display the updated DataFrame
print(df)
