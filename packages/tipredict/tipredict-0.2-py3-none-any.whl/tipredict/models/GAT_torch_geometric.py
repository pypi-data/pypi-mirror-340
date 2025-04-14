
from torch_geometric.nn import GCNConv,GATConv
import torch
import torch.nn.functional as F

class GATGeometric(torch.nn.Module):
    def __init__(self, config):
        super(GATGeometric, self).__init__()
        torch.manual_seed(12345)
        self.heads= config.heads
        self.n_feat = config.n_feat
        self.penultimate_layer = config.penultimate_layer
        self.hidden_channels1 = config.hidden_channels1
        self.hidden_channels2 = config.hidden_channels2
        self.hidden_channels3 = config.hidden_channels3
        self.dropout = config.dropout_rate
        self.conv1 = GATConv(self.n_feat, self.hidden_channels1, self.heads, self.dropout)
        self.conv2 = GATConv(self.hidden_channels1 * self.heads, self.hidden_channels2, self.heads//2, self.dropout)
        self.conv3 = GATConv(self.hidden_channels2 * self.heads//2, self.hidden_channels3, self.heads//4, self.dropout)
        # On the Pubmed dataset, use heads output heads in conv2.
        self.conv4 = GATConv(self.hidden_channels3 *  self.heads//4, config.out_channels, heads=1,
                             concat=False, dropout=self.dropout)
        self.res_proj1 = torch.nn.Linear(self.n_feat, self.hidden_channels1*self.heads)
        self.res_proj2 = torch.nn.Linear(self.hidden_channels1*self.heads, self.hidden_channels2*self.heads//2)
        self.res_proj3 = torch.nn.Linear(self.hidden_channels2*self.heads//2, self.hidden_channels3*self.heads//4)
        #self.bn1 = F.BatchNorm1d(self.hidden_channels1)
        #self.bn2 = F.BatchNorm1d(self.hidden_channels2)
        #self.bn3 = F.BatchNorm1d(self.hidden_channels3)
    def reset_parameters(self):
        self.conv1.reset_parameters()
        self.conv2.reset_parameters()

    def forward(self, x, edge_index):
        #x = F.dropout(x, p=self.dropout, training=self.training)
        #identity = self.res_proj1(x)
        x = F.elu(self.conv1(x, edge_index))
        #x = self.bn1(x)
        #x+=identity
        x = F.dropout(x, p=self.dropout)
        #identity = self.res_proj2(x)
        x = F.elu(self.conv2(x, edge_index))
        #x = self.bn2(x)
        #x+=identity
        x = F.dropout(x, p=self.dropout)
        #identity = self.res_proj3(x)
        x = self.conv3(x,edge_index)
        if self.penultimate_layer:
            return x
        x = F.elu(x)
        #x = self.bn3(x)
        #x+=identity
        x = F.dropout(x, p=self.dropout)
        x = self.conv4(x, edge_index)
        
        return F.log_softmax(x,dim=1)