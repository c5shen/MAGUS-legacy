'''
3.22.2024 - Added by Chengze Shen
'''

from configuration import Configs
from tools import external_tools
from collections import defaultdict
import os

# convert matrix graph to undirected one (i.e., remove (j, i) if (i, j) already
# present
def convertGraph(inpath, outpath):
    edges = {}
    with open(inpath, 'r') as f:
        line = f.readline().strip()
        while line:
            s, t, w = line.split()
            # skip bi-directional edge
            if (int(s), int(t)) in edges or (int(t), int(s)) in edges:
                pass
            else:
                edges[(int(s), int(t))] = w
            line = f.readline().strip()
    # write to outpath
    with open(outpath, 'w') as f:
        for edge, w in edges.items():
            f.write('{} {} {}\n'.format(edge[0], edge[1], w))

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
            try: 
                # tab delimiter
                vertex, cluster = line.split('\t')
            except ValueError:
                # space delimiter
                vertex, cluster = line.split()

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
            #'--no-prune',
            #str(max(1, Configs.numCores // 2)), 
            '--quiet']
    Configs.debug('Running a command: {}'.format(' '.join(args)))
    os.system(' '.join(args))

    # post-process CM output and render correct format for following steps
    readCMOutput(CMOutputPath, graph.clusterPath, graph.graphPath)

    graph.readClustersFromFile(graph.clusterPath)

def runCMExperimental(graph, mode):
    Configs.log("(Chengze Shen) Running Min's CM pipeline (with weight support)...")
    Configs.log("CM using [{}, alpha={}]".format(mode, Configs.resolution_parameter))

    outdir = os.path.dirname(graph.clusterPath)
    CMOutputPath = os.path.join(outdir, 'cm_clusters.txt')

    # create a temporary file containing only one-direction edges of the
    # original graph
    modifiedGraphPath = os.path.join(outdir, 'graph_undirected.txt') 
    convertGraph(graph.graphPath, modifiedGraphPath)

    external_tools.runCMExperimental(modifiedGraphPath, Configs.resolution_parameter,
            mode, graph.workingDir, CMOutputPath).run()

    # post-process CM output and render correct format for following steps
    readCMOutput(CMOutputPath, graph.clusterPath, modifiedGraphPath)

    graph.readClustersFromFile(graph.clusterPath)
