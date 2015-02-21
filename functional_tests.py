"""Functional tests for seed-choosing script

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""
import json
from operator import itemgetter
import networkx as nx
import seed


def test_correct_number_of_seeds():
    seeds = seed.run('graphs/2.5.01.json')
    assert len(seeds) == 250
    seeds = seed.run('graphs/8.35.01.json')
    assert len(seeds) == 1750


def test_one_player_seeds_are_highest_degree():
    graph_path = 'graphs/1.5.01from2501.json'
    with open(graph_path) as graph_file:
        graph = nx.Graph(json.load(graph_file))
    sorted_degree_nodes = [node for node, _ in sorted(graph.degree_iter(), key=itemgetter(1), reverse=True)]
    highest_degree_nodes = sorted_degree_nodes[:5] * seed.NUM_ROUNDS
    seeds = seed.run(graph_path)
    assert seeds == tuple(highest_degree_nodes)


if __name__ == '__main__':
    test_correct_number_of_seeds()
    test_one_player_seeds_are_highest_degree()
