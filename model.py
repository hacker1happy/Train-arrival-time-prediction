# Importing the libraries
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

# loading data from train_data(csv file) with pandas 
dataset = pd.read_csv('train_data.csv')

# Dividing data into independent features (X) and dependent feature (y)
X = dataset.iloc[:, 2:6].values
y = dataset.iloc[:, -1].values


#Since we have a very small dataset, we will train our model with all availabe data.
# here number of decision trees considered are 100.
regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)

#Fitting model with trainig data
regressor.fit(X, y)

# Predicting a new result
x = [[0, 0, 1, 4]]
# print(regressor.predict(x))

# Saving model to disk
pickle.dump(regressor, open('model.pkl','wb'))

# # Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[1,1,1,4]]))