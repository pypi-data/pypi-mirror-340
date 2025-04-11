import torch
class GraphSageConfig(object):
    def __init__(self):
        self.model_name = 'Graphsage'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.input_channels=34
        self.dropout_Gs = 0.5    
        self.hidden_channels1 = 64
        self.hidden_channels2 = 128
        self.hidden_channels3 = 256
        self.out_channels = 3                                                            
        self.penultimate_layer = False

class GATConfig(object):
    def __init__(self):
        self.model_name = 'GAT'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.n_feat=34
        self.hidden_channels1= 64
        self.hidden_channels2= 128
        self.hidden_channels3 = 256
        self.out_channels = 3
        self.heads = 8
        self.dropout_rate = 0.3
        self.penultimate_layer = False

class GINConfig(object):
    def __init__(self):
        self.model_name = 'GIN'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.input_channels=34
        self.dropout = 0.3
        self.output_channels = 3                                           
        self.hidden_channels1 = 64
        self.hidden_channels2 = 128
        self.hidden_channels3 = 256
        self.out_channels = 3
        self.penultimate_layer = False
        
class ensembleConfig(object):
    def __init__(self):
        self.model_name = 'GIN'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.input_channels=34
        self.K = 4
        self.k = 3
        self.feat_dim = 34
        self.hidden_dim = 64
        self.use_relu = True
        self.class_dim = 3
        self.alpha = 0.1
        self.dropout = 0.3
        self.output_channels = 3                                           
        self.num_epochs = 15000                                                                           
        self.learning_rate = 5e-3  
        self.hidden_channels1 = 64#
        self.hidden_channels2 = 128
        self.hidden_channels3 = 256
        self.output_dim = 3
        self.n_feat=34
        self.out_channels = 3
        self.output_dim = 3
        self.heads = 8
        self.dropout_rate = 0.3
        self.dropout_Gs = 0.5
        self.saveDir = "030405xgb"
        self.input_dim = 34
        self.hidden_dim1 = 64
        self.hidden_dim2 = 128
        self.hidden_dim3 = 256
        self.Init = "PPR"
        self.num_classes = 3        
        self.Gamma = [] #should be a vector
        self.penultimate_layer = False

class DAGTransformerConfig(object):
    def __init__(self):
        self.model_name='DAGTransformer'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   
        self.dropout = 0.3                                              
        self.num_classes = 3                                            
        self.num_epochs = 500                                          
        self.batch_size = 500                                         
        self.num_task = 7                                             
        self.learning_rate = 1e-4     
        self.n_feat = 34
        self.hidden_dim = 1024
        self.num_head = 8
        self.num_encoder = 6
        self.d_k=512
        self.res_num_layer=4
        self.structure=True
        self.penultimate_layer = False