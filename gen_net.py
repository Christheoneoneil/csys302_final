import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import momepy
import networkx as nx
import os

def gen_net(file_name: str, node_vals, out_file_name) -> nx.Graph:
    """
    gen_net takes in a file and returns a network x network
    
    Params:
    file_name: name of geodata file
    node_vals: list of feature names that contain node info
    out_file_name: name of subset file 

    Returns: 
    graph of given data
    """
    list_dir = os.listdir()
    list_diff = list(set([out_file_name])-set(list_dir))
    
    if list_diff == [out_file_name]: 
        roads = geopandas.read_file(file_name)
        roads = roads[node_vals] 
        roads.to_csv(out_file_name)
        
    roads = pd.read_csv(out_file_name)
    G = nx.from_pandas_edgelist(roads, node_vals[0], node_vals[1], create_using=nx.DiGraph())
    return G

net = gen_net("VT_Road_Centerline.geojson",  ["StartNodeID", "EndNodeID"], "edge_list.csv")
print(net)