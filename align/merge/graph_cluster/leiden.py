'''
4.7.2024 - Added by Chengze Shen
'''

from configuration import Configs
import os, sys
import numpy as np

def runLeiden(graph, mode="modularity", resolution_parameter=0.01):
    inPath = graph.graphPath
    outdir = os.path.dirname(inPath)
    #outPath = outdir + '/graph.nolen.txt' 
    clusterPath = graph.clusterPath

    # only retaining edges with lengths >= median_length
    # since without doing so, Leiden-modularity gives 
    #Configs.log('(Chengze Shen) Creating graph by removing edge lengths...')
    #Configs.log('\t Only retaining edges with lengths >= median_length...')
    #edges = {}; lengths = []
    #with open(inPath, 'r') as f:
    #    line = f.readline().strip()
    #    while line:
    #        s, t, l = line.strip().split()
    #        lengths.append(int(l))
    #        edges[(s, t)] = int(l)
    #        line = f.readline().strip()
    #median_length = np.median(lengths)
    #with open(outPath, 'w') as f:
    #    for edge, l in edges.items():
    #        if l >= 10 * median_length:
    #            f.write('{} {}\n'.format(edge[0], edge[1]))
    # create no-edge-length graph from inPath
    #Configs.log('(Chengze Shen) Creating graph by removing edge lengths...')
    #cmd = ['cat', inPath, '|', 'awk \'{print $1 \" \" $2 }\'',
    #        '>', outPath]
    #os.system(' '.join(cmd))
    
    # import leidenalg, igraph and perform leiden operation
    import leidenalg as la
    import igraph as ig

    # read from graph.txt and create a tuple list of edges (no weights)
    # avoid adding edges that already exit (e.g., (a,b) then no (b,a))
    edges = set()
    with open(inPath, 'r') as f:
        line = f.readline().strip()
        while line:
            s, t, _ = line.strip().split()
            s = int(s); t = int(t)
            if not (s, t) in edges and not (t, s) in edges: 
                edges.add((s, t))
            line = f.readline().strip()
    g = ig.Graph.TupleList(edges, directed=False)
    #g = ig.Graph.Read_Edgelist(outPath, directed=False)
    if mode == 'modularity':
        Configs.log('(Chengze Shen) Running Leiden with [{}] ...'.format(mode))
        part = la.find_partition(g, la.ModularityVertexPartition)
    elif mode == 'cpm':
        Configs.log(
            '(Chengze Shen) Running Leiden with [{}, lambda={}] ...'.format(
                mode, resolution_parameter))
        part = la.find_partition(g, la.CPMVertexPartition,
                resolution_parameter=resolution_parameter)
    else:
        raise NotImplementedError

    # write to output
    Configs.log('(Chengze Shen) Writing clusters to {}'.format(clusterPath))
    with open(clusterPath, 'w') as f:
        for line in part:
            f.write('\t'.join([str(x) for x in line]))
            f.write('\n')
    graph.readClustersFromFile(graph.clusterPath)
