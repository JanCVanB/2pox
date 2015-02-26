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


if __name__ == '__main__':
    test_correct_number_of_seeds()
