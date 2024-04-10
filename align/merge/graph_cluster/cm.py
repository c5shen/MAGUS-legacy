'''
3.22.2024 - Added by Chengze Shen
'''

from configuration import Configs
from tools import external_tools
from collections import defaultdict
import os

# CM output: each line --> vertex id \t cluster id
def readCMOutput(inpath, outpath, graph):
    # read in all original vertices (for appending singletons) 
    vertices = set()
    with open(graph, 'r') as f:
        line = f.readline().strip()
        while line:
            s, t, _ = line.split()
            vertices.add(int(s))
            line = f.readline().strip()
    Configs.debug('Number of vertices in the graph: {}'.format(len(vertices)))

    clusters = defaultdict(list)
    max_cluster_id = 0
    with open(inpath, 'r') as f:
        line = f.readline().strip()
        while line:
            vertex, cluster = line.split('\t')
            vertices.remove(int(vertex))
            clusters[int(cluster)].append(vertex)
            max_cluster_id = max(max_cluster_id, int(cluster))
            line = f.readline().strip()
    Configs.debug('Number of singletons: {}'.format(len(vertices)))

    with open(outpath, 'w') as f:
        for cluster, ids in clusters.items():
            f.write('{}\n'.format('\t'.join(ids)))
        # write all remaining singletons as well
        for vertex in vertices:
            f.write('{}\n'.format(vertex))

def runCM(graph, mode):
    Configs.log("(Chengze Shen) Running Connectivity-Modifier (CM) pipeline...")
    Configs.log("CM using [{}, alpha={}]".format(mode, Configs.resolution_parameter))

    outdir = os.path.dirname(graph.clusterPath)
    CMOutputPath = os.path.join(outdir, 'cm_clusters.txt')

    #external_tools.runCM(graph.graphPath, Configs.resolution_parameter,
    #        graph.workingDir, CMOutputPath).run()
    #tempPath = os.path.join(outdir, 'temp_{}'.format(os.path.basename(CMOutputPath)))
    args = ['python3', '-m', 'hm01.cm', '-i', graph.graphPath,
            '-o', CMOutputPath, '-c', 'leiden',
            '-g', str(Configs.resolution_parameter),
            '--threshold', '1log10', '--nprocs',
            '1',
            #str(max(1, Configs.numCores // 2)), 
            '--quiet']
    Configs.debug('Running a command: {}'.format(' '.join(args)))
    os.system(' '.join(args))

    # post-process CM output and render correct format for following steps
    readCMOutput(CMOutputPath, graph.clusterPath, graph.graphPath)

    graph.readClustersFromFile(graph.clusterPath)
