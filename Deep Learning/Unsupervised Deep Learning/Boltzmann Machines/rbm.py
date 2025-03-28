# Converted from: rbm.ipynb

#!/usr/bin/env python
# coding: utf-8

# # Boltzmann Machines

# ### Importing the libraries

# In[ ]:


import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data
from torch.autograd import Variable

# ## Part 1 - Data Preprocessing

# ### Importing the dataset

# In[ ]:


movies = pd.read_csv('ml-1m/movies.dat', sep = '::', header = None, engine = 'python', encoding = 'latin-1')
users = pd.read_csv('ml-1m/users.dat', sep = '::', header = None, engine = 'python', encoding = 'latin-1')
ratings = pd.read_csv('ml-1m/ratings.dat', sep = '::', header = None, engine = 'python', encoding = 'latin-1')

# ### Preparing the training set and the test set

# In[ ]:


training_set = pd.read_csv('ml-100k/u1.base', delimiter = '\t')
training_set = np.array(training_set, dtype = 'int')
test_set = pd.read_csv('ml-100k/u1.test', delimiter = '\t')
test_set = np.array(test_set, dtype = 'int')

# ### Getting the number of users and movies

# In[ ]:


nb_users = int(max(max(training_set[:,0]), max(test_set[:,0])))
nb_movies = int(max(max(training_set[:,1]), max(test_set[:,1])))

# ### Converting the data into an array with users in lines and movies in columns

# In[ ]:


def convert(data):
    new_data = []
    for id_users in range(1, nb_users + 1):
        id_movies = data[:,1][data[:,0] == id_users]
        id_ratings = data[:,2][data[:,0] == id_users]
        ratings = np.zeros(nb_movies)
        ratings[id_movies - 1] = id_ratings
        new_data.append(list(ratings))
    return new_data

training_set = convert(training_set)
test_set = convert(test_set)

# ### Converting the data into Torch tensors

# In[ ]:


training_set = torch.FloatTensor(training_set)
test_set = torch.FloatTensor(test_set)

# ### Converting the ratings into binary ratings 1 (Liked) or 0 (Not Liked)

# In[ ]:


training_set[training_set == 0] = -1
training_set[training_set == 1] = 0
training_set[training_set == 2] = 0
training_set[training_set >= 3] = 1

test_set[test_set == 0] = -1
test_set[test_set == 1] = 0
test_set[test_set == 2] = 0
test_set[test_set >= 3] = 1

# ## Part 2 -  Creating the architecture of the Neural Network

# ### Building the Restricted Boltzmann Machine (RBM)

# In[ ]:


class RBM():
    def __init__(self, nv, nh):
        self.W = torch.randn(nh, nv)
        self.a = torch.randn(1, nh)
        self.b = torch.randn(1, nv)

    def sample_h(self, x):
        wx = torch.mm(x, self.W.t())
        activation = wx + self.a.expand_as(wx)
        p_h_given_v = torch.sigmoid(activation)
        return p_h_given_v, torch.bernoulli(p_h_given_v)

    def sample_v(self, y):
        wy = torch.mm(y, self.W)
        activation = wy + self.b.expand_as(wy)
        p_v_given_h = torch.sigmoid(activation)
        return p_v_given_h, torch.bernoulli(p_v_given_h)

    def train(self, v0, vk, ph0, phk):
        self.W += (torch.mm(v0.t(), ph0) - torch.mm(vk.t(), phk)).t()
        self.b += torch.sum((v0 - vk), 0)
        self.a += torch.sum((ph0 - phk), 0)

# ### Setting parameters

# In[ ]:


nv = len(training_set[0])
nh = 100
batch_size = 100
rbm = RBM(nv, nh)

# ## Part 3 - Training The Restricted RBM 

# ### The Training Phase

# In[ ]:


nb_epoch = 10  # Number of epochs for training
for epoch in range(1, nb_epoch + 1):
    
    train_loss = 0  # Initialize training loss for the epoch
    s = 0.  # Counter for the number of batches

    for id_user in range(0, nb_users - batch_size, batch_size):

        vk = training_set[id_user:id_user+batch_size]  # Get a batch of training data
        v0 = training_set[id_user:id_user+batch_size]  # Initial visible nodes
        ph0, _ = rbm.sample_h(v0)  # Initial hidden nodes probabilities

        for k in range(10):  # Perform k steps of contrastive divergence

            _, hk = rbm.sample_h(vk)  # Sample hidden nodes given visible nodes
            _, vk = rbm.sample_v(hk)  # Sample visible nodes given hidden nodes
            vk[v0 < 0] = v0[v0 < 0]  # Maintain the original values for missing data

        phk, _ = rbm.sample_h(vk)  # Final hidden nodes probabilities
        rbm.train(v0, vk, ph0, phk)  # Train the RBM with the batch
        train_loss += torch.mean(torch.abs(v0[v0 >= 0] - vk[v0 >= 0]))  # Calculate the batch loss
        s += 1.  # Increment the batch counter
        
    print('epoch: ' + str(epoch) + ' loss: ' + str(train_loss / s))  # Print the average loss for the epoch

# ### Testing the RBM

# In[ ]:


test_loss = 0
s = 0.
for id_user in range(nb_users):
    v = training_set[id_user:id_user+1]
    vt = test_set[id_user:id_user+1]
    if len(vt[vt >= 0]) > 0:
        _, h = rbm.sample_h(v)
        _, v = rbm.sample_v(h)
        test_loss += torch.mean(torch.abs(vt[vt >= 0] - v[vt >= 0]))
        s += 1.
print('test loss: ' + str(test_loss / s))
