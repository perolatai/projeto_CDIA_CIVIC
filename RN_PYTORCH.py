#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch 
import pandas as pd 
import torch.nn as nn 
from torch.utils.data import random_split, DataLoader, TensorDataset 
import torch.nn.functional as F 
import numpy as np 
import torch.optim as optim 
from torch.optim import Adam
from sklearn.metrics import log_loss


# In[2]:


civic = pd.read_csv(r'civic') 

print(civic.head()) 


# In[3]:


civic.info()


# In[4]:


civic = civic[['gene', 'entrez_id', 'variant', 'disease', 'doid', 'phenotypes', 'drugs', 'drug_interaction_type', 'evidence_type', 'evidence_direction', 'evidence_level', 'clinical_significance', 'evidence_statement', 'citation_id', 'source_type', 'citation', 'rating', 'evidence_status', 'evidence_id', 'variant_id', 'gene_id', 'chromosome', 'start', 'stop', 'reference_bases', 'variant_bases', 'representative_transcript', 'ensembl_version', 'reference_build', 'variant_summary', 'variant_origin', 'is_flagged', 'variant_types', 'hgvs_expressions', 'civic_variant_evidence_score', 'allele_registry_id', 'clinvar_ids', 'variant_aliases', 'description']].apply(lambda x: pd.factorize(x)[0])
civic


# In[5]:


label = {'gene': 0, 'disease': 1, 'clinical_significance': 2, }

input = civic.iloc[:, 1:-2]         
print('Input values are: ') 
print(input.head())   
output = civic.iloc[:, 1:-2]         
print('Output values are: ') 
print(output.head())   


# In[6]:


input = torch.Tensor(input.to_numpy())      
print('\nInput format: ', input.shape, input.dtype)      
output = torch.tensor(output.to_numpy())         
print('Output format: ', output.shape, output.dtype)   
data = TensorDataset(input, output) 


# In[7]:


train_batch_size = 10        
number_rows = len(input)    
test_split = int(number_rows*0.3)  
validate_split = int(number_rows*0.2) 
train_split = number_rows - test_split - validate_split     
train_set, validate_set, test_set = random_split( 
    data, [train_split, validate_split, test_split])


# In[8]:


train_loader = DataLoader(train_set, batch_size = train_batch_size, shuffle = True) 
validate_loader = DataLoader(validate_set, batch_size = 1) 
test_loader = DataLoader(test_set, batch_size = 1)


# In[9]:


input_size = list(input.shape)[1]    
learning_rate = 0.01 
output_size = len(label)


# In[10]:


class Network(nn.Module): 
   def __init__(self, input_size, output_size): 
       super(Network, self).__init__() 
        
       self.layer1 = nn.Linear(input_size, 24) 
       self.layer2 = nn.Linear(24, 24) 
       self.layer3 = nn.Linear(24, output_size) 


   def forward(self, x): 
       x1 = F.relu(self.layer1(x)) 
       x2 = F.relu(self.layer2(x1)) 
       x3 = self.layer3(x2) 
       return x3 


# In[11]:


model = Network(input_size, output_size)


# In[12]:


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
print("The model will be running on", device, "device\n") 
model.to(device)


# In[13]:


def saveModel(): 
    path = "./NetModel.pth" 
    torch.save(model.state_dict(), path)


# In[14]:


loss_fn = nn.CrossEntropyLoss()
optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)


# In[15]:


def train(num_epochs): 
    best_accuracy = 0 
     
    print("Begin training...") 
    for epoch in range(1, num_epochs+1): 
        running_train_loss = 0 
        running_accuracy = 0 
        running_vall_loss = 0 
        total = 0 


# In[16]:


for data in train_loader:
    inputs, outputs = data   
    optimizer.zero_grad()            
    predicted_outputs = model(inputs)   
    train_loss = loss_fn(predicted_outputs)
    target = Variable(target.cuda()
    loss = log_loss.backward()
    optimizer.step()
    running_train_loss +=train_loss.item()
    
    


# In[ ]:




