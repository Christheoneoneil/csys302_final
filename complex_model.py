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
import mapclassify
from gen_complex_net import gen_net


def gen_visuals(streets) -> None:
    """
    gen_visuals generates visual of subsetted network

    Params:
    streets: data frame containing network data

    Returns:
    None
    """
    
    # Primal models: Intersections as nodes, roads as edges
    primal = momepy.gdf_to_nx(streets, approach='primal')
    primal = momepy.closeness_centrality(primal, radius=400, name='closeness400', distance='mm_len', weight='mm_len')
    primal = momepy.closeness_centrality(primal, name='closeness_global', weight='mm_len')
    primal = momepy.betweenness_centrality(primal, name='betweenness_metric_n', mode='nodes', weight='mm_len')
    primal = momepy.betweenness_centrality(primal, name='betweenness_metric_e', mode='edges', weight='mm_len')
    primal = momepy.straightness_centrality(primal)

    momepy.mean_nodes(primal, 'straightness')
    momepy.mean_nodes(primal, 'closeness400')
    momepy.mean_nodes(primal, 'closeness_global')
    momepy.mean_nodes(primal, 'betweenness_metric_n')

    primal_gdf = momepy.nx_to_gdf(primal, points=False)

    fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(45, 15))

    primal_gdf.plot(ax=ax1, column='straightness', cmap='magma_r', scheme='quantiles', k=15, alpha=0.6)
    ax1.set_axis_off()
    ax1.set_title('straightness')

    primal_gdf.plot(ax=ax2, column='closeness400', cmap='magma_r', scheme='quantiles', k=15, alpha=0.6)
    ax2.set_axis_off()
    ax2.set_title('closeness400')

    primal_gdf.plot(ax=ax3, column='betweenness_metric_n', cmap='magma_r', scheme='quantiles', k=15, alpha=0.6)
    ax3.set_axis_off()
    ax3.set_title('betweenness angular')

    plt.savefig("betweenness")


    fig, ax = plt.subplots(1,1, figsize=(8.5, 8.5), dpi=2000)

    primal_gdf.plot(ax=ax,
            column='straightness',
            cmap='Reds',
            scheme='quantiles',
            k=15,
            alpha=0.33,
            zorder=3)

    primal_gdf.plot(ax=ax,
            column='closeness400',
            cmap='Greens',
            scheme='quantiles',
            k=15,
            alpha=0.33,
            zorder=2)

    primal_gdf.plot(ax=ax,
            column='betweenness_metric_n',
            cmap='Blues',
            scheme='quantiles',
            k=15,
            alpha=0.33,
            zorder=1)

    ax.set_axis_off()
    ax.set_title('   Intersection based averages of Straightness (Red), Closeness (Green), and Betweeness (Blue)   \nProjected onto Roadways within 10 km. of Burlington, VT')

    plt.savefig('straightness_closeness_betweeness_btv_10KM_nodebasedmean.png')


    # Dual models: flipped nodes and edges
    dual = momepy.gdf_to_nx(streets, approach='dual')
    dual = momepy.betweenness_centrality(dual, name='angbetweenness', mode='nodes', weight='angle')

    dual_gdf = momepy.nx_to_gdf(dual, points=False)

    edges_d = momepy.nx_to_gdf(dual)

    fig, ax = plt.subplots(1,1, figsize=(12,12),
                    dpi=2000)

    dual_gdf.plot(ax=ax,
            column='angbetweenness',
            cmap= 'magma_r',
            scheme='quantiles',
            k=15,
            alpha=0.33,
            zorder=1)
    ax.set_axis_off()
    plt.savefig('angbetween.png',
        facecolor='white',
        transparent=False)

net = gen_net()
gen_visuals(net)
