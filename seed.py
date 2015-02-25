"""Write seed node choices for a given graph file

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""
from json import load
import networkx as nx
from operator import itemgetter
from re import split
from math import factorial
from random import sample


NUM_ROUNDS = 50


def choose_seeds(graph, num_players, num_seeds):
    """Return one flat tuple of the seed nodes for each round

    If num_seeds is 2 and NUM_ROUNDS is 2, the seed list will look like this:

    ['Seed1ForRound1', 'Seed2ForRound1', 'Seed1ForRound2', 'Seed2ForRound2']

    :param graph: NetworkX Graph
    :param int num_players: number of players competing on the graph
    :param int num_seeds: number of seeds to choose each round
    :return: names of seed nodes
    :rtype: tuple
    """
    nodes = graph.nodes()
    scored_nodes = {node: [] for node in nodes}
    centrality_nodes = nx.degree_centrality(graph)
    closeness_nodes = nx.closeness_centrality(graph)
    betweenness_nodes = nx.betweenness_centrality(graph)

    for node, centrality in centrality_nodes.iteritems():
        scored_nodes[node].append(centrality)

    for node, centrality in closeness_nodes.iteritems():
        scored_nodes[node].append(centrality)

    for node, centrality in betweenness_nodes.iteritems():
        scored_nodes[node].append(centrality)
    '''num_nodes = len(nodes)
    samples = None
    if num_nodes <= 100:
        samples = nodes
    else:
        sample_indicies = sample(xrange(num_nodes), 100)
        samples = map(str, sample_indicies)

    scored_nodes = {node: [] for node in nodes if graph.degree(node)}

    # Get the importance in degree, closeness, and betweenness centrality.
    closeness_paths = {}
    betweenness_paths = {}
    for i in scored_nodes:
        int_i = int(i)
        sum_of_distances = 0
        sum_of_ratios = 0

        # Degree centrality calculation.
        num_neighors = len(list(nx.all_neighbors(graph, i)))

        scored_nodes[i].append(float(num_neighors)
                               / float(num_nodes - 1))

        for j in samples:
            if j == i:
                continue

            int_j = int(j)

            # Closeness centrality calculations.
            try:
                key = str(tuple(sorted([int_i, int_j])))
                if key not in closeness_paths:
                    path_length = len(
                        nx.shortest_path(graph, source=i, target=j)) - 1

                    closeness_paths[key] = path_length

                sum_of_distances += closeness_paths[key]

            except nx.NetworkXNoPath:
                pass

            for k in samples:
                if k == i or k == j:
                    continue

                # Betweenness centrality calculations.
                try:
                    key = str(tuple(sorted([int_j, int(k)])))
                    if key not in betweenness_paths:
                        betweenness_paths[key] = list(nx.all_shortest_paths(graph, j, k))

                    paths_with_i = 0
                    for path in betweenness_paths[key]:
                        if i in path:
                            paths_with_i += 1

                    sum_of_ratios += float(paths_with_i) / float(len(betweenness_paths[key]))

                except nx.NetworkXNoPath:
                    pass

        if sum_of_distances:
            scored_nodes[i].append(float(num_nodes - 1) / float(sum_of_distances))
        else:
            scored_nodes[i].append(float(0))

        scored_nodes[i].append(sum_of_ratios / (factorial(num_nodes - 1) / (factorial(2) * factorial (num_nodes - 3))))'''

    for node, centralities in scored_nodes.iteritems():
        scored_nodes[node] = sum(centralities) / float(len(centralities))

    sorted_centrality_nodes = [node for node, _ in sorted(scored_nodes.items(),
                                                          key=itemgetter(1),
                                                          reverse=True)]

    centralest_nodes = sorted_centrality_nodes[:num_seeds] * NUM_ROUNDS
    return tuple(centralest_nodes)


def read_graph(graph_path):
    """Read graph at given path and return graph with metadata

    :param str graph_path: path to graph file
    :return: NetworkX Graph, number of players, and number of seeds
    :rtype: tuple
    """
    with open(graph_path) as graph_file:
        graph_data = load(graph_file)
    graph = nx.Graph(graph_data)
    graph_metadata = split('/|\.', graph_path)
    num_players = int(graph_metadata[1])
    num_seeds = int(graph_metadata[2])
    return graph, num_players, num_seeds


def write_seeds(graph_path, seeds):
    """Write the output file of seed node names

    :param str graph_path: path to graph file
    :param tuple seeds: names of seed nodes
    """
    seeds_path = graph_path.replace('graphs', 'seeds').replace('json', 'seeds.txt')
    with open(seeds_path, 'w') as seeds_file:
        seeds_file.writelines(seed + '\n' for seed in seeds)


def run(graph_path):
    """Read the graph at the given path and return the names of the seed nodes

    :param graph_path: path to graph file
    :return: names of seed nodes
    :rtype: tuple
    """
    graph, num_players, num_seeds = read_graph(graph_path)
    seeds = choose_seeds(graph, num_players, num_seeds)
    return seeds


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('graph_path', metavar='G', help='path to graph file')
    args = parser.parse_args()
    write_seeds(args.graph_path, run(args.graph_path))
