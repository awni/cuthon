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
SEP = "--"

class Status(enum.Enum):
    success = 0
    no_cuda = 1
    no_gpus = 2

def get_val(node):
    return int(node.text.split()[0])

def get_free(num_gpus):
    try:
        cmd = ["nvidia-smi", "-x", "-q"]
        nv_stats = subprocess.check_output(cmd)
    except OSError as e:
        return Status.no_cuda, 0

    gpus = ET.fromstring(nv_stats).findall("gpu")
    free_list = []
    for e, gpu in enumerate(gpus):

        mem = gpu.find("fb_memory_usage")
        tot = get_val(mem.find("total"))
        used = get_val(mem.find("used"))

        if used / tot < THRESHOLD:
            free_list.append(e)

    free_list = free_list[:num_gpus]
    if len(free_list) == num_gpus:
        status = Status.success
    else:
        status = Status.no_gpus

    return status, free_list

def parse_args(argvs):
    desc = ("Select the first available GPU(s) and run Python. "
            "To pass the script arguments specify '{0}' between "
            "cuthon arguments and arguments to be passed through "
            "to your script. If '{0}' is not specified, then all "
            "arguments will be passed through.")
    desc = desc.format(SEP)
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--num_gpus",
            type=int, default=1,
            help="The number of GPUs to use.")

    argvs = argvs[1:]
    if SEP in argvs:
        idx = argvs.index(SEP)
        args = parser.parse_args(argvs[:idx])
        cmd_args = argvs[idx + 1:]
    else:
        args = parser.parse_args([])
        cmd_args = argvs
    cmd_args.insert(0, "python")
    return args, cmd_args

def main():

    # TODOs
    # force run on gpu option
    # run on cpu option
    # run on cpu if no gpu available option
    # specify threshold

    args, cmd_args = parse_args(sys.argv)

    status, gpus = get_free(args.num_gpus)

    if status == Status.no_gpus:
        print("Not enough free GPUs found, aborting.")
        sys.exit(0)
    elif status == Status.no_cuda:
        print("nvidia-smi not found, aborting.")
        sys.exit(0)
    elif status == Status.success:
        gpu_env = ",".join(str(gpu) for gpu in gpus)
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_env

    subprocess.call(" ".join(cmd_args),
        env=os.environ, shell=True)

if __name__ == "__main__":
    main()
