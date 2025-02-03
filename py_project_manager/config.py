# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 21:40:43 2025

@author: brendan

The configuration file for py_project_manager

Sensitive variables will be held within the host PC's environmental variables

"""
# %% Global imports
from pathlib import Path

import importlib.util
import platform


# %% py_project_manager imports


# %% Module level config

host_drive_map = {
    "Barricade": "C:"
    }

library_dir = Path(importlib.util.find_spec(
    "py_project_manager").submodule_search_locations[0]).parent


# %% Classes

class Config:
    log_drive = host_drive_map.get(platform.node()) or Path.cwd().drive
    # This reverts to the drive holding the file if its not in explicit map
    
    LOG_DIR = str(Path(f"{log_drive}\\", "log_files"))
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

    TEST_SUPPORTING_DATA = str(Path(library_dir,
                                    "py_project_manager",
                                    "tests",
                                    "supporting_data"))
