import torch
import torch.nn.functional as F
from torch_geometric.nn import GINConv,APPNP
from torch_geometric.nn import Sequential
#https://projects.volkamerlab.org/teachopencadd/talktorials/T035_graph_neural_networks.html
class GIN(torch.nn.Module):
    def __init__(self, config):
        super(GIN, self).__init__()
        self.input_channels = config.input_channels
        self.output_channels = config.output_channels
        self.hidden_channels1 = config.hidden_channels1
        self.hidden_channels2 = config.hidden_channels2
        self.hidden_channels3 = config.hidden_channels3
        self.dropout = config.dropout
        self.penultimate_layer = config.penultimate_layer
        # Define the GIN layers
        self.conv1 = GINConv(
            Sequential('x, edge_index', [
                (torch.nn.Linear(self.input_channels, self.hidden_channels1), 'x -> x'),
                torch.nn.BatchNorm1d(self.hidden_channels1),
                torch.nn.ReLU(),
                torch.nn.Linear(self.hidden_channels1, self.hidden_channels1),
                torch.nn.ReLU(),
                torch.nn.Linear(self.hidden_channels1,self.hidden_channels1)
            ])
        )
        
        self.conv2 = GINConv(
            Sequential('x, edge_index', [
                (torch.nn.Linear(self.hidden_channels1, self.hidden_channels2), 'x -> x'),
                torch.nn.BatchNorm1d(self.hidden_channels2),
                torch.nn.ReLU(),
                torch.nn.Linear(self.hidden_channels2, self.hidden_channels2),
                torch.nn.ReLU(),
                torch.nn.Linear(self.hidden_channels2,self.hidden_channels2)
            ])
        )
        
        self.conv3 = GINConv(
            Sequential('x, edge_index', [
                (torch.nn.Linear(self.hidden_channels2, self.hidden_channels3), 'x -> x'),
                torch.nn.BatchNorm1d(self.hidden_channels3),
                torch.nn.ReLU(),
                torch.nn.Linear(self.hidden_channels3, self.hidden_channels3),
                torch.nn.ReLU(),
                torch.nn.Linear(self.hidden_channels3,self.hidden_channels3)
            ])
        )
        
        self.conv4 = GINConv(
            Sequential('x, edge_index', [
                (torch.nn.Linear(self.hidden_channels3, self.output_channels), 'x -> x')
            ])
        )
        self.res_proj1 = torch.nn.Linear(self.input_channels, self.hidden_channels1)
        self.res_proj2 = torch.nn.Linear(self.hidden_channels1, self.hidden_channels2)
        self.res_proj3 = torch.nn.Linear(self.hidden_channels2, self.hidden_channels3)
        self.lv1= torch.nn.Parameter(torch.randn(self.hidden_channels1,self.hidden_channels1))
        self.lv2= torch.nn.Parameter(torch.randn(self.hidden_channels2,self.hidden_channels2))
        self.lv3= torch.nn.Parameter(torch.randn(self.hidden_channels3,self.hidden_channels3))
        self.appnp = APPNP(K=4, alpha=0.1, dropout=self.dropout, add_self_loops=False)
        self.reset_parameters()
        
    def reset_parameters(self):
        # Xavier initialization for learnable matrices
        torch.nn.init.xavier_uniform_(self.lv1)
        torch.nn.init.xavier_uniform_(self.lv2)
        torch.nn.init.xavier_uniform_(self.lv3)

    def forward(self, x, edge_index):
        # Forward pass through each layer
        identity = self.res_proj1(x)
        x = self.conv1(x, edge_index)
        x = F.dropout(x, p=self.dropout)
        x += identity
        #x = x@self.lv1
        x = F.relu(x)
        
        identity = self.res_proj2(x)
        x = self.conv2(x, edge_index)
        x = F.dropout(x, p=self.dropout)
        x += identity
        #x = x@self.lv2
        x = F.relu(x)

        identity = self.res_proj3(x)
        x = self.conv3(x, edge_index)
        if self.penultimate_layer:
            return x
        x = F.dropout(x, p=self.dropout)
        x += identity
        #x = x@self.lv3
        x = F.relu(x)

        x = self.conv4(x, edge_index)
        #x=self.appnp(x,edge_index)
        return F.log_softmax(x,dim=1)

