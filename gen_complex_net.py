import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import os

def gen_net(file_name: str, node_vals, out_file_name, classes) -> nx.Graph:
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
        roads["Weights"] = roads[node_vals[-1]].apply(lambda row: 1 if (row in classes) else 2)
        print(roads["Weights"])
        roads.rename(columns={node_vals[0]: "Source", 
                        node_vals[1]: "Target"}, inplace=True)
        roads.to_csv(out_file_name, index=False)
        
    roads = pd.read_csv(out_file_name)
    G = nx.from_pandas_edgelist(roads, source="Source", target="Target", 
                                 edge_attr=["Weights"], create_using=nx.Graph())
    return G


"""
The road classification in this data set is horrible, so there will be 
two different edge types, edges where there are assumed two lanes for 
each direction of traffic, and one lane. below are the encoded values
for edges that most likely do not contain two lanes for each direction 
of traffic
"""

not_two_lane_classes = [70, 80, 81, 82, 83, 86, 87, 88, 92, 96, 97, 98, 99,
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16]
net = gen_net("VT_Road_Centerline.geojson",  ["StartNodeID", "EndNodeID", 
                                             "AOTCLASS"], 
            "edge_complex_list.csv", not_two_lane_classes)
print(net.edges(data=True))