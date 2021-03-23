import pandas as pd
df = pd.read_csv('glassdoor_jobs-239.csv')

# salary parsing
# salary string: "Employer Provided Salary:$80K - $186K" or "$120K - $180K (Employer est.)"
df = df[df['Salary_Estimate'] !='-1']
df['Hourly'] = df['Salary_Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

salary = df['Salary_Estimate'].apply(lambda x: x.split('(')[0])

clean_salary = salary.apply(lambda x: x.lower().replace('employer provided salary:','').replace('k','').replace('$','').replace('per hour',''))
df['Salary_Estimate'] = clean_salary

df['min_salary'] = df['Salary_Estimate'].apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = df['Salary_Estimate'].apply(lambda x: int(x.split('-')[1]) if len(x.split('-')) > 1 else 0)
df['average_salary'] = (df['min_salary']+df['max_salary'])/2

#print(df['Salary_Estimate'])

# state field# some values are like "Cranberry Twp, PA"
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1] if len(x.split(',')) > 1 else -1)

#print(df['job_state'])

# age of company
df['age_of_company']= df['Founded'].apply(lambda x: x if x < 1 else 2020 -x)

#print(df['age_of_company'])

# parsing job description
# it's a long string like: "We are looking for a Data Scientist to analyze large amounts of  ..."
# let's see if the string "python" is in the job description
df['python_jd'] = df['Job_Description'].apply(lambda x: 1 if "python" in x.lower() else 0)

#print(df['python_jd'].value_counts())

# let's see if the string "spark" is in the job description
df['spark_jd'] = df['Job_Description'].apply(lambda x: 1 if "spark" in x.lower() else 0)
#print(df['spark_jd'].value_counts())

# let's see if the string "excel" is in the job description
df['excel'] = df['Job_Description'].apply(lambda x: 1 if "excel" in x.lower() else 0)
#print(df['excel'].value_counts())

# let's see if the string "excel" is in the job description
df['aws'] = df['Job_Description'].apply(lambda x: 1 if "aws" in x.lower() else 0)
#print(df['aws'].value_counts())

df.to_csv('salary_data_cleaned.csv' , index=False)