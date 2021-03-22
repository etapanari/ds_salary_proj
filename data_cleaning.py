import pandas as pd
df = pd.read_csv('glassdoor_jobs-239.csv')

# salary parsing
# state field
# age of company
# parsing job description

df = df[df['Salary_Estimate'] !='-1']

df.head()