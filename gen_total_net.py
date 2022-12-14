import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import collections
import networkx as nx
import os
import seaborn as sns

def gen_net(file_name: str, node_vals: list, out_file_name: str) -> nx.Graph:
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
        roads.rename(columns={node_vals[0]: "Source", 
                        node_vals[1]: "Target"}, inplace=True)
        roads.to_csv(out_file_name, index=False)
        
    roads = pd.read_csv(out_file_name)
    G = nx.from_pandas_edgelist(roads, source="Source", target="Target", 
                                create_using=nx.Graph())
    return G

def stats(network: nx.Graph) -> None:
    """
    stats takes in a network file and gathers basic network
    stats to inform our models
    
    Params:
    network: given network object

    Returns:
    None
    """
    
    print(network)
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
    
    density = nx.density(network)
    print("Network density:", density)

    pears_corr = nx.degree_assortativity_coefficient(network)
    print("Avg Pearosn Corr Coeff", pears_corr)

net = gen_net("VT_Road_Centerline.geojson",  ["StartNodeID", "EndNodeID"], 
                "edge_simple_list.csv")
stats(net)
