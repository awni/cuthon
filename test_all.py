"""
Run tests with:

`pytest`
"""

import argparse
import cuthon

def test_argparse():

    argvs = ['cuthon.py', '--num_gpus=2', '--']
    exp_args = argparse.Namespace()
    exp_args.num_gpus = 2
    exp_cmd_args = ['python']
    args, cmd_args = cuthon.parse_args(argvs)

    assert args == exp_args
    assert cmd_args == exp_cmd_args

    argvs = ['cuthon.py', '--test_args1', '--test_args2']
    exp_args = argparse.Namespace()
    exp_args.num_gpus = 1
    exp_cmd_args = ['python', '--test_args1', '--test_args2']
    args, cmd_args = cuthon.parse_args(argvs)

    assert args == exp_args
    assert cmd_args == exp_cmd_args
