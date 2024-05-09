'''
4.11.2024 - Added by Chengze Shen
'''

from configuration import Configs
from tools import external_tools
import os
from collections import defaultdict

def runInfomapClustering(graph):
    Configs.log("(Chengze Shen) Running Infomap clustering...")
    infomapOutpath = os.path.join(os.path.dirname(graph.graphPath),
            'infomap.clusters.txt')
    num_trials = Configs.num_trials
    external_tools.runInfomap(graph.graphPath, graph.workingDir,
            infomapOutpath, num_trials).run()

    # post-process infomap output to actual graph.clusterPath
    Configs.log("(Chengze Shen) Reading and processing Infomap output: {}".format(
        infomapOutpath))
    clusters = defaultdict(list)
    with open(infomapOutpath, 'r') as f:
        line = f.readline().strip()
        while line:
            if not line.startswith('#'):
                node, idx, _ = line.split()
                clusters[idx].append(node)
            line = f.readline().strip()
    with open(graph.clusterPath, 'w') as f:
        for clt, nodes in clusters.items():
            if len(nodes) > 0:
                f.write('\t'.join(nodes) + '\n')
    graph.readClustersFromFile(graph.clusterPath)
