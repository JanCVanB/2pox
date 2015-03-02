# 2Pox

Cascade-seeding algorithm for graph dominance competitions (Caltech CS 144, Winter 2015)

## "Pandemaniac" Competition Guidelines

In groups of 2 or 3, create an algorithm that will take as input an undirected graph (in adjacencylist form) and output a list of N seed nodes where your epidemic will start (where N is given).
You will be competing against other teams who are also trying to spread their epidemics on the same graph.
Your team's goal is to take over more of the network (i.e., a larger number of nodes) with your epidemic than your competitors do with theirs.

See pandemaniac.pdf for more competition rules and information.

## Our Algorithm

First we calculate the closeness and degree centralities for each node.
A high degree centrality allows us to convert a large number of nodes quickly,
while a high closeness centrality allows our influence to expand to other areas rapidly.
Combined, these rankings identify seeds that will allow us to convert uncolored nodes in many areas of the graph.
We weight these two centrality measures equally,
because our simulation testing was inconclusive regarding which measure contributed more to a strategy’s success.
Considering the following aspects of our algorithm,
we see no convincing reason to prefer one measure over the other.

We then remove the bottom 90% of nodes with regard to the sum of the two measures of centrality,
or the “score” of a node. We then draw our seeds from a probability distribution over this top 10% of nodes,
where the probability of selecting a node grows linearly with its score.
This hedges our seeds against the threat of repeated collisions across rounds
by not repeatedly picking the same nodes as another team.
We accelerate this computation by considering the highest-scoring nodes first,
which greatly reduces the number of iterations required to find a fixed number of nodes by probabilistic means.

Additionally, we never pick a node with a closeness or degree centrality in the top 1% of the graph.
This further hedges our seeds against the threat of collisions,
as the data gleaned from histograms of prior rounds’ seed nodes showed that
some groups’ strategies heavily weighted one or both of these centrality metrics.
Often the highest scoring teams avoided the top 1% most-central nodes
(whether this is intentional or a by-product of a radically different algorithm is unknown),
so we emulated this in our design.

See report.pdf for more information about our approach and reasoning.

![Our Approach in a Nutshell](http://i.imgur.com/DJhUzRy.jpg)
