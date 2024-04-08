'''
3.22.2024 - Added by Chengze Shen
'''

from configuration import Configs
from tools import external_tools

def runHipMclClustering(graph):
    Configs.log("(Chengze Shen) Running HipMCL alignment graph clustering...")
    external_tools.runHipMcl(graph.graphPath, Configs.mclInflationFactor, graph.workingDir, graph.clusterPath).run()
    graph.readClustersFromFile(graph.clusterPath)
