import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('salary_data_cleaned.csv')

print(df.columns)
# choose relevant columns
df['desc_len'] = df['Job_Description'].apply(lambda x: len(x))

df_model = df[['average_salary','Rating','Size','Type_Of_Ownership','Industry','Sector','Revenue','Hourly',
             'job_state','age_of_company','python_jd','excel','desc_len']]

df_dum = pd.get_dummies(df_model)

# train test split
from sklearn.model_selection import train_test_split

X = df_dum.drop('average_salary', axis =1)
y = df_dum.average_salary.values # we make an array with the average salary values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# multiple linear regression
import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y, X_sm)
print(model.fit().summary())

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

print(np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

#lasso regression
lm_l = Lasso(alpha=.13)
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))

alpha = []
error = []

for i in range(1, 100):
    alpha.append(i / 100)
    lml = Lasso(alpha=(i / 100))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

print(plt.plot(alpha, error))

err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns=['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]

# random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

print(np.mean(cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error', cv= 3)))

# tune models GridsearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

print("best score tuned")
print(gs.best_score_)
print(gs.best_estimator_)

# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
print(mean_absolute_error(y_test,tpred_lm))
print(mean_absolute_error(y_test,tpred_lml))
print(mean_absolute_error(y_test,tpred_rf))

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)

import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0]

print(list(X_test.iloc[1,:]))
