# Converted from: Random_Forest_Regression.ipynb

#!/usr/bin/env python
# coding: utf-8

# # Random Forest Regression

# ## Importing the libraries

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ## Importing the dataset

# In[2]:


dataset = pd.read_csv('Position_Salaries.csv')
X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, -1].values

# ## Training the Random Forest Regression model on the whole dataset

# In[3]:


from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X, y)

# ## Predicting a new result

# In[4]:


regressor.predict([[6.5]])

# ## Visualising the Random Forest Regression results (higher resolution)

# In[5]:


X_grid = np.arange(min(X), max(X), 0.01)
X_grid = X_grid.reshape((len(X_grid), 1))
plt.scatter(X, y, color = 'red')
plt.plot(X_grid, regressor.predict(X_grid), color = 'blue')
plt.title('Truth or Bluff (Random Forest Regression)')
plt.xlabel('Position level')
plt.ylabel('Salary')
plt.show()
