"""Simulate multiple algorithms competing on a graph

Written by Jan Van Bruggen <jancvanbruggen@gmail.com>
Last edited on February 25, 2015
"""
from __future__ import print_function
from csv import reader
from json import load
from os.path import isfile

import seed
import sim


NUM_ROUNDS = seed.NUM_ROUNDS


def read_config(config_path):
    with open(config_path) as config_file:
        config_reader = reader(config_file)
        next(config_reader)  # Skip header
        all_weights = []
        for row in config_reader:
            all_weights.append([int(x) for x in row])
    return all_weights


def read_graph(graph_path):
    with open(graph_path) as graph_file:
        return load(graph_file)


def read_seeds(seed_path):
    flat_seeds = []
    with open(seed_path) as seed_file:
        seed_reader = reader(seed_file)
        for row in seed_reader:
            flat_seeds.append(row[0])
    step = int(len(flat_seeds) / NUM_ROUNDS)
    nested_seeds = [flat_seeds[i:i + step] for i in range(0, NUM_ROUNDS * step, step)]
    return nested_seeds


def write_seeds(graph_path, weights, weights_string):
    new_graph_path = graph_path.replace('graphs/', 'simseeds/weights{}-'.format(weights_string))
    seed_path = new_graph_path.replace('.json', '.seeds.txt')
    if not isfile(seed_path):
        seed.write_seeds(new_graph_path, seed.run(graph_path, weights))
    return seed_path


def run(graph_path, weights_path):
    all_weights = read_config(weights_path)
    all_weights_strings = [','.join(str(w) for w in weights) for weights in all_weights]
    seed_paths = []
    for i, weights in enumerate(all_weights):
        weights_string = all_weights_strings[i]
        print('calculating seeds for weights={}'.format(weights_string))
        seed_paths.append(write_seeds(graph_path, weights, weights_string))
    graph = read_graph(graph_path)
    all_seeds = []
    for i in range(len(all_weights)):
        all_seeds.append(read_seeds(seed_paths[i]))
    nodes = {all_weights_strings[i]: all_seeds[i] for i in range(len(all_weights))}
    print('running sim')
    results = sim.run(graph, nodes, NUM_ROUNDS)
    rank_strategies = lambda score_dict: sorted(score_dict.keys(), key=lambda x: score_dict[x], reverse=True)
    for round_number, result in enumerate(results):
        print('-' * 160)
        print('Graph {}'.format(graph_path))
        print('Round {}'.format(round_number))
        scores, seeds = result
        for strategy in rank_strategies(scores):
            print('{} won {} nodes with these seeds: {}'.format(strategy, scores[strategy], seeds[strategy]))
    print('-' * 160)
    all_scores = [result[0] for result in results]
    avg_scores = {strategy: float(sum(scores[strategy] for scores in all_scores)) / len(all_scores)
                  for strategy in all_scores[0]}
    for strategy in rank_strategies(avg_scores):
        print('{} averaged {} nodes'.format(strategy, avg_scores[strategy]))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('graph_path', metavar='G', help='path to graph file')
    args = parser.parse_args()
    run(args.graph_path, 'sim_run.weights')
