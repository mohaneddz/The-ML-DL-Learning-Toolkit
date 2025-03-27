# Converted from: Apriori.ipynb

#!/usr/bin/env python
# coding: utf-8

# # Apriori

# ## Importing the libraries

# In[1]:


!pip install apyori

# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ## Data Preprocessing

# In[3]:


dataset = pd.read_csv('Market_Basket_Optimisation.csv', header = None)
transactions = []
for i in range(0, 7501):
  transactions.append([str(dataset.values[i,j]) for j in range(0, 20)])

# ## Training the Apriori model on the dataset

# In[4]:


from apyori import apriori
rules = apriori(transactions = transactions, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2, max_length = 2)

# ## Visualising the results

# ### Displaying the first results coming directly from the output of the apriori function

# In[5]:


results = list(rules)

# In[6]:


results

# ### Putting the results well organised into a Pandas DataFrame

# In[7]:


def inspect(results):
    lhs         = [tuple(result[2][0][0])[0] for result in results]
    rhs         = [tuple(result[2][0][1])[0] for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))
resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])

# ### Displaying the results non sorted

# In[8]:


resultsinDataFrame

# ### Displaying the results sorted by descending lifts

# In[9]:


resultsinDataFrame.nlargest(n = 10, columns = 'Lift')
