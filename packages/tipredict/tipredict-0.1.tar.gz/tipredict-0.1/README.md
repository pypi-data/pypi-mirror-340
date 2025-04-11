Manual

The models in this package were trained on Alibaba Cluster-Trace-v2018. The measurements for CPU and memory average are found in
https://github.com/alibaba/clusterdata/blob/master/cluster-trace-v2018/schema.txt

Since Cuda is not supported for pip, torch and torch_geometric have to be installed manually!
The following versions work and higher versions will likely work as well, but make sure that torch and torch-geometric versions match.
versions:
torch 2.0.0+cu118 
torch-geometric 2.6.1

functions:
from tipredict import preprocess_GNN, run_pretrained, preprocess_dagtransformer, normalize

Inputs (with headers, else first row isnt read & predicted!):
#################################################################################
input 1:
-workflow csv 
shape number_wokflows x (34 task level features * number_tasks), predicted task features are set 0
----------------------------------------------------------
features:

(the task level features are aggregations of the instance measurements)

count of instances
mean_ca Average of CPU average usage
var_ca Variance of CPU average usage
max_ca Maximum of CPU average usage 
min_ca Minimum of CPU average usage 
med_ca Median of CPU average usage 
skew_ca Skewness of CPU average usage 
kurt_ca Kurtosis of CPU average usage 

mean_cm Average of CPU maximum usage
var_cm Variance of CPU maximum usage
max_cm Maximum of CPU maximum usage
min_cm Minimum of CPU maximum usage
med_cm Median of CPU maximum usage
skew_cm Skewness of CPU maximum usage
kurt_cm Kurtosis of CPU maximum usage

mean_ma Average of memory average usage 
var_ma Variance of memory average usage 
max_ma Maximum of memory average usage 
min_ma Minimum of memory average usage 
med_ma Median of memory average usage 
skew_ma Skewness of memory average usage 
kurt_ma Kurtosis of memory average usage 

mean_mm Average of memory maximum usage
var_mm Variance of memory maximum usage
max_mm Maximum of memory maximum usage
min_mm Minimum of memory maximum usage
med_mm Median of memory maximum usage
skew_mm Skewness of memory maximum usage
kurt_mm Kurtosis of memory maximum usage

mean_t Average running time 
max_t Maximum running time
var_t Variance of running time
min_t Minimum running time
maxtime Actual running time
----------------------------------------------------------


input 2:
-DAG csv
-shape number_workflows x ((2*number_tasks+1)*number_tasks)
for each task 15 features:
----------------------------------------------------------
Feature example for a 3-task-workflow
#comment: if a node has multiple incoming or outgoing edges, the feature is 10/number of edges

position 1
1o_1 0  #1 has no edge leading to 1
1o_2 10/2 = 5	#1 has an edge leading to 2
1o_3 10/2 = 5	#1 has an edge leading to 3
1i_1 0  #1 has no incoming edge from 1
1i_2 0  #1 has no incoming edge from 2
1i_3 0  #1 has no incoming edge from 3
position 2
2o_1 0  #2 has no edge leading to 1
2o_2 0  #2 has no edge leading to 2
2o_3 10  #2 has an edge leading to 3
2i_1 10  #2 has an incoming edge from 1
2i_2 0  #2 has no incoming edge from 2
2i_3 0  #2 has noincoming edge from 3
position 3
3o_1 0	#similarly
3o_2 0
3o_3 0
3i_1 10/2 = 5
3i_2 10/2 = 5
3i_3 0 
--------------------------------------------------------------
#################################################################################

applications:
preprocess_GNN(num_tasks, feature-csv, dag-csv) -> preprocesses the input data into GNN format
preprocess_dagtransformer(num_tasks, feature-csv, dag-csv) -> preprocesses the input data into DAGTransformer format
normalize(features) -> normalizes input features of shape tasks x 34 (features) for GNN usage to enable building an own preprocessing pipeline

run_pretrained(model,num_tasks,memory,data_GNN,data_DAGTransformer,penultimateLayer)
inputs:
model ("GAT","GIN","GraphSAGE","GNN_ensemble","DAGTransformer","DT&GNN")
num_tasks -> number of tasks per workflow
memory -> predict memory (boolean, if false predict cpu)

(you can use the output of preprocess_GNN and preprocess_dagtransformer for the following inputs):
data_GNN -> preprocessed data for GNN models, if DAGTransformer use False
data_DAGTransformer -> preprocessed data for DAGTransformer, if not included in model use False

penultimateLayer -> True, returns penultimate layer of the model for further processing, False returns the predicted label directly
