# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 09:08:57 2025

@author: brend

"""
# %% Global imports
from pathlib import Path


# %% py_project_manager imports
from py_project_manager.config import (
    Config,
    )

from py_project_manager.lib.logging_config import (
    Logger,
    )

# %% Module level configuration

api_models_ = Logger(
    logger_name="api.models.tables",
    log_file=str(Path(Config.LOG_DIR, 
                      "api.models.tables.log")),
    )
api_models_logger = api_models_.get_logger()


db_handler_ = Logger(
    logger_name="db_handler",
    log_file=str(Path(Config.LOG_DIR, 
                      "db_handler.log")),
    )
db_handler_logger = db_handler_.get_logger()


tests_ = Logger(
    logger_name="tests",
    log_file=str(Path(Config.LOG_DIR, 
                      "tests.log")),
    )
tests_logger = tests_.get_logger()

