# _

## About

This is a personal set of tools to automatically save stuff during exploratory research.

It is based on a custom fork of <https://github.com/bartman/git-wip> and some personal python functions.

## Install

1. Clone the repository and install the python package:

  ```console
  git clone https://github.com/tomdlt/savate.git
  cd savate
  pip install -e .
  ```

2. Change `SAVE_PATH` in `savate/io.py` to a path that suits your need.

## Example

If I want to save a matplotlib figure, I just call:

```python
from savate import save_fig
save_fig(fig, 'simulation_0')
```

which under the hood will:

- get the general save path stored in `SAVE_PATH`,
- add it the python script name that I ran (if I ran `python my_script.py` it will be `my_script`),
- add the file name, a timestamp and a number if necessary to make it unique,
- save at this full path (e.g. `SAVE_PATH/my_script/simulation_0_2017-11-03-18h58.png`),
- create a git commit on a branch called `my_branch_wip` without leaving `my_branch`.

Therefore, my figures are automatically sorted in directories named by the scripts that created them. Their names are unique to prevent overwrite, and contain a timestamp that I can use to recover the code in my `*_wip` branch.
