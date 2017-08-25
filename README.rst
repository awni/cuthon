Cuthon is a simple Python script to avoid setting `CUDA_VISIBLE_DEVICES` when
running python programs on a GPU. This tool is intended for a fairly niche
use-case: running python programs on an interactive node which has more than
one GPU.  For those that have done this often you may be relieved at never
having to run `nvidia-smi` followed by setting `CUDA_VISIBLE_DEVICES` again
(when running a python program). This script should save you about 11.5 seconds
per python program launch -- approximately the time it takes to run
`nvidia-smi` followed by setting the `CUDA_VISIBLE_DEVICES` environment
variable. I hope you enjoy those returned seconds as much as I have.
