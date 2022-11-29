import collections
from contextily import add_basemap
import geopandas
import matplotlib.pyplot as plt
import momepy
import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
import seaborn as sns

def gen_net()-> None:

    """

    gen_net gathers network data for Chittendan County

    Params: 
    None

    Retuns:
    Pandas csv of network data
    """
    streets_graph = ox.graph_from_place('Burlington, Vermont',
                                        network_type ='drive',
                                        simplify = True,
                                        retain_all = False,
                                        truncate_by_edge = False,
                                        which_result = None,
                                        buffer_dist = 10000,
                                        clean_periphery = True,
                                        custom_filter = None)

    streets_graph = ox.projection.project_graph(streets_graph)

    streets = ox.graph_to_gdfs(ox.get_undirected(streets_graph),
                            nodes=False,
                            edges=True,
                            node_geometry=False,
                            fill_edge_geometry=True)

    streets["lanes"] = streets["lanes"].fillna(1)
    return streets

net = gen_net()
