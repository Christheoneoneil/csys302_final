import geopandas
import matplotlib.pyplot as plt
import momepy
import networkx as nx


def gen_net(file_name: str, node_vals) -> nx.Graph:
    """
    gen_net takes in a file and returns a network x network
    :param file_name: name of geodata file
    :param node_vals: list of feature names that contain node info
    """
    roads = geopandas.read_file(file_name)
    roads = roads[node_vals]
    G = nx.from_pandas_edgelist(roads, node_vals[0], node_vals[1], create_using=nx.DiGraph())
    return G

net = gen_net("VT_Road_Centerline.geojson",  ["StartNodeID", "EndNodeID"])
print(net)