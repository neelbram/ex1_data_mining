import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = r"C:\Users\97250\ex1_data_mining-1\ex1\output\problem1\problem1.json"
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)


def convert_to_numeric(record):
    for key, value in record.items():
        if isinstance(value, str) and value.isdigit():
            record[key] = int(value)
        elif isinstance(value, str) and value.replace('.', '', 1).isdigit() and value.count('.') < 2:
            record[key] = float(value)
    return record


records = data["records"]["record"]
converted_records = [convert_to_numeric(record) for record in records]
data["records"]["record"] = converted_records

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

df = pd.DataFrame(data['records']['record'])

df['DollarsPledged'] = pd.to_numeric(df['DollarsPledged'], errors='coerce')
df['DollarsGoal'] = pd.to_numeric(df['DollarsGoal'], errors='coerce')
df['NumBackers'] = pd.to_numeric(df['NumBackers'], errors='coerce')
df['DaysToGo'] = pd.to_numeric(df['DaysToGo'], errors='coerce')

numeric_columns = ['DollarsPledged', 'DollarsGoal', 'NumBackers', 'DaysToGo']
statistics = df[numeric_columns].describe()

print(statistics)

stats = {
    "min": statistics.loc['min'],
    "max": statistics.loc['max'],
    "mean": statistics.loc['mean'],
    "std": statistics.loc['std']
}

for stat, values in stats.items():
    print(f"{stat.capitalize()}:")
    for col, val in values.items():
        print(f"  {col}: {val}")

days_to_go_values = df['DaysToGo'].dropna().astype(int).tolist()

plt.figure(figsize=(10, 6))
plt.hist(days_to_go_values, bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of DaysToGo')
plt.xlabel('DaysToGo')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
sns.lmplot(data=df, x='DollarsGoal', y='DollarsPledged',
           scatter_kws={"s": 50}, line_kws={"color": "red"})
plt.title('DollarsPledged vs DollarsGoal', fontsize=15)
plt.xlabel('DollarsGoal', fontsize=12)
plt.ylabel('DollarsPledged', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('DollarsPledged_vs_DollarsGoal_lmplot.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.lmplot(data=df, x='NumBackers', y='DollarsPledged',
           scatter_kws={"s": 50}, line_kws={"color": "green"})
plt.title('DollarsPledged vs NumBackers', fontsize=15)
plt.xlabel('NumBackers', fontsize=12)
plt.ylabel('DollarsPledged', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('DollarsPledged_vs_NumBackers_lmplot.png')
plt.show()
