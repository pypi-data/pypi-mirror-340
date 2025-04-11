import torch
from tipredict.models.GAT_torch_geometric import GATGeometric 
from tipredict.models.GIN import GIN as GIN_model
from tipredict.models.Graphsage import GraphSAGE
from .configs import GATConfig,GINConfig,GraphSageConfig,DAGTransformerConfig
import torch.nn.functional as F
from tipredict.models.DAG_Transformer import DAGTransformer
from importlib.resources import files
def run_pretrained(model="GAT", num_tasks="7", memory=False, data_GNN=False, data_DAGTransformer=False, penultimateLayer=False):
    if model not in ["GIN","GAT","GraphSAGE","GNN_ensemble","DAGTransformer","DT&GNN"]:
        raise KeyError('model must be in ["GIN","GAT","GraphSAGE","GNN_ensemble","DAGTransformer","DT&GNN"].')
    if memory not in [True,False]:
        raise KeyError('memory must be a boolean.')
    if not isinstance(num_tasks, int):
        raise KeyError('num_tasks must be an integer.')
    if model in ["DAGTransformer","DT&GNN"]:
        if data_DAGTransformer == False:
            raise ValueError(f"data_DAGTransformer must not be False when applying {model}")    
    if model in ["GIN","GAT","GraphSAGE","GNN_ensemble","DT&GNN"]:
        if data_GNN == False:
            raise ValueError(f"data_GNN must not be False when applying {model}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if (model == "GNN_ensemble" or model == "DT&GNN") and penultimateLayer:
        raise KeyError(f"penultimateLayer not callable on ensemble models because of different dimension sizes")

    if model == "GIN":
        config = GINConfig()
        if penultimateLayer:
            config.penultimate_layer = True
        GIN = GIN_model(config)
        if not memory:
            GIN.load_state_dict(torch.load(files("tipredict.weights").joinpath("GIN_cpu.pth"), map_location=device))
        else:
            GIN.load_state_dict(torch.load(files("tipredict.weights").joinpath("GIN_mem.pth"), map_location=device))
        GIN.to(device)
        GIN.eval()
        data_GNN = data_GNN.to(device)
        h, adj = data_GNN.x, data_GNN.edge_index
        outputs = GIN(h, adj)
        if penultimateLayer:
            return outputs
        predictions = torch.max(outputs[data_GNN.mask], 1)[1]
    
    elif model == "GAT":
        config = GATConfig()
        if penultimateLayer:
            config.penultimate_layer = True
        GAT = GATGeometric(config)
        if not memory:
            GAT.load_state_dict(torch.load(files("tipredict.weights").joinpath("GAT_cpu.pth"), map_location=device))
        else:
            GAT.load_state_dict(torch.load(files("tipredict.weights").joinpath("GAT_mem.pth"), map_location=device))
        GAT.to(device)
        GAT.eval()
        data_GNN = data_GNN.to(device)
        h, adj = data_GNN.x, data_GNN.edge_index
        outputs = GAT(h, adj)
        if penultimateLayer:
            return outputs
        predictions = torch.max(outputs[data_GNN.mask], 1)[1]
    
    elif model == "GraphSAGE":
        config = GraphSageConfig()
        if penultimateLayer:
            config.penultimate_layer = True
        GS = GraphSAGE(config)
        if not memory:
            GS.load_state_dict(torch.load(files("tipredict.weights").joinpath("Graphsage_cpu.pth"), map_location=device))
        else:
            GS.load_state_dict(torch.load(files("tipredict.weights").joinpath("Graphsage_mem.pth"), map_location=device))
        GS.to(device)
        GS.eval()
        data_GNN = data_GNN.to(device)
        h, adj = data_GNN.x, data_GNN.edge_index
        outputs = GS(h, adj)
        if penultimateLayer:
            return outputs
        predictions = torch.max(outputs[data_GNN.mask], 1)[1]
    
    elif model == "GNN_ensemble":
        GS_config = GraphSageConfig()
        GAT_Config = GATConfig()
        GIN_Config = GINConfig()
        GS = GraphSAGE(GS_config)
        GAT = GATGeometric(GAT_Config)
        GIN = GIN_model(GIN_Config)
        if not memory:
            GS.load_state_dict(torch.load(files("tipredict.weights").joinpath("Graphsage_cpu.pth"), map_location=device))
            GIN.load_state_dict(torch.load(files("tipredict.weights").joinpath("GIN_cpu.pth"), map_location=device))
            GAT.load_state_dict(torch.load(files("tipredict.weights").joinpath("GAT_cpu.pth"), map_location=device))
        else:
            GS.load_state_dict(torch.load(files("tipredict.weights").joinpath("Graphsage_mem.pth"), map_location=device))
            GIN.load_state_dict(torch.load(files("tipredict.weights").joinpath("GIN_mem.pth"), map_location=device))
            GAT.load_state_dict(torch.load(files("tipredict.weights").joinpath("GAT_mem.pth"), map_location=device))
        data_GNN = data_GNN.to(device)
        h, adj = data_GNN.x, data_GNN.edge_index
        for GNN_model in [GS,GIN,GAT]:
            GNN_model.to(device)
            GNN_model.eval()
        outputs_GIN = GIN(h,adj)
        outputs_GAT = GAT(h,adj)
        outputs_GS = GS(h,adj)
        outputs = (outputs_GAT + outputs_GIN + outputs_GS)/3
        if penultimateLayer:
            return outputs
        outputs = F.softmax(outputs, dim=1)
        predictions = torch.max(outputs[data_GNN.mask], 1)[1]

    elif model == "DAGTransformer":
        config = DAGTransformerConfig()
        if penultimateLayer:
            config.penultimate_layer = True
            data_loader=torch.utils.data.DataLoader(dataset=data_DAGTransformer,batch_size=len(data_DAGTransformer),num_workers=2,shuffle=False)
        else:
            data_loader=torch.utils.data.DataLoader(dataset=data_DAGTransformer,batch_size=500,num_workers=2,shuffle=False)

        Transformer = DAGTransformer(config)
        if not memory:
            Transformer.load_state_dict(torch.load(files("tipredict.weights").joinpath("DAGTransformer_cpu.pth"), map_location=device))
        else:
            Transformer.load_state_dict(torch.load(files("tipredict.weights").joinpath("DAGTransformer_mem.pth"), map_location=device))
        Transformer.to(device)
        Transformer.eval()
        predictions = torch.LongTensor([]).to(device)
        with torch.no_grad():
            for (texts, poss, masks) in data_loader:
                texts=texts.float().to(device)
                poss=poss.float().to(device)
                masks=masks.float().to(device)
                outputs = Transformer(texts,poss,masks)
                if penultimateLayer:
                    return outputs
                predic = torch.max(outputs.data, 1)[1]
                predictions = torch.cat((predictions, predic),0)
    
    elif model == "DT&GNN":
        GS = GraphSAGE(GraphSageConfig())
        GAT = GATGeometric(GATConfig())
        GIN = GIN_model(GINConfig())
        if not memory:
            GS.load_state_dict(torch.load(files("tipredict.weights").joinpath("Graphsage_cpu.pth"), map_location=device))
            GIN.load_state_dict(torch.load(files("tipredict.weights").joinpath("GIN_cpu.pth"), map_location=device))
            GAT.load_state_dict(torch.load(files("tipredict.weights").joinpath("GAT_cpu.pth"), map_location=device))
        else:
            GS.load_state_dict(torch.load(files("tipredict.weights").joinpath("Graphsage_mem.pth"), map_location=device))
            GIN.load_state_dict(torch.load(files("tipredict.weights").joinpath("GIN_mem.pth"), map_location=device))
            GAT.load_state_dict(torch.load(files("tipredict.weights").joinpath("GAT_mem.pth"), map_location=device))
        data_GNN = data_GNN.to(device)
        h, adj = data_GNN.x, data_GNN.edge_index
        for GNN_model in [GS,GIN,GAT]:
            GNN_model.to(device)
            GNN_model.eval()

        data_loader=torch.utils.data.DataLoader(dataset=data_DAGTransformer,batch_size=len(data_DAGTransformer),num_workers=2,shuffle=False)
        Transformer = DAGTransformer(DAGTransformerConfig())
        if not memory:
            Transformer.load_state_dict(torch.load(files("tipredict.weights").joinpath("DAGTransformer_cpu.pth"), map_location=device))
        else:
            Transformer.load_state_dict(torch.load(files("tipredict.weights").joinpath("DAGTransformer_mem.pth"), map_location=device))
        Transformer.to(device)
        Transformer.eval()
        with torch.no_grad():
            for (texts, poss, masks) in data_loader:
                texts=texts.float().to(device)
                poss=poss.float().to(device)
                masks=masks.float().to(device)
                predictions_DT = Transformer(texts,poss,masks)
                predictions_DT_final = torch.zeros(predictions_DT.shape[0]*num_tasks, predictions_DT.shape[1])
                predictions_DT_final[num_tasks-1::num_tasks] = predictions_DT
        outputs_GIN = GIN(h,adj)
        outputs_GAT = GAT(h,adj)
        outputs_GS = GS(h,adj)
        outputs = (outputs_GAT + outputs_GIN + outputs_GS + predictions_DT_final.to(device))/4
        outputs = F.softmax(outputs, dim=1)
        predictions = torch.max(outputs[data_GNN.mask], 1)[1]
    
    predictions[predictions==1] = 3
    predictions[predictions==2] = 1
    predictions[predictions==3] = 2
    
    return predictions