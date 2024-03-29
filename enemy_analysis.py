"""Graph seed characteristics from a competition submission

Written by Jan Van Bruggen <jancvanbruggen@gmail.com>
Last edited on February 27, 2015
"""
from json import load
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx

import seed


def make_histogram(bins, rank_list, teams, title):
    plt.figure()
    plt.title(title)
    plt.xlabel('Node Rank by {}'.format(title.split()[-1]))
    plt.ylabel('Number of Seeds in Each {}-Node Bin'.format(bins[1]))
    plt.hist([rank_list[team] for team in teams],
             bins, histtype='bar', label=teams, edgecolor="none",
             color=[cm.jet((i + 0.5) / len(teams), 1) for i in range(len(teams))])
    plt.legend(loc='best')
    plt.savefig('submissions/{}.png'.format('_'.join(title.split())), frameon=False)


def run(results_path):
    with open(results_path) as results_file:
        results = load(results_file)
    graph, _ = seed.read_graph(results_path.replace('submissions', 'graphs').replace('-2pox', ''))
    num_nodes = graph.number_of_nodes()
    betweenness_centralities = nx.betweenness_centrality(graph)
    closeness_centralities = nx.closeness_centrality(graph)
    degree_centralities = nx.degree_centrality(graph)
    rank_dict_values = lambda d: sorted(d.keys(), key=lambda x: d[x], reverse=True)
    most_between = rank_dict_values(betweenness_centralities)
    most_close = rank_dict_values(closeness_centralities)
    most_degree = rank_dict_values(degree_centralities)
    rank_by_most = lambda most_list, seed_list: [most_list.index(x) for x in seed_list]
    rank_between = {}
    rank_close = {}
    rank_degree = {}
    for team, all_seeds in results.iteritems():
        rank_between[team] = []
        rank_close[team] = []
        rank_degree[team] = []
        for seeds in all_seeds:
            try:
                rank_between[team].extend(rank_by_most(most_between, seeds))
                rank_close[team].extend(rank_by_most(most_close, seeds))
                rank_degree[team].extend(rank_by_most(most_degree, seeds))
            except ValueError:
                pass
    bins = range(0, num_nodes + 1, int(num_nodes / 20))
    teams = sorted(results.keys())
    graph_id_string = results_path[12:results_path.index('-')]
    title_prefix = 'Graph {} Seed Choices by '.format(graph_id_string)
    make_histogram(bins, rank_between, teams, title_prefix + 'Betweenness Centrality')
    make_histogram(bins, rank_close, teams, title_prefix + 'Closeness Centrality')
    make_histogram(bins, rank_degree, teams, title_prefix + 'Degree Centrality')
    bins = range(0, int(num_nodes / 5 + 1), int(num_nodes / 100))
    make_histogram(bins, rank_between, teams, title_prefix + 'Zoomed Betweenness Centrality')
    make_histogram(bins, rank_close, teams, title_prefix + 'Zoomed Closeness Centrality')
    make_histogram(bins, rank_degree, teams, title_prefix + 'Zoomed Degree Centrality')
    plt.show()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('results_path', metavar='R', help='path to results file')
    args = parser.parse_args()
    run(args.results_path)
