import glassdoor_scraper as gs
import pandas as pd

path="C:/Users/etapa/PycharmProjects/ds_salary_proj/chromedriver"

df = gs.get_jobs('data_scientist', 15, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index = False)

print(df.head())

