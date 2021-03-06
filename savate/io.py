import traceback
import subprocess
import os
import time

import numpy as np
import pandas as pd
from scipy import io


# directory to save the plots
SAVE_PATH = os.environ['HOME'] + '/work/figures/'


def save_fig(fig, name, extension='.png', *args, **kwargs):
    """Save a matplotlib figure in proper directory with the time in filename
    """
    commit_with_git_wip()
    save_name = _compute_name(name=name, extension=extension)
    fig.savefig(save_name, *args, **kwargs)
    print('Saved fig: %s' % save_name)
    return save_name


def save_data(data, name, overwrite=False):
    """Save the data in proper directory with the time in filename
    """
    commit_with_git_wip()
    if isinstance(data, pd.DataFrame):
        save_name = _compute_name(name=name, extension='.csv',
                                  overwrite=overwrite)
        data.to_csv(save_name)
    elif name[-4:] == '.mat':
        save_name = _compute_name(name=name, extension='.mat',
                                  overwrite=overwrite)
        if not isinstance(data, dict):
            data = {'data': data}
        io.savemat(save_name, data)
    else:
        save_name = _compute_name(name=name, extension='.npy',
                                  overwrite=overwrite)
        np.save(save_name, data)
    print('Saved data: %s' % save_name)
    return save_name


def load_data(name):
    """Find the data in proper directory and load it
    """
    full_name = _compute_name(name=name, extension='', overwrite=True)

    extensions = ['.mat', '.csv', '.npy']
    all_names = [name, full_name]
    all_names += [full_name + ext for ext in extensions]
    all_names += [name + ext for ext in extensions]

    load_name = None
    for this in all_names:
        if os.path.isfile(this):
            load_name = this
            break

    if load_name is None:
        raise ValueError('File not found: %s' % name)
    elif load_name[-4:] == '.mat':
        data = io.loadmat(load_name)
    elif load_name[-4:] == '.csv':
        data = pd.read_csv(load_name)
    elif load_name[-4:] == '.npy':
        data = np.load(load_name).item()
    else:
        raise ValueError('Unknown extension: %s' % load_name)

    print('Loaded data: %s' % load_name)
    return data


def _compute_name(name, extension, overwrite=False, path_name=SAVE_PATH):
    """Compute a file name, with the script name in prefix and time in suffix

    Parameters
    ----------
    name: string
        The original name (e.g. "my_figure")
    extension: string
        The file extansion (e.g. ".txt")
    overwrite: boolean
        If True, does not add a time stemp nor unique suffix.
        It can potentially overwrite an existing file.
    path_name: string
        Path to the general save directory

    Returns
    -------
    filename: string
        A transformed filename
    """
    script_name, directory_name = _get_calling_script()

    # create directory with script name
    directory = os.path.join(path_name, directory_name, script_name)
    if not os.path.exists(directory):
        # add robustness to multiple threads creating the same directory
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass

    # add directory to file name
    save_name = os.path.join(directory, name)

    if overwrite:
        suffix = ''
    else:
        # add time at the end of the file name
        suffix_time = '_' + time_string()

        # check if the file already exists and add a suffix
        k = 0
        suffix = ''
        while os.path.isfile(save_name + suffix_time + suffix + extension):
            k += 1
            suffix = '_%d' % k
        suffix = suffix_time + suffix

    filename = save_name + suffix + extension
    return filename


def _get_calling_script():
    """Get the calling script from the traceback stack"""
    stack = traceback.extract_stack()

    script_path = None
    for trace in stack:
        if trace[2] == '<module>':
            script_path = trace[0]
    if script_path is None:
        for trace in stack:
            if '/run_' in trace[0]:
                script_path = trace[0]
    if script_path is None:
        script_path = stack[-1][0]  # default

    script_name = os.path.basename(script_path)
    directory_name = os.path.basename(os.path.dirname(script_path))
    if script_name[:14] == '<ipython-input':
        script_name = '<ipython>'
    if script_name[-3:] == '.py':
        script_name = script_name[:-3]

    return script_name, directory_name


def time_string():
    """
    Get the time in a string
    """
    t = time.localtime(time.time())
    return '%4d-%02d-%02d-%02dh%02d' % (t[0], t[1], t[2], t[3], t[4])


def commit_with_git_wip():
    script_name, _ = _get_calling_script()
    commit_message = "autosave called from " + script_name

    try:
        result = subprocess.run(["git", "wip", "save_silent", commit_message])
    except Exception as e:
        print(e)
        result = 1
    return result
