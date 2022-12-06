import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from complex_model import generate_drivers
from complex_model import run_model
from gen_complex_net import gen_net
from gen_complex_net import gen_data



def gen_means(bad_p, wrong_p, num_iters) -> list:

    for bad, wrong in zip(bad_p, wrong_p):
        outcomes = []
        mean_list = []
        for i in range(num_iters):
                driver_list = generate_drivers(num_drivers=100, bad_driver_prop=bad, states=["good", "bad"])
                net = gen_net(data=gen_data(), node_vals=["u", "v", "length"])
                mod = run_model(drivers=driver_list, network=net, origin_node=204449959, 
                        end_node=204350837, prob_wrong_turn=wrong)
                outcomes.append(mod)
                print(bad, wrong, np.mean(outcomes))
        mean_list.append(np.mean(outcomes))
    return(means)


def gen_plot(bad_p, wrong_p, means_list) -> None: 

    plt.scatter(bad_p, wrong_p, c=mean_list, cmap='viridis')
    sns.despine()
    plt.title("Relationship of Probablities and Number of Iterations")
    plt.xlabel("Proportion of Bad Drivers")
    plt.ylabel("Probability of Taking Taking Bad Turn")
    cbar = plt.colorbar()
    cbar.set_label("Avg Iterations", rotation=270)
    plt.savefig("runs_colormap")

bad_props = np.arange(0, 1.1, 0.1)
wrong_turns_props = np.arange(0, 1.1, 0.1)
means = gen_means(bad_p=bad_props, wrong_p=wrong_turns_props, num_iters=1) 
gen_plot(means, bad_p=bad_props, wrong_p=wrong_turns_props, means_list=means)
