import networkx as nx
from gen_complex_net import gen_net
from gen_complex_net import gen_data
import random 
import numpy as np


def generate_drivers(num_drivers: int, bad_driver_prop: float, states: list) -> list:
        
        """
        generate drivers generates an array of randomly chosen good and bad drivers

        Params: 
        num_drivers: total number of drivers
        bad_driver_prop: proportion of bad drivers on the network

        Returns:
        list of drivers and their state

        """

        drivers = {key: random.choices(states, [1-bad_driver_prop, bad_driver_prop]) for key in np.arange(1,num_drivers+1, 1)}
        return drivers

def run_model(drivers: list, netowrk: nx.Graph()) -> float:
        """
        run_model runs a model with the given generated drivers

        Params:
        drivers: array of drivers of given attributes

        Returns:
        number of iterations required for all drivers to get to final
        destination
        """


        


generate_drivers(1000, .5, ["good", "bad"])
net = gen_net(gen_data(), ["u", "v", "speed_kph"])