import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import collections
import numpy as np
import networkx as nx
import os
import seaborn as sns

def gen_net(file_name: str, node_vals, out_file_name) -> nx.DiGraph:
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
    G = nx.from_pandas_edgelist(roads, node_vals[0], node_vals[1], 
                                create_using=nx.DiGraph())
    return G

def stats(network: nx.DiGraph) -> None:
    """
    stats takes in a network file and gathers basic network
    stats to inform out models
    
    Params:
    network: given network object

    Returns: 
    None
    """
    degree_sequence = sorted([d for n, d in network.degree()], 
                            reverse=True)
    degcounts = collections.Counter(degree_sequence)
    deg, cnt = zip(*degcounts.items())
    plt.bar(deg, cnt, color='green')
    plt.xlabel("Degree")
    plt.ylabel("Log Counts")
    plt.title("Degree Distribution")
    sns.despine()
    plt.yscale("log")
    plt.savefig("degree_hist")
    

net = gen_net("VT_Road_Centerline.geojson",  ["StartNodeID", "EndNodeID"], 
                "edge_list.csv")
stats(net)
