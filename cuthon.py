#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import argparse
import enum
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

THRESHOLD = 0.05

class Status(enum.Enum):
    success = 0
    no_cuda = 1
    no_gpu = 2

def get_val(node):
    return int(node.text.split()[0])

def get_first_free():
    try:
        cmd = ["nvidia-smi", "-x", "-q"]
        nv_stats = subprocess.check_output(cmd)
    except OSError as e:
        return Status.no_cuda, 0

    gpus = ET.fromstring(nv_stats).findall("gpu")
    for e, gpu in enumerate(gpus):

        mem = gpu.find("fb_memory_usage")
        tot = get_val(mem.find("total"))
        used = get_val(mem.find("used"))

        if used / tot < THRESHOLD:
            return Status.success, e

    return Status.no_gpu, e

def main():
    SEP = "--"
    desc = ("Select the first available GPU(s) and run Python. "
            "To pass the script arguments specify '{0}' between "
            "cuthon arguments and arguments to be passed through "
            "to your script. If '{0}' is not specified, then all "
            "arguments will be passed through.")
    desc = desc.format(SEP)

    parser = argparse.ArgumentParser(description=desc)
    # num_gpus option
    # force run on gpu option
    # run on cpu option
    # run on cpu if no gpu available option
    # specify threshold

    argvs = sys.argv[1:]
    if SEP in argvs:
        idx = argvs.index(SEP)
        args = parser.parse_args(argvs[:idx])
        cmd_args = argvs[idx + 1:]
    else:
        args = []
        cmd_args = argvs

    args = parser.parse_args(args)

    status, gpu = get_first_free()

    if status == Status.no_gpu:
        print("No free GPUs found, aborting.")
        sys.exit(0)
    elif status == Status.no_cuda:
        print("nvidia-smi not found, aborting.")
        sys.exit(0)
    elif status == Status.success:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)

    cmd_args.insert(0, "python")
    subprocess.call(" ".join(cmd_args), env=os.environ, shell=True)

if __name__ == "__main__":
    main()
