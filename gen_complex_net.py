import osmnx as ox
import networkx as nx
import geopandas

def gen_data()-> geopandas.geodataframe.GeoDataFrame:

    """

    gen_net gathers network data for Chittendan County

    Params: 
    None

    Retuns:
    network digraph
    """

    try:
        streets_graph = ox.io.load_graphml('btv_20km_streets.graphml')
    except FileNotFoundError:
        streets_graph = ox.graph_from_place('Burlington, Vermont',
                                            network_type ='drive',
                                            simplify = True,
                                            retain_all = False,
                                            truncate_by_edge = False,
                                            which_result = None,
                                            buffer_dist = 20000,
                                            clean_periphery = True,
                                            custom_filter = None)
        
        speed_limits = {'motorway' : 104.67,
                        'trunk' : 64.3738,
                        'primary' : 80.4672,
                        'secondary' : 80.4672, 
                        'tertiary' : 80.4672, 
                        'unclassified' : 80.4672, 
                        'residential' : 40.2336, 
                        'service' : 40.2336, 
                        'motorway_link' : 80.4672, 
                        'trunk_link' : 64.3738, 
                        'primary_link' : 104.67, 
                        'secondary_link' : 104.67, 
                        'motorway_junction' : 104.67}

        streets_graph = ox.projection.project_graph(streets_graph)

        streets_graph = ox.speed.add_edge_speeds(G = streets_graph,
                                                hwy_speeds = speed_limits,
                                                fallback = 80.4672,
                                                precision = 4)

        streets_graph = ox.speed.add_edge_travel_times(G = streets_graph,
                                                        precision = 2)
        
        ox.io.save_graphml(streets_graph, filepath = "tv_20km_streets.graphml", 
        encoding='utf-8')
    
    return ox.utils_graph.graph_to_gdfs(streets_graph)[1]


def gen_net(data: geopandas.geodataframe.GeoDataFrame, node_vals: list) -> nx.Graph():
    """
    gen_net generates the road networok from the subset of data

    Params:
    data: geopandas data frame of road features
    node_vals: names of nodes and their weights

    Returns:
    netowrkx graph
    """

    data.reset_index(inplace=True)
    data_node_ats = data[node_vals]
    G =nx.from_pandas_edgelist(data_node_ats, source=node_vals[0], target=node_vals[1],
                                edge_attr=node_vals[2], create_using=nx.Graph())
    nx.set_node_attributes(G, values={"queue": list()}, name="Queue")
    
    return G
