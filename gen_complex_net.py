#########################################################################################################
# This file loads the Greater Burlington Area road network as a networkx graph object and simulates     #
# agents (drivers) on the network. The simulation is run for a given number of iterations and the 		  #
# number of iterations required for all drivers to reach the destination is returned.                   #
# Comparisons of the number of iterations required for different network topologies and different 		  #
# driver attributes are plotted and saved to the current working directory.                             #
#########################################################################################################

import osmnx as ox
import networkx as nx
import geopandas

def gen_data():
	"""
	Description:
	Retrieve Road Network Data within 20km of Burlington
	(Most of the Chittenden County road network)

	Params: 
	None

	Retuns:
	edges: geopandas.GeoDataFrame
	Numeric representation of road network.
	"""
	try:
		streets_graph = ox.load_graphml('btv_20km_streets.graphml')
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
		# streets_graph = ox.project_graph(streets_graph)
		streets_graph = ox.add_edge_speeds(G = streets_graph,
																			 hwy_speeds = speed_limits,
																			 fallback = 80.4672,
																			 precision = 4)
		streets_graph = ox.add_edge_travel_times(G = streets_graph,
																						 precision = 2)
		ox.save_graphml(streets_graph,
										filepath = "btv_20km_streets.graphml",
										encoding='utf-8')
	return ox.graph_to_gdfs(streets_graph)[1]

def gen_net(edges, node_vals: list) -> nx.Graph:
	"""
	Description:
	Build NetworkX Graph from Road Network Data.

	Params:
	edges: GeoDataFrame | Series[Unknown] | <subclass of Series and DataFrame>
		Numeric representation of road network.
	node_vals: list
			Node IDs and edge attributes.

	Returns:
	G: netowrkx.Graph
		NetworkX Graph object of road network.
		Includes node attribute for Traffic as "Queue".
	"""
	edges.reset_index(inplace=True)
	data_node_ats = edges[node_vals]
	G = nx.from_pandas_edgelist(data_node_ats, source=node_vals[0], target=node_vals[1], edge_attr=node_vals[2], create_using=nx.Graph())
	nx.set_node_attributes(G, values=[], name="Queue")
	for node in G.nodes:
		G.nodes[node]["Queue"] = []
	return G
