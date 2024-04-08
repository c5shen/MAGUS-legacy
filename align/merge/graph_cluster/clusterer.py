'''
Created on Aug 23, 2020

@author: Vlad
'''

import os
import time

from configuration import Configs

from align.merge.graph_cluster.mcl import runMclClustering
from align.merge.graph_cluster.mlr_mcl import runMlrMclClustering
from align.merge.graph_cluster.rg import rgClustering

from align.merge.graph_cluster.hipmcl import runHipMclClustering
from align.merge.graph_cluster.leiden import runLeiden

'''
The alignment graph is clustered, the clusters are written out as an array of node arrays.
MCL is the main way to do this, but rg could be used if there are scalability issues.
'''

def clusterGraph(graph):
    time1 = time.time()
    
    if os.path.exists(graph.clusterPath):
        Configs.log("Found existing cluster file {}".format(graph.clusterPath))
        graph.readClustersFromFile(graph.clusterPath)
        
    elif Configs.graphClusterMethod == "mcl":
        runMclClustering(graph)      
        
    elif Configs.graphClusterMethod == "mlrmcl":
        runMlrMclClustering(graph)
        
    elif Configs.graphClusterMethod == "rg":
        rgClustering(graph)
        
    elif Configs.graphClusterMethod == "hipmcl":
        runHipMclClustering(graph)
    
    elif "leiden" in Configs.graphClusterMethod:
        _method = Configs.graphClusterMethod.lower()
        if "cpm" in _method:
            runLeiden(graph, "cpm",
                    resolution_parameter=Configs.resolution_parameter)
        else:
            runLeiden(graph, "modularity")

    else:
        Configs.log("No alignment graph clustering requested..")
    
    time2 = time.time()  
    Configs.log("Clustered the graph in {} sec..".format(time2-time1))
