"""Functional tests for seed-choosing script

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""
from json import load
from operator import itemgetter
import networkx as nx

from seed import NUM_ROUNDS
from seed import run


def test_correct_number_of_seeds():
    seeds = run('graphs/2.5.01.json')
    assert len(seeds) == 250
    seeds = run('graphs/8.35.01.json')
    assert len(seeds) == 1750


def test_one_player_seeds_are_highest_degree():
    graph_path = 'graphs/1.5.01from2501.json'
    with open(graph_path) as graph_file:
        graph = nx.DiGraph(load(graph_file))
    sorted_degree_nodes = [node for node, _ in sorted(graph.out_degree_iter(), key=itemgetter(1), reverse=True)]
    highest_degree_nodes = sorted_degree_nodes[:5] * NUM_ROUNDS
    seeds = run(graph_path)
    assert seeds == tuple(highest_degree_nodes)


if __name__ == '__main__':
    test_correct_number_of_seeds()
    test_one_player_seeds_are_highest_degree()
