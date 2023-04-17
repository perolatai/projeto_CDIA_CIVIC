import torch 
import pandas as pd 
import torch.nn as nn 
from torch.utils.data import random_split, DataLoader, TensorDataset 
import torch.nn.functional as F 
import numpy as np 
import torch.optim as optim 
from torch.optim import Adam 

#lendo arquivo
df = pd.read_csv('Civic.csv') 
#print(df['evidence_type'].value_counts()) 

y = df[['evidence_type']]

X = df.drop(['entrez_id', 'evidence_type', 'gene_id', 'evidence_level', 'citation_id', 'source_type', 'citation', 'evidence_id', 'representative_transcript',
                    'ensembl_version', 'allele_registry_id'], axis=1).apply(lambda x: pd.factorize(x)[0])


#converte para numero as features:
labels = {'Predictive':0, 'Predisposing':1, 'Prognostic':2, 'Diagnostic':3, 'Oncogenic':4, 'Functional':5} 

y['evidence_type_num'] = y['evidence_type']   # Create a new column "evidence_type_num" 
y.evidence_type_num = [labels[item] for item in y.evidence_type_num]  # Convert the values to numeric ones 

# Define input and output datasets 
#input = df.iloc[:, 1:-2]            # We drop the first column and the two last ones. 
#print('\nInput values are:') 
#print(input.head())   
output = y.loc[:, 'evidence_type_num']   # Output Y is the last column  
#print('\nThe output value is:') 
#print(output.head()) 


# Convert Input and Output data to Tensors and create a TensorDataset 
input = torch.Tensor(X.to_numpy())      # Create tensor of type torch.float32 
print('\nInput format: ', input.shape, input.dtype)     # Input format: torch.Size([150, 4]) torch.float32 
output = torch.tensor(output.to_numpy())        # Create tensor type torch.int64  
print('Output format: ', output.shape, output.dtype)  # Output format: torch.Size([150]) torch.int64 
data = TensorDataset(input, output) 

# Split to Train, Validate and Test sets using random_split 
train_batch_size = 10
number_rows = len(input)    # The size of our dataset or the number of rows in excel table.  
test_split = int(number_rows*0.3)  
validate_split = int(number_rows*0.2) 
train_split = number_rows - test_split - validate_split     
train_set, validate_set, test_set = random_split( 
    data, [train_split, validate_split, test_split])    
 
# Create Dataloader to read the data within batch sizes and put into memory. 
train_loader = DataLoader(train_set, batch_size = train_batch_size, shuffle = True) 
validate_loader = DataLoader(validate_set, batch_size = 1) 
test_loader = DataLoader(test_set, batch_size = 1)

# Define model parameters 
input_size = list(input.shape)[1]   # = 4. The input depends on how many features we initially feed the model. In our case, there are 4 features for every predict value  
learning_rate = 0.01 
output_size = len(labels)           # The output is prediction results for three types of Irises.  

########

# Define neural network 
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
 
# Instantiate the model 
model = Network(input_size, output_size) 

# Define your execution device 
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
print("The model will be running on", device, "device\n") 
model.to(device)    # Convert model parameters and buffers to CPU or Cuda 

########

# Function to save the model 
def saveModel(): 
    path = "./Resultado-do-Civic-Modelo.pth" 
    torch.save(model.state_dict(), path) 

# Define the loss function with Classification Cross-Entropy loss and an optimizer with Adam optimizer
loss_fn = nn.CrossEntropyLoss()
optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

########

