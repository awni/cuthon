# cuthon
Cuthon is a simple Python script to avoid setting `CUDA_VISIBLE_DEVICES` when
running python programs on a GPU. The script will find the first *unused*
GPU(s) then run the program as usual. At its simplest:

```
cuthon my_program.py
```

This tool is intended for a fairly niche use-case: running python programs on
an interactive node which has more than one GPU. For those that have done this
often you may be relieved at never having to run `nvidia-smi` followed by
setting `CUDA_VISIBLE_DEVICES` again (when running a python program that is).
This script should save you about 11.5 seconds per python program launch --
approximately the time it takes to run `nvidia-smi` followed by setting the
`CUDA_VISIBLE_DEVICES` environment variable. I hope you enjoy those seconds
back as much as I have.

## Install

```
pip install cuthon
```

## Usage

In general, use `cuthon` just like you would use `python`.
- `cuthon` to launch a python repl.
- `cuthon -V` to see the python version number.
- `cuthon train_model.py` to run your program.

For help on available `cuthon` options type:
```
cuthon -h --
```

Note the `--` separator. This is to distinguish between `cuthon` arguments and
arguments to `python`. If the `--` is present then all arguments before it are
passed to `cuthon` and all arguments after are passed to python. If `--` is
absent all arguments are passed directly to python.

For example, to run on two available GPUs execute

```
cuthon --num_gpus=2 -- train_model.py
```
