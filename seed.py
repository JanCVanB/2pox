"""Write seed node choices for a given graph file

Written by Jan Van Bruggen <jancvanbruggen@gmail.com> and Sean Dolan <stdolan@gmail.com>
Last edited on March 1, 2015
"""
from __future__ import print_function
from json import load
import networkx as nx
from operator import itemgetter
from re import split
from random import random


NUM_ROUNDS = 50


def probabilistic_grab(possible_seeds, scores, num_seeds, closeness_centralities, degree_centralities):
    """Return a list of nodes to seed, given their scores and centralities

    :param list possible_seeds: all nodes to consider seeding
    :param dict scores: score for each node, from which to determine selection probabilities
    :param int num_seeds: number of nodes to seed
    :param dict closeness_centralities: closeness centrality for each node
    :param dict degree_centralities: degree centralities for each node
    :return: nodes to seed
    :rtype: list
    """
    chosen_seeds = []
    total_score = 0
    for seed in possible_seeds:
        total_score += scores[seed]
    closeness_values = closeness_centralities.values()
    degree_values = degree_centralities.values()
    for round_number in range(NUM_ROUNDS):
        print('round number', round_number)
        round_seeds = []
        i = 0
        while len(round_seeds) != num_seeds:
            seed = possible_seeds[i % len(possible_seeds)]
            i += 1
            higher_closeness_counts = [value > closeness_centralities[seed] for value in closeness_values]
            higher_degree_counts = [value > degree_centralities[seed] for value in degree_values]
            if sum(higher_closeness_counts) / float(len(higher_closeness_counts)) < 0.01:
                continue
            if sum(higher_degree_counts) / float(len(higher_degree_counts)) < 0.01:
                continue
            if scores[seed] > random() and seed not in round_seeds:
                round_seeds.append(seed)
        chosen_seeds += round_seeds
    return chosen_seeds


def choose_seeds(graph, num_seeds, weights=None):
    """Return one flat tuple of the seed nodes for each round

    If num_seeds is 2 and NUM_ROUNDS is 2, the seed list will look like this:

    ['Seed1ForRound1', 'Seed2ForRound1', 'Seed1ForRound2', 'Seed2ForRound2']

    :param graph: NetworkX Graph
    :param int num_seeds: number of seeds to choose each round
    :param list weights: weights for each centrality when scoring nodes, ultimately unused
    :return: names of seed nodes
    :rtype: tuple
    """
    scores = {}
    closeness_centralities = nx.closeness_centrality(graph)
    # In case of graphs with more than 5000 nodes, use betweenness centrality instead (to run in under 5 minutes)
    # closeness_centralities = nx.betweenness_centrality(graph, k=500)
    degree_centralities = nx.degree_centrality(graph)
    for node in graph.nodes_iter():
        scores[node] = (closeness_centralities[node] + degree_centralities[node]) / 2.0
    sorted_centrality_nodes = [node for node, _ in sorted(scores.items(),
                                                          key=itemgetter(1),
                                                          reverse=True)]
    centralest_nodes = sorted_centrality_nodes[:int(len(graph) / 10)]
    return tuple(probabilistic_grab(centralest_nodes, scores, num_seeds, closeness_centralities, degree_centralities))


def read_graph(graph_path):
    """Read graph at given path and return graph with metadata

    :param str graph_path: path to graph file
    :return: NetworkX Graph, number of players, and number of seeds
    :rtype: tuple
    """
    with open(graph_path) as graph_file:
        graph_data = load(graph_file)
    graph = nx.Graph(graph_data)
    graph_metadata = split('\.', graph_path)  # Assumes no periods in path before graph file name
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
