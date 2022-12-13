#########################################################################################################
# This file loads the Greater Burlington Area road network as a networkx graph object and simulates     #
# agents (drivers) on the network. The simulation is run for a given number of iterations and the 		  #
# number of iterations required for all drivers to reach the destination is returned.                   #
# Comparisons of the number of iterations required for different network topologies and different 		  #
# driver attributes are plotted and saved to the current working directory.                             #
#########################################################################################################

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import random
from gen_complex_net import gen_net
from gen_complex_net import gen_data

def generate_drivers(num_drivers: int, bad_driver_prop: float, states: list) -> list:
	"""
	generate drivers generates an array of randomly chosen good and bad drivers

	Params:
	num_drivers: total number of drivers
	bad_driver_prop: proportion of bad drivers on the network
	states: state of drivers

	Returns:
	list of drivers and their state
	"""
	return [{key: {'State': random.choices(states, [1 - bad_driver_prop, bad_driver_prop])[0], 'Iterations': 0}} for key in np.arange(1, num_drivers + 1, 1)]

def traverse_nodes(node, network, end_node, good_driver_path, prob_wrong_turn, active_nodes, iteration_check):
	"""
	Search node for queue of drivers
	If queue is not empty, pop first driver and check state
	If state is good, send driver to next node in good driver path
	If state is bad, send driver to next node in bad driver path
	If queue is empty, remove node from active nodes

	Params:
	node: <int> current node id
	network: <nx.Graph> networkx graph object
	end_node: <int> destination node id
	good_driver_path: <list> shortest path from start node to end node
	prob_wrong_turn: <float> probability of bad driver taking wrong turn
	active_nodes: <set> set of nodes with active drivers
	iteration_check: <int> number of iterations

	Returns:
	end_drivers: <list> of drivers at the destination
	"""
	if node != end_node:
		try:
			drivers = network.nodes[node]["Queue"]
			try:
				first_out = drivers.pop(0)
			except IndexError:
				active_nodes[node] = 0
			driver_id = list(first_out.keys())[0]
			state = first_out[driver_id]['State']
			iterations = first_out[driver_id]['Iterations']
			first_out[driver_id]['Iterations'] = iterations + 1
			iteration_check = iteration_check + 1
			if state == "good":
				current_node_ind = good_driver_path.index(node)
				next_step = good_driver_path[current_node_ind + 1]
				network.nodes[next_step]["Queue"].append(first_out)
			else:
				turn_choice = random.choices(["on_path", "off_path"], [1-prob_wrong_turn, prob_wrong_turn])[0]
				if turn_choice == "off_path":
					next_step = random.choice(list(network.neighbors(node)))
				else:
					bad_driver_path = nx.shortest_path(network, source=node, target=end_node, method='dijkstra', weight="length")
					current_node_ind = bad_driver_path.index(node)
					next_step = bad_driver_path[current_node_ind + 1]
				network.nodes[next_step]["Queue"].append(first_out)
				active_nodes[node] = next_step
		except ValueError:
			active_nodes[node] = 0
	return [list(driver.keys())[0] for driver in network.nodes[end_node]["Queue"]], network

def run_model(drivers: list, network: nx.Graph, origin_node: int, end_node: int, prob_wrong_turn: float):
	"""
	run_model runs a model with the given generated drivers

	Params:
	drivers: array of drivers of given attributes
	network: networkx graph object
	origin_node: node point of origin
	end_node: node point of sink
	prob_wrong_turn: probability that bad driver makes a random turn
	at a given node

	Returns:
	number of iterations required for all drivers to get to final
	destination
	"""

	nx.set_node_attributes(network,
												 [],
												 "Queue")
	network.nodes[origin_node]["Queue"] = drivers
	# network.nodes["Queue"] += drivers
	good_driver_path = nx.shortest_path(network,
																			source=origin_node,
																			target=end_node,
																			method='dijkstra',
																			weight="length")
	init_drivers = [list(driver.keys())[0] for driver in network.nodes[origin_node]["Queue"]]

	driver_states = list(nx.get_node_attributes(network, 'State').values())

	good_drivers = driver_states.count('good')
	bad_drivers = driver_states.count('bad')

	end_drivers = []
	comp_good = {}
	comp_bad = {}
	active_nodes = {i: 1 for i in good_driver_path}
	iteration_check = 0

	while not end_drivers or sorted(init_drivers) != sorted(end_drivers):
		for node in active_nodes:
			end_drivers, network = traverse_nodes(end_drivers, node, network, end_node, good_driver_path, prob_wrong_turn, active_nodes, iteration_check)
			good_complete = [list(driver.values())[0]['State'] for driver in network.nodes[end_node]["Queue"]].count('good')
			bad_complete = [list(driver.values())[0]['State'] for driver in network.nodes[end_node]["Queue"]].count('bad')
			if good_complete != 0:
				comp_good[good_complete] = iteration_check
			if bad_complete != 0:
				comp_bad[bad_complete] = iteration_check

	iteration_list = [list(driver.values())[0]['Iterations'] for driver in network.nodes[end_node]["Queue"]]
	final_good = pd.DataFrame.from_dict(comp_good, orient='index')
	final_bad = pd.DataFrame.from_dict(comp_bad, orient='index')
	if final_good.empty:
		final_good = pd.DataFrame([0], columns=['Iterations'])
	if final_bad.empty:
		final_bad = pd.DataFrame([0], columns=['Iterations'])
	return iteration_list, final_good, final_bad

def run_and_plot(num_drivers: int, scale: int, bad_prop: list, iteration_list: list, good_df: pd.DataFrame, bad_df: pd.DataFrame):
	prop_bad = scale * 0.1
	driver_list = generate_drivers(num_drivers, prop_bad, states = ["good","bad"])
	net = gen_net(edges=gen_data(), node_vals=["u", "v", "length"])
	total, good, bad = run_model(drivers=driver_list,
															network=net,
															origin_node=204449959,
															end_node=204350837,
															prob_wrong_turn=0.01)
	bad_prop.append(prop_bad)
	iteration_list.append(total)
	good_df = pd.concat((good_df, good))
	bad_df = pd.concat((bad_df, bad))
	print(f'Iterations: {total[-1]}')
	print(f'Proportion Bad: {prop_bad}')
	print(f'Mean Iter. Good: {good.mean(0)[0]}')
	plt.plot(good,
					 label='{:2f}% Bad'.format(prop_bad*100),
					 alpha=0.2,
					 color='blue')
	plt.xlabel('Count of Good Drivers')
	plt.ylabel('Time-steps to Complete Shortest Path')
	plt.title(f'Average Good Driver Commute Time with {int(num_drivers * prop_bad)} Bad Drivers')

	plt.savefig(f'{num_drivers}_10eneg2.png')
	return plt.gca(), bad_prop, iteration_list, good_df, bad_df


# Initialize lists and dataframes
bad_prop = []
iteration_list = []
good_df = pd.DataFrame()
bad_df = pd.DataFrame()
# Set parameters
num_drivers = 1000
sig_digits = 10
# Initialize plot
fig, ax = plt.subplots(1,1, figsize = (5.5, 5.5))
# Iterate through different proportions of bad drivers, and update plot
for i in range(sig_digits):
	ax, bad_prop, iteration_list, good_df, bad_df = run_and_plot(num_drivers, i, bad_prop, iteration_list, good_df, bad_df)
plt.show()