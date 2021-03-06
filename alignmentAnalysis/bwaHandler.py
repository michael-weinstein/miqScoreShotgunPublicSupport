def bwaAlignPE(forwardReads:str, reverseReads:str, workingFolder:str, outputBAM:str, refGenome:str, coreLimit:int=None, compressionCoresPercentage:float=0.15, mock:bool=False):
    import multiprocessing
    import os
    availableCores = multiprocessing.cpu_count() - 1
    if coreLimit and coreLimit > 0:
        availableCores = max([availableCores, coreLimit])
    compressionCores = round(availableCores * compressionCoresPercentage)
    compressionCores = max([compressionCores, 1])
    alignmentCores = availableCores - compressionCores
    if alignmentCores < 1:
        streaming = False
    else:
        streaming = True
    if streaming:
        bwaCommand = "bwa mem -t %s %s %s %s" %(alignmentCores, refGenome, forwardReads, reverseReads)
        samtoolsCommand = "samtools view -b -@ %s -o %s" %(compressionCores, outputBAM)
        combinedCommand = "%s | %s" %(bwaCommand, samtoolsCommand)
        print("RUN: %s" %combinedCommand, flush=True)
        if "MOCK" in os.environ:
            mock = True
        if not mock:
            exitCode = os.system(combinedCommand)
        else:
            exitCode = 0
            print("MOCK RUN: %s" %combinedCommand)
        print("Completed with status %s" %exitCode, flush=True)
        if exitCode:
            raise RuntimeError("Running alignment and compression returned a non-zero exit status")
    else:
        tempSAM = os.path.join(workingFolder, "temp.sam")
        bwaCommand = "bwa mem %s %s %s > %s" % (refGenome, forwardReads, reverseReads, tempSAM)
        samtoolsCommand = "samtools view -b -@ %s -o %s %s" % (compressionCores, outputBAM, tempSAM)
        combinedCommand = "%s && %s && rm %s" % (bwaCommand, samtoolsCommand, tempSAM)
        print("RUN: %s" % combinedCommand)
        if not mock:
            exitCode = os.system(combinedCommand)
        else:
            exitCode = 0
            print("MOCK RUN: %s" %combinedCommand)
        print("Completed with status %s" % exitCode)
        if exitCode:
            raise RuntimeError("Running alignment and compression returned a non-zero exit status")


def bwaAlignSE(forwardReads:str, workingFolder:str, outputBAM:str, refGenome:str, coreLimit:int=None, compressionCoresPercentage:float=0.15, mock:bool=False):
    import multiprocessing
    import os
    availableCores = multiprocessing.cpu_count() - 1
    if coreLimit and coreLimit > 0:
        availableCores = max([availableCores, coreLimit])
    compressionCores = round(availableCores * compressionCoresPercentage)
    compressionCores = max([compressionCores, 1])
    alignmentCores = availableCores - compressionCores
    if alignmentCores < 1:
        streaming = False
    else:
        streaming = True
    if streaming:
        bwaCommand = "bwa mem -t %s %s %s" %(alignmentCores, refGenome, forwardReads)
        samtoolsCommand = "samtools view -b -@ %s -o %s" %(compressionCores, outputBAM)
        combinedCommand = "%s | %s" %(bwaCommand, samtoolsCommand)
        print("RUN: %s" %combinedCommand, flush=True)
        if "MOCK" in os.environ:
            mock = True
        if not mock:
            exitCode = os.system(combinedCommand)
        else:
            exitCode = 0
            print("MOCK RUN: %s" %combinedCommand)
        print("Completed with status %s" %exitCode, flush=True)
        if exitCode:
            raise RuntimeError("Running alignment and compression returned a non-zero exit status")
    else:
        tempSAM = os.path.join(workingFolder, "temp.sam")
        bwaCommand = "bwa mem %s %s > %s" % (refGenome, forwardReads, tempSAM)
        samtoolsCommand = "samtools view -b -@ %s -o %s %s" % (compressionCores, outputBAM, tempSAM)
        combinedCommand = "%s && %s && rm %s" % (bwaCommand, samtoolsCommand, tempSAM)
        print("RUN: %s" % combinedCommand)
        if not mock:
            exitCode = os.system(combinedCommand)
        else:
            exitCode = 0
            print("MOCK RUN: %s" %combinedCommand)
        print("Completed with status %s" % exitCode)
        if exitCode:
            raise RuntimeError("Running alignment and compression returned a non-zero exit status")