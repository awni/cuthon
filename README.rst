Cuthon is a simple Python script to avoid setting `CUDA_VISIBLE_DEVICES` when
running python programs on a GPU. The script will find the first *unused*
GPU(s) then run the program as usual. At its simplest:

```
cuthon my_program.py
```

This tool is intended for a fairly niche use case: running python programs on
an interactive node which has more than one GPU. For those that have done this
often you may be relieved at never having to run `nvidia-smi` followed by
setting `CUDA_VISIBLE_DEVICES` again (when running a python program that is).
