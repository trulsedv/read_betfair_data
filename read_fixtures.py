import pandas as pd

with open('output.txt', 'r') as file:
    lines = file.readlines()

data = []

for line in lines:
    dict_data = eval(line.strip())  # Parse the line as a dictionary
    if 'other' in dict_data:
        continue
    data.append(dict_data)

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'], format='%d.%b.%Y')

df.sort_values(by=['date'], inplace=True)  # 'home_team', 'away_team',
df.reset_index(drop=True, inplace=True)

pd.set_option('display.max_rows', None)  # Set to None to display all rows
print(df)
pd.reset_option('display.max_rows')
df.to_csv('output_rev.csv', index=False)


# df = pd.read_csv('output_rev.csv')
# last_date = ''
# reversed_df = df[::-1]
# for index, row in reversed_df.iterrows():
#     if row['date'] != last_date:
#         print(f"\n{row['date']}")
#         last_date = row['date']
#     print(row['home_team'], row['away_team'])