# Training Function 
def train(num_epochs): 
    best_accuracy = 0.0 
     
    print("Begin training...") 
    for epoch in range(1, num_epochs+1): 
        running_train_loss = 0.0 
        running_accuracy = 0.0 
        running_vall_loss = 0.0 
        total = 0 
 
        # Training Loop 
        for data in train_loader: 
        #for data in enumerate(train_loader, 0): 
            inputs, outputs = data  # get the input and real species as outputs; data is a list of [inputs, outputs] 
            optimizer.zero_grad()   # zero the parameter gradients          
            predicted_outputs = model(inputs)   # predict output from the model 
            train_loss = loss_fn(predicted_outputs, outputs)   # calculate loss for the predicted output  
            train_loss.backward()   # backpropagate the loss 
            optimizer.step()        # adjust parameters based on the calculated gradients 
            running_train_loss +=train_loss.item()  # track the loss value 
 
        # Calculate training loss value 
        train_loss_value = running_train_loss/len(train_loader) 
 
        # Validation Loop 
        with torch.no_grad(): 
            model.eval() 
            for data in validate_loader: 
               inputs, outputs = data 
               predicted_outputs = model(inputs) 
               val_loss = loss_fn(predicted_outputs, outputs) 
             
               # The label with the highest value will be our prediction 
               _, predicted = torch.max(predicted_outputs, 1) 
               running_vall_loss += val_loss.item()  
               total += outputs.size(0) 
               running_accuracy += (predicted == outputs).sum().item() 
 
        # Calculate validation loss value 
        val_loss_value = running_vall_loss/len(validate_loader) 
                
        # Calculate accuracy as the number of correct predictions in the validation batch divided by the total number of predictions done.  
        accuracy = (100 * running_accuracy / total)     
 
        # Save the model if the accuracy is the best 
        if accuracy > best_accuracy: 
            saveModel() 
            best_accuracy = accuracy 
         
        # Print the statistics of the epoch 
        print('Completed training batch', epoch, 'Training Loss is: %.4f' %train_loss_value, 'Validation Loss is: %.4f' %val_loss_value, 'Accuracy is %d %%' % (accuracy))
########
# Function to test the model 
def test(): 
    # Load the model that we saved at the end of the training loop 
    model = Network(input_size, output_size) 
    path = "Resultado-do-Civic-Modelo.pth" 
    model.load_state_dict(torch.load(path)) 
     
    running_accuracy = 0 
    total = 0 
 
    with torch.no_grad(): 
        for data in test_loader: 
            inputs, outputs = data 
            outputs = outputs.to(torch.float32) 
            predicted_outputs = model(inputs) 
            _, predicted = torch.max(predicted_outputs, 1) 
            total += outputs.size(0) 
            running_accuracy += (predicted == outputs).sum().item() 
 
        print('Accuracy of the model based on the test set of', test_split ,'inputs is: %d %%' % (100 * running_accuracy / total))    
 
 
# Optional: Function to test which species were easier to predict  
def test_species(): 
    # Load the model that we saved at the end of the training loop 
    model = Network(input_size, output_size) 
    path = "Resultado-do-Civic-Modelo.pth" 
    model.load_state_dict(torch.load(path)) 
     
    labels_length = len(labels) # how many labels of Irises we have. = 3 in our database. 
    labels_correct = list(0. for i in range(labels_length)) # list to calculate correct labels [how many correct setosa, how many correct versicolor, how many correct virginica] 
    labels_total = list(0. for i in range(labels_length))   # list to keep the total # of labels per type [total setosa, total versicolor, total virginica] 
  
    with torch.no_grad(): 
        for data in test_loader: 
            inputs, outputs = data 
            predicted_outputs = model(inputs) 
            _, predicted = torch.max(predicted_outputs, 1) 
             
            label_correct_running = (predicted == outputs).squeeze() 
            label = outputs[0] 
            if label_correct_running.item():  
                labels_correct[label] += 1 
            labels_total[label] += 1  
  
    label_list = list(labels.keys()) 
    for i in range(output_size): 
        print('Accuracy to predict %5s : %2d %%' % (label_list[i], 100 * labels_correct[i] / labels_total[i]))
########

if __name__ == "__main__": 
    num_epochs = 10
    train(num_epochs) 
    print('Finished Training\n') 
    test() 
    test_species()

