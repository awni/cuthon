======
cuthon
======

Cuthon is a simple Python script to avoid setting `CUDA_VISIBLE_DEVICES` when
running python programs on a GPU. The script will find the first *unused*
GPU(s) then run the program as usual. At its simplest::

  cuthon my_program.py

This tool is intended for a fairly niche use case: running python programs on
an interactive node which has more than one GPU. For those that have done this
often you may be relieved at never having to run `nvidia-smi` followed by
setting `CUDA_VISIBLE_DEVICES` again (when running a python program that is).

-------
Install
-------
Install with `pip`::

    pip install cuthon

-----
Usage
-----

In general, use `cuthon` just like you would use `python`.

- `cuthon` to launch a python repl.
- `cuthon -V` to see the python version number.
- `cuthon train_model.py` to run your program.

For help on available `cuthon` options type::

    cuthon -h --

The output will be::

    usage: cuthon.py [-h] [-n NUM_GPUS] [-l]

    Select the first unused GPU(s) and run Python. To pass the script arguments
    specify '--' between cuthon arguments and arguments to be passed through to
    your script. If '--' is not specified, then all arguments will be passed
    through.

    optional arguments:
      -h, --help            show this help message and exit
      -n NUM_GPUS, --num_gpus NUM_GPUS
                            The number of GPUs to use.
      -l, --least_used      Switch from an unused to a least-used policy.

For example, to run on two available GPUs execute::

    cuthon -n 2 -- train_model.py
