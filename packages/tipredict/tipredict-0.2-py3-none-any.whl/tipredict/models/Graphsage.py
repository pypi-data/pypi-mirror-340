from torch_geometric.nn import SAGEConv
import torch
import torch.nn.functional as F

class GraphSAGE(torch.nn.Module):
    def __init__(self, config):
        super(GraphSAGE, self).__init__()
        self.dropout = config.dropout_Gs
        in_dim = config.input_channels
        hidden_dim1 = config.hidden_channels1
        hidden_dim2 = config.hidden_channels2
        hidden_dim3 = config.hidden_channels3
        out_dim = config.out_channels
        self.penultimate_layer = config.penultimate_layer

        self.conv1 = SAGEConv(in_dim, hidden_dim1)
        self.conv2 = SAGEConv(hidden_dim1, hidden_dim2)
        self.conv3 = SAGEConv(hidden_dim2, hidden_dim3)
        self.conv4 = SAGEConv(hidden_dim3, out_dim)
    
    def forward(self, x, adj_t):
        x = self.conv1(x, adj_t)
        x = F.elu(x)
        x = F.dropout(x, p=self.dropout)
        
        x = self.conv2(x, adj_t)
        x = F.elu(x)
        x = F.dropout(x, p=self.dropout)
        
        x = self.conv3(x, adj_t)
        if self.penultimate_layer:
            return x
        x = F.elu(x)
        x = F.dropout(x, p=self.dropout)

        x = self.conv4(x, adj_t)
        
        return torch.log_softmax(x, dim=-1)