#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

THRESHOLD = 0.05
SEP = "--"

def get_val(node):
    return int(node.text.split()[0])

def get_usage():
    cmd = ["nvidia-smi", "-x", "-q"]
    nv_stats = subprocess.check_output(cmd)

    gpus = ET.fromstring(nv_stats).findall("gpu")
    usage = []
    for e, gpu in enumerate(gpus):

        mem = gpu.find("fb_memory_usage")
        tot = get_val(mem.find("total"))
        used = get_val(mem.find("used"))
        usage.append(used / tot)
    return usage

def get_least(usage, num_gpus):
    least_list = sorted(enumerate(usage),
                        key=lambda x: x[1])
    least_list = list(zip(*least_list))[0]
    return least_list[:num_gpus]

def get_free(usage, num_gpus):
    free_list = [e for e, used in enumerate(usage)
                    if used < THRESHOLD]
    free_list = free_list[:num_gpus]
    return free_list

def parse_args(argvs):
    desc = ("Select the first unused GPU(s) and run Python. "
            "To pass the script arguments specify '{0}' between "
            "cuthon arguments and arguments to be passed through "
            "to your script. If '{0}' is not specified, then all "
            "arguments will be passed through.")
    desc = desc.format(SEP)
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-n", "--num_gpus",
        type=int, default=1,
        help="The number of GPUs to use.")
    parser.add_argument("-l", "--least_used",
        action="store_true",
        help="Switch from an unused to a least-used policy.")

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

    args, cmd_args = parse_args(sys.argv)

    try:
        usage = get_usage()
    except OSError as e:
        print("nvidia-smi not found, aborting.")
        sys.exit(1)

    if args.least_used:
        gpus = get_least(usage, args.num_gpus)
    else:
        gpus = get_free(usage, args.num_gpus)

    if len(gpus) < args.num_gpus:
        print("Not enough free GPUs found, aborting.")
        sys.exit(2)

    gpu_env = ",".join(str(gpu) for gpu in gpus)
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu_env

    sys.exit(subprocess.call(" ".join(cmd_args),
                env=os.environ, shell=True))

if __name__ == "__main__":
    main()
