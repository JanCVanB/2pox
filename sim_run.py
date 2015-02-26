"""Simulate multiple algorithms competing on a graph

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""
from csv import reader
from json import load
from pprint import pprint

import seed
import sim


NUM_ROUNDS = seed.NUM_ROUNDS


def read_config(config_path):
    with open(config_path) as config_file:
        config_reader = reader(config_file)
        run_number = next(config_reader)[1]
        graph_path = next(config_reader)[1]
        next(config_reader)  # Skip weights header
        all_weights = []
        for row in config_reader:
            all_weights.append([float(x) for x in row])
    return run_number, graph_path, all_weights


def read_graph(graph_path):
    with open(graph_path) as graph_file:
        return load(graph_file)


def read_seeds(seed_path, weights):
    flat_seeds = []
    with open(seed_path) as seed_file:
        seed_reader = reader(seed_file)
        for row in seed_reader:
            flat_seeds.append(row[0])
    step = len(flat_seeds) / NUM_ROUNDS
    nested_seeds = [flat_seeds[i:i + step] for i in range(0, NUM_ROUNDS * step, step)]
    return nested_seeds


def write_seeds(run_number, graph_path, weights):
    new_graph_path = graph_path.replace('graphs/', 'simseeds/run{}-'.format(run_number))
    seed.write_seeds(new_graph_path, seed.run(graph_path, weights))
    return new_graph_path.replace('.json', '.seeds.txt')


def run(config_path):
    run_number, graph_path, all_weights = read_config(config_path)
    seed_paths = []
    for weights in all_weights:
        seed_paths.append(write_seeds(run_number, graph_path, weights))
    graph = read_graph(graph_path)
    all_seeds = []
    for i in range(len(all_weights)):
        all_seeds.append(read_seeds(seed_paths[i], all_weights[i]))
    all_weights_strings = [','.join(str(w) for w in weights) for weights in all_weights]
    nodes = {all_weights_strings[i]: all_seeds[i] for i in range(len(all_weights))}
    results = sim.run(graph, nodes, NUM_ROUNDS)
    for round_number, result in enumerate(results):
        print '-' * 160
        print 'Graph {}'.format(graph_path)
        print 'Round {}'.format(round_number)
        pprint(result)


if __name__ == '__main__':
    run('sim_run.config')
