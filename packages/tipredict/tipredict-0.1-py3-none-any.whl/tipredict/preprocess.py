
import torch
import numpy as np
import pandas as pd
import numpy as np
from tqdm import tqdm
import torch
from torch_geometric.data import Data
import numpy as np
import torch
from importlib.resources import files

def prepare_data(df_path,dag_path):
    df=pd.read_csv(df_path)
    dag=pd.read_csv(dag_path)
    return df, dag  

def preprocess_GNN(num_task=7,df_path="path_to_dataframe_csv",dag_path="path_to_DAG_csv",num_feat=34):
    df, df_dag = prepare_data(df_path,dag_path)
    feat=df.to_numpy().reshape(-1,num_feat)
    edge_info=df_dag.to_numpy().reshape(-1,2*num_task+1)
    edge_info=edge_info[:,1:]
    out_mat=edge_info[:,:num_task]
    edge=torch.tensor([[],[]],dtype=torch.long)
    print('preparing data...')
    for src in tqdm(range(out_mat.shape[0])):
        for tgt in range(num_task):
            if(out_mat[src,tgt]!=0):
                edge=torch.cat((edge,torch.tensor([[src],[src+(tgt-src%num_task)]],dtype=torch.long),
                           torch.tensor([[src+(tgt-src%num_task)],[src]],dtype=torch.long)),1)
    self_loop=torch.tensor([[x for x in range(df.shape[0]*num_task)],[x for x in range(df.shape[0]*num_task)]],dtype=torch.long)
    edge=torch.cat((edge,self_loop),1)
    feat_min = np.loadtxt(files("tipredict").joinpath("min.csv"),delimiter=",")
    feat_max = np.loadtxt(files("tipredict").joinpath("max.csv"),delimiter=",")
    denominator = feat_max - feat_min
    denominator[denominator == 0] = 1
    feat = (feat - feat_min) / denominator
    feat=torch.tensor(feat,dtype=torch.float)
    Gdata = Data(x=feat, edge_index=edge)
    Gdata.mask=torch.ByteTensor([False for x in range(df.shape[0]*num_task)]).bool()
    for x in range(df.shape[0]*num_task):
        if(x+1)%num_task==0:
            Gdata.mask[x]=True
    return Gdata

def preprocess_dagtransformer(num_task=7,df_path="path_to_workflow_csv",dag_path="path_to_DAG_csv",num_head=8,num_feat=34):
    df, dag=prepare_data(df_path,dag_path)
    ##nodes features
    arr=np.array(df)
    data=np.vstack(arr.reshape(arr.shape[0]*num_task,num_feat))
    min = np.loadtxt(files("tipredict").joinpath("min.csv"),delimiter=",")
    max = np.loadtxt(files("tipredict").joinpath("max.csv"),delimiter=",")
    denominator = max - min
    denominator[denominator == 0] = 1
    data = (data - min) / denominator
    data=data[:arr.shape[0]*num_task,:]
    data=data.reshape(-1,num_task,num_feat)
    #####dag info
    dag=dag.to_numpy().reshape(-1,num_task,num_task*2+1)
    dag=dag[:,:,1:]
    dagout=dag[:,:,:num_task]
    dagin=dag[:,:,num_task:]
    mask=dagin+dagout
    pos=np.zeros((arr.shape[0],num_task))
    for x in range(pos.shape[0]):
        pos[x]=find_pos(dagout[x],num_task)
    position=create_position(pos,num_feat)
    mask=create_attn_mask(mask,num_heads=num_head,num_nodes=num_task)
    data=np.array(data,dtype=np.float32)
    position=np.array(position,dtype=np.float32)
    ######data
    final_data=[]
    for x in range(data.shape[0]):
        final_data.append((data[x],position[x],mask[x]))

    return final_data

def create_position(pos,num_feat):
    pe = np.array([[[posit / (10000.0 ** (i // 2 * 2.0 / num_feat))  for i in range(num_feat)]for posit in posi] for posi in pos])
    pe[:,:,0::2]=np.sin(pe[:,:,0::2])
    pe[:,:,1::2]=np.cos(pe[:,:,1::2])
    return pe

def create_attn_mask(tensor,num_heads,num_nodes):
    mask=np.zeros(((tensor.shape[0]*num_heads),tensor.shape[1],tensor.shape[2]))
    for x in range(0,mask.shape[0],num_heads):
        mask[x:x+num_heads]=tensor[x//num_heads]+np.eye(num_nodes)
    return mask.reshape(tensor.shape[0],num_heads,tensor.shape[1],tensor.shape[2])

def find_pos(out_degree_matrix,num_nodes):
    stage=np.zeros(num_nodes)
    signal=True
    cycle = False
    while signal:
        temp=stage.copy()
        for m in range(num_nodes):
            for n in range(num_nodes):
                if stage[n] > num_nodes:
                    signal=False
                    cycle = True
                    break
                if(out_degree_matrix[m,n]!=0):
                    stage[n]=max(stage[n],stage[m]+1)
        if (temp==stage).all():
            signal=False
    if cycle:
        return np.zeros(num_nodes)
    return stage

def normalize(features):
    feat_min = np.loadtxt("min.csv", delimiter=",")
    feat_max = np.loadtxt("max.csv", delimiter=",")
    denominator = feat_max - feat_min
    denominator[denominator == 0] = 1
    features = (features - feat_min) / denominator
    return features