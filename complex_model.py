import random 
import copy
import networkx as nx
import numpy as np
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

        drivers = [{key: random.choices(states, 
                [1-bad_driver_prop, bad_driver_prop])[0]} for key in np.arange(1,num_drivers+1, 1)]
        return drivers


def run_model(drivers: list, network: nx.Graph(), origin_node: int, end_node: int) -> float:
        """
        run_model runs a model with the given generated drivers

        Params:
        drivers: array of drivers of given attributes
        network: networkx graph object
        origin_node: node point of origin 
        end_node: node point of sink

        Returns:
        number of iterations required for all drivers to get to final
        destination
        """


        network.nodes[origin_node]["Queue"] +=  drivers
        good_driver_path = nx.shortest_path(network, source=origin_node, target=end_node, method='dijkstra', weight="length")
        init_drivers = [list(driver.keys())[0] for driver in network.nodes[origin_node]["Queue"]]
        end_drivers = []
        active_nodes = {origin_node}
        iterations = 0

        """
        The reason that this while loop is set up like this is there is a lot of
        mutation going on within this while loop, so to not cause issues with memory
        a flag was not created to just stop popping off end_drivers node, so once the last
        driver is in the end_drivers queue the loop ends and we return a count
        """
        while len(end_drivers) == 0 or sorted(init_drivers)[-1] != sorted(end_drivers)[-1]:
                iterations += 1
                # Keep this as deepcopy or for loop behavior changes
                for node in copy.deepcopy(active_nodes):
                        if node != end_node:
                                try:        
                                        drivers = network.nodes[node]["Queue"]
                                        
                                        first_out = drivers.pop(0)
                                        state = list(first_out.values())[0]
                                        if state == "good":
                                                current_node_ind = good_driver_path.index(node)
                                                next_step = good_driver_path[current_node_ind + 1]
                                                network.nodes[next_step]["Queue"].append(first_out)
                                        else:
                                                pass
                                except IndexError:
                                        # Once all drivers are dequed remove node from active
                                        # nodes list
                                        active_nodes.remove(node)
                end_drivers = [list(driver.keys())[0] for driver in network.nodes[end_node]["Queue"]]
                active_nodes.add(next_step)
        
        return iterations


driver_list = generate_drivers(1000, 0, ["good", "bad"])
net = gen_net(data=gen_data(), node_vals=["u", "v", "length"])
# origin and end node were found by our jupyiter notebook
print(run_model(drivers=driver_list, network=net, origin_node=204449959, end_node=204350837))
