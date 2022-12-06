import random 
import copy
import networkx as nx
import numpy as np

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

        drivers = [{key: random.choices(states, 
                [1-bad_driver_prop, bad_driver_prop])[0]} for key in np.arange(1,num_drivers+1, 1)]
        return drivers


def run_model(drivers: list, network: nx.Graph(), origin_node: int, end_node: int, prob_wrong_turn: float) -> int:
        """
        run_model runs a model with the given generated drivers

        Params:
        drivers: array of drivers of given attributes
        network: networkx graph object
        origin_node: node point of origin 
        end_node: node point of sink
        prob_wrong_turn: probablity that bad driver makes a random turn
        at a given node

        Returns:
        number of iterations required for all drivers to get to final
        destination
        """


        network.nodes[origin_node]["Queue"] += drivers
        good_driver_path = nx.shortest_path(network, source=origin_node, target=end_node, method='dijkstra', weight="length")
        init_drivers = [list(driver.keys())[0] for driver in network.nodes[origin_node]["Queue"]]
        end_drivers = []
        active_nodes = {origin_node}
        iterations = 0

        while len(end_drivers) == 0 or sorted(init_drivers) != sorted(end_drivers):
                iterations+=1
                # Keep this as copy or for loop behavior changes
                for node in copy.copy(active_nodes):
                        if node != end_node:
                                try:        
                                        drivers = network.nodes[node]["Queue"]
                                        
                                        first_out = drivers.pop(0)
                                        state = list(first_out.values())[0]
                                        if state == "good":
                                                current_node_ind = good_driver_path.index(node)
                                                next_step = good_driver_path[current_node_ind + 1]
                                                network.nodes[next_step]["Queue"].append(first_out)
                                                active_nodes.add(next_step)
                                        else:
                                                # at each step cause a bad driver to make a wrong turn with given prob.
                                                turn_choice = random.choices(["on_path", "off_path"], 
                                                                             [1-prob_wrong_turn, prob_wrong_turn])[0]
                                                if turn_choice == "off_path":
                                                        next_step = random.choice([n for n in network.neighbors(node)])
                                                else: 
                                                        bad_driver_path = nx.shortest_path(network, source=node, target=end_node, method='dijkstra', weight="length")
                                                        current_node_ind = bad_driver_path.index(node)
                                                        next_step = bad_driver_path[current_node_ind+1]
                                                network.nodes[next_step]["Queue"].append(first_out)
                                                active_nodes.add(next_step)
                                except IndexError:
                                        # Once all drivers are dequed remove node from active
                                        # nodes list
                                        active_nodes.remove(node)
                                  
                end_drivers = [list(driver.keys())[0] for driver in network.nodes[end_node]["Queue"]]

        return iterations


## TODO: Implement version of model that spawns drivers at random nodes throughoutt the graph
# Have more interactions between drivers other then being stuck in a queue at each intersection##

# origin and end node were found by our jupyiter notebook
