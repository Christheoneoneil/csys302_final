import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from complex_model import generate_drivers
from complex_model import run_model
from gen_complex_net import gen_net
from gen_complex_net import gen_data


def gen_means(bad_p: list, wrong_p: list, num_iters: int) -> list:
    """
    Params:
    bad_p = proportion of bad drivers
    wrong_p = probability of taking a wrong turn
    num_iters = number of runs

    Retruns:
    list of mean values calculated for each proportion
    """
    mean_list = []
    for bad, wrong in zip(bad_p, wrong_p):
        outcomes = []
        for i in range(num_iters):
                driver_list = generate_drivers(num_drivers=100, bad_driver_prop=bad, states=["good", "bad"])
                net = gen_net(data=gen_data(), node_vals=["u", "v", "length"])
                mod = run_model(drivers=driver_list, network=net, origin_node=204449959, 
                        end_node=204350837, prob_wrong_turn=wrong)
                outcomes.append(mod)
        print(bad, wrong, np.mean(outcomes))
        mean_list.append(np.mean(outcomes))
    print(mean_list)
    return mean_list


def gen_plot(bad_p: list, wrong_p: list, means_list: list) -> None: 
    """
    Params:
    bad_p = proportion of bad drivers
    wrong_p = probability of taking a wrong turn
    means_list = list of means

    Retruns:
    list of mean values calculated for each proportion
    """

    plt.scatter(bad_p, wrong_p, c=means_list, cmap='viridis')
    sns.despine()
    plt.title("Relationship of Probablities and Number of Iterations")
    plt.xlabel("Proportion of Bad Drivers")
    plt.ylabel("Probability of Taking Taking Bad Turn")
    plt.colorbar().set_label("Avg Iterations", rotation=270)
    plt.savefig("runs_colormap")

bad_props = np.arange(0, 1.1, 0.5)
wrong_turns_props = np.arange(0, 1.1, 0.5)

means = gen_means(bad_p=[0.5, 0.5, 0.5], wrong_p=[0.3, 0.5, 0.7], num_iters=3) 
gen_plot(bad_p=bad_props, wrong_p=wrong_turns_props, means_list=means)
