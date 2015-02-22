"""Write seed node choices for a given graph file

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""
from json import load
from networkx import DiGraph
from operator import itemgetter
from re import split


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
    sorted_degree_nodes = [node for node, _ in sorted(graph.degree_iter(), key=itemgetter(1), reverse=True)]
    highest_degree_nodes = sorted_degree_nodes[:num_seeds] * NUM_ROUNDS
    return tuple(highest_degree_nodes)


def read_graph(graph_path):
    """Read graph at given path and return graph with metadata

    :param str graph_path: path to graph file
    :return: NetworkX Graph, number of players, and number of seeds
    :rtype: tuple
    """
    with open(graph_path) as graph_file:
        graph_data = load(graph_file)
    graph = DiGraph(graph_data)
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
