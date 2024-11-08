'''
Created on Apr 14, 2020

@author: Vlad
'''

import os
import time
import shutil

from helpers import sequenceutils

class Configs:
    
    workingDir = None
    sequencesPath = None
    subsetPaths = None
    subalignmentPaths = None
    backbonePaths = None
    guideTree = "fasttree"
    outputPath = None
    dataType = None
    
    decompositionMaxNumSubsets = 25
    decompositionMaxSubsetSize = 50
    decompositionStrategy = "pastastyle"
    decompositionSkeletonSize = 300
    #decompositionKmhIterations = 1
    
    graphBuildMethod = "mafft"
    graphBuildHmmExtend = False
    graphBuildRestrict = False
    graphClusterMethod = "mcl" 
    graphTraceMethod = "minclusters"
    graphTraceOptimize = False
    
    mafftRuns = 10
    mafftSize = 200
    mclInflationFactor = 4
    
    constrain = True
    onlyGuideTree = False
    recurse = True
    recurseGuideTree = "fasttree"
    recurseThreshold = 200
    
    clustalPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/clustal/clustalo")
    mafftPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/mafft/mafft")
    mclPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/mcl/bin/mcl")
    mlrmclPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/mlrmcl/mlrmcl")
    hmmalignPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/hmmer/hmmalign")
    hmmbuildPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/hmmer/hmmbuild")
    hmmsearchPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/hmmer/hmmsearch")
    fasttreePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/fasttree/FastTreeMP")
    raxmlPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/raxmlng/raxml-ng")

    '''
    5.9.2024 - bin path to cmExp
    '''
    cmExpPath = shutil.which('cmExp')

    '''
    3.22.2024 - Added by Chengze Shen
    path to hipmcl, and per-process-mem
    4.7.2024 - Updated by ----
    added resolution_parameter argument
    5.8.2024 - Updated by ----
    added num_trials argument for Infomap
    '''
    hipmclPath = shutil.which('hipmcl')
    per_process_mem = 8
    resolution_parameter = 0.01
    num_trials = 1

    logPath = None
    errorPath = None
    debugPath = None
    
    numCores = 1
    searchHeapLimit = 5000
    alignmentSizeLimit = 100
    
    @staticmethod
    def log(msg, path = None):
        print(msg)
        path = Configs.logPath if path is None else path
        Configs.writeMsg(msg, path)
    
    @staticmethod
    def error(msg, path = None):
        Configs.log(msg)
        path = Configs.errorPath if path is None else path
        Configs.writeMsg(msg, path)
    
    @staticmethod
    def debug(msg, path = None):
        path = Configs.debugPath if path is None else path
        Configs.writeMsg(msg, path)
    
    @staticmethod
    def writeMsg(msg, path):
        if path is not None:
            with open(path, 'a') as logFile:
                logFile.write("{}    {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), msg))
    
    @staticmethod
    def inferDataType(sequencesFile):
        if Configs.dataType is None:
            Configs.dataType = sequenceutils.inferDataType(sequencesFile)
            Configs.log("Data type wasn't specified. Inferred data type {} from {}".format(Configs.dataType.upper(), sequencesFile))
        return Configs.dataType 

def buildConfigs(args):
    Configs.outputPath = os.path.abspath(args.output)
    
    if args.directory is not None:
        Configs.workingDir = os.path.abspath(args.directory) 
    else:
        Configs.workingDir = os.path.join(os.path.dirname(Configs.outputPath), "magus_working_dir")
    if not os.path.exists(Configs.workingDir):
        os.makedirs(Configs.workingDir)
    
    Configs.sequencesPath = os.path.abspath(args.sequences) if args.sequences is not None else Configs.sequencesPath
    
    Configs.guideTree = os.path.abspath(args.guidetree) if args.guidetree is not None else Configs.guideTree
    if args.guidetree is not None:
        Configs.guideTree = os.path.abspath(args.guidetree) if os.path.exists(os.path.abspath(args.guidetree)) else args.guidetree
    
    Configs.subalignmentPaths = []
    for p in args.subalignments:
        path = os.path.abspath(p)
        if os.path.isdir(path):
            for filename in os.listdir(path):
                Configs.subalignmentPaths.append(os.path.join(path, filename))
        else:
            Configs.subalignmentPaths.append(path)
    
    Configs.backbonePaths = []
    for p in args.backbones:
        path = os.path.abspath(p)
        if os.path.isdir(path):
            for filename in os.listdir(path):
                Configs.backbonePaths.append(os.path.join(path, filename))
        else:
            Configs.backbonePaths.append(path)

    if args.numprocs > 0:
        Configs.numCores = args.numprocs
    else:
        Configs.numCores = os.cpu_count()

    Configs.decompositionMaxSubsetSize = args.maxsubsetsize
    Configs.decompositionMaxNumSubsets = args.maxnumsubsets
    Configs.decompositionStrategy = args.decompstrategy
    Configs.decompositionSkeletonSize = args.decompskeletonsize
    Configs.dataType = args.datatype
    
    Configs.graphBuildMethod = args.graphbuildmethod
    Configs.graphBuildHmmExtend = args.graphbuildhmmextend.lower() == "true"
    Configs.graphBuildRestrict = args.graphbuildrestrict.lower() == "true"
    Configs.graphClusterMethod = args.graphclustermethod
    Configs.graphTraceMethod = args.graphtracemethod
    Configs.graphTraceOptimize = args.graphtraceoptimize.lower() == "true"

    Configs.mafftRuns = args.mafftruns
    Configs.mafftSize = args.mafftsize
    Configs.mclInflationFactor = args.inflationfactor
    
    Configs.constrain = args.constrain.lower() == "true"
    Configs.onlyGuideTree = args.onlyguidetree.lower() == "true"
    Configs.recurse = args.recurse.lower() == "true"
    Configs.recurseGuideTree = args.recurseguidetree
    Configs.recurseThreshold = args.recursethreshold
    
    Configs.logPath = os.path.join(Configs.workingDir, "log.txt")    
    Configs.errorPath = os.path.join(Configs.workingDir, "log_errors.txt")
    Configs.debugPath = os.path.join(Configs.workingDir, "log_debug.txt")
    
    Configs.alignmentSizeLimit = args.alignsizelimit

    '''
    3.22.2024 - Added by Chengze Shen
    take input for per_process_mem
    5.8.2024 - Added by ----
    take input for num_trials
    '''
    Configs.num_nodes = args.num_nodes
    Configs.per_process_mem = args.per_process_mem
    Configs.resolution_parameter = args.resolution_parameter
    Configs.num_trials = args.num_trials
