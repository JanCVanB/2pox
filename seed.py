"""Write seed node choices for a given graph file

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""
from json import load
import networkx as nx
from operator import itemgetter
from re import split
from random import random


NUM_ROUNDS = 50


def probabilistic_grab(possible_seeds, scores, num_seeds):
    chosen_seeds = []
    total_score = 0
    for seed in possible_seeds:
        total_score += scores[seed]

    for _ in xrange(NUM_ROUNDS):
        round_seeds = []
        for seed in possible_seeds:
            if len(round_seeds) >= num_seeds:
                break
            if scores[seed] > random():
                round_seeds.append(seed)

        i = 0
        while len(round_seeds) != num_seeds:
            if possible_seeds[i] not in round_seeds:
                round_seeds.append(possible_seeds[i])
            i += 1

        chosen_seeds += round_seeds

    return chosen_seeds



def choose_seeds(graph, num_seeds, weights=None):
    """Return one flat tuple of the seed nodes for each round

    If num_seeds is 2 and NUM_ROUNDS is 2, the seed list will look like this:

    ['Seed1ForRound1', 'Seed2ForRound1', 'Seed1ForRound2', 'Seed2ForRound2']

    :param graph: NetworkX Graph
    :param int num_seeds: number of seeds to choose each round
    :return: names of seed nodes
    :rtype: tuple
    """
    scores = {}
    betweenness_centralities = nx.betweenness_centrality(graph, k=100)
    closeness_centralities = nx.closeness_centrality(graph)
    degree_centralities = nx.degree_centrality(graph)

    if weights is None:
        weights = [1] * 3
    for node in graph.nodes_iter():
        scores[node] = (weights[0] * betweenness_centralities[node] +
                        weights[1] * closeness_centralities[node] +
                        weights[2] * degree_centralities[node]) / 3.0

    sorted_centrality_nodes = [node for node, _ in sorted(scores.items(),
                                                          key=itemgetter(1),
                                                          reverse=True)]
    centralest_nodes = sorted_centrality_nodes[:len(graph) / 10]

    return tuple(probabilistic_grab(centralest_nodes, scores, num_seeds))


def read_graph(graph_path):
    """Read graph at given path and return graph with metadata

    :param str graph_path: path to graph file
    :return: NetworkX Graph, number of players, and number of seeds
    :rtype: tuple
    """
    with open(graph_path) as graph_file:
        graph_data = load(graph_file)
    graph = nx.Graph(graph_data)
    graph_metadata = split('\.', graph_path)
    num_seeds = int(graph_metadata[1])
    return graph, num_seeds


def write_seeds(graph_path, seeds):
    """Write the output file of seed node names

    :param str graph_path: path to graph file
    :param tuple seeds: names of seed nodes
    """
    seeds_path = graph_path.replace('graphs', 'seeds').replace('json', 'seeds.txt')
    with open(seeds_path, 'w') as seeds_file:
        seeds_file.writelines(seed + '\n' for seed in seeds)


def run(graph_path, weights=None):
    """Read the graph at the given path and return the names of the seed nodes

    :param graph_path: path to graph file
    :return: names of seed nodes
    :rtype: tuple
    """
    graph, num_seeds = read_graph(graph_path)
    seeds = choose_seeds(graph, num_seeds, weights)
    return seeds


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('graph_path', metavar='G', help='path to graph file')
    args = parser.parse_args()
    write_seeds(args.graph_path, run(args.graph_path))
