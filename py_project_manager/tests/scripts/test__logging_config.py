# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:10:35 2025

@author: brend

# A tester for the logging_config module (within lib)

"""

# %% Global imports
from collections.abc import Callable
from pathlib import Path
from tqdm import tqdm

import inspect
import os
import pyjson5
import pytest
import shutil
import sys
import time


# %% py_project_manager imports
from py_project_manager.config import Config
# Need this to know where to add our test ruleset file

from py_project_manager.tests.lib import MiscTest
# This .py contains generic functions used across testing

# The component under test
from py_project_manager.lib.logging_config import Logger


# %% Module config




# %% Objects




# %% Functions


# %% Classes

# -----------------------------------------------------------------------------
class Test__logging_module:
    """!
    Class for testing the logging module
    
    """
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__instantiation(self=None):
        """!
        Testing instantiation
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger_ = Logger(
            logger_name=f"{test}",
            log_file=str(Path(Config.TEST_SUPPORTING_DATA, 
                              f"{test}.log")),
            )
        logger = logger_.get_logger()
        
        MiscTest.process_returns(
            test_no=test, 
            result=str(type(logger)),
            expected_response=
            "<class 'structlog._config.BoundLoggerLazyProxy'>"            
            )
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__debug_message(self=None):
        """!
        **Testing simple log messages - debug**
        
        This also implicitly tests specification of log file
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
        
        # Specifying the log file
        log_file = str(Path(Config.TEST_SUPPORTING_DATA, 
                            f"{test}.log"))
        
        # Creating the logger
        logger_ = Logger(
            logger_name=f"{test}",
            log_file=log_file,
            )
        logger = logger_.get_logger()
        
        # Sending a test message
        logger.debug("Test debug")
        
        # Dynamically get the line no in script of above
        logger_line = inspect.getframeinfo(inspect.currentframe())
        logger_line_ = logger_line.lineno - 3  # offset is -3
        
        # Then retrieving data from the log file to check it
        with open(log_file, "r") as f:
            log_file_ = f.readlines()
        
        log_line = pyjson5.decode(log_file_[-1])
        
        MiscTest.process_returns(
            test_no=test, 
            result={"event": log_line["event"],
                    "level": log_line["level"],
                    "filename": log_line["filename"],
                    "func_name": log_line["func_name"],
                    "lineno": log_line["lineno"],
                    },
            expected_response={"event": "Test debug",
                               "level": "debug",
                               "filename": Path(__file__).name,
                               "func_name": test,
                               "lineno": logger_line_,
                               },  
            )
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__info_message(self=None):
        """!
        **Testing simple log messages - info**
        
        This also implicitly tests specification of log file
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
        
        # Specifying the log file
        log_file = str(Path(Config.TEST_SUPPORTING_DATA, 
                            f"{test}.log"))
        
        # Creating the logger
        logger_ = Logger(
            logger_name=f"{test}",
            log_file=log_file,
            )
        logger = logger_.get_logger()
        
        # Sending a test message
        logger.info("Test info")
        
        # Dynamically get the line no in script of above
        logger_line = inspect.getframeinfo(inspect.currentframe())
        logger_line_ = logger_line.lineno - 3  # offset is -3
        
        # Then retrieving data from the log file to check it
        with open(log_file, "r") as f:
            log_file_ = f.readlines()
        
        log_line = pyjson5.decode(log_file_[-1])
        
        MiscTest.process_returns(
            test_no=test, 
            result={"event": log_line["event"],
                    "level": log_line["level"],
                    "filename": log_line["filename"],
                    "func_name": log_line["func_name"],
                    "lineno": log_line["lineno"],
                    },
            expected_response={"event": "Test info",
                               "level": "info",
                               "filename": Path(__file__).name,
                               "func_name": test,
                               "lineno": logger_line_,
                               },  
            )
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__warning_message(self=None):
        """!
        **Testing simple log messages - warning**
        
        This also implicitly tests specification of log file
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
        
        # Specifying the log file
        log_file = str(Path(Config.TEST_SUPPORTING_DATA, 
                            f"{test}.log"))
        
        # Creating the logger
        logger_ = Logger(
            logger_name=f"{test}",
            log_file=log_file,
            )
        logger = logger_.get_logger()
        
        # Sending a test message
        logger.warning("Test warning")
        
        # Dynamically get the line no in script of above
        logger_line = inspect.getframeinfo(inspect.currentframe())
        logger_line_ = logger_line.lineno - 3  # offset is -3
        
        # Then retrieving data from the log file to check it
        with open(log_file, "r") as f:
            log_file_ = f.readlines()
        
        log_line = pyjson5.decode(log_file_[-1])
        
        MiscTest.process_returns(
            test_no=test, 
            result={"event": log_line["event"],
                    "level": log_line["level"],
                    "filename": log_line["filename"],
                    "func_name": log_line["func_name"],
                    "lineno": log_line["lineno"],
                    },
            expected_response={"event": "Test warning",
                               "level": "warning",
                               "filename": Path(__file__).name,
                               "func_name": test,
                               "lineno": logger_line_,
                               },  
            )
                
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__error_message(self=None):
        """!
        **Testing simple log messages - error**
        
        This also implicitly tests specification of log file
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
        
        # Specifying the log file
        log_file = str(Path(Config.TEST_SUPPORTING_DATA, 
                            f"{test}.log"))
        
        # Creating the logger
        logger_ = Logger(
            logger_name=f"{test}",
            log_file=log_file,
            )
        logger = logger_.get_logger()
        
        # Sending a test message
        logger.error("Test error")
        
        # Dynamically get the line no in script of above
        logger_line = inspect.getframeinfo(inspect.currentframe())
        logger_line_ = logger_line.lineno - 3  # offset is -3
        
        # Then retrieving data from the log file to check it
        with open(log_file, "r") as f:
            log_file_ = f.readlines()
        
        log_line = pyjson5.decode(log_file_[-1])
        
        MiscTest.process_returns(
            test_no=test, 
            result={"event": log_line["event"],
                    "level": log_line["level"],
                    "filename": log_line["filename"],
                    "func_name": log_line["func_name"],
                    "lineno": log_line["lineno"],
                    },
            expected_response={"event": "Test error",
                               "level": "error",
                               "filename": Path(__file__).name,
                               "func_name": test,
                               "lineno": logger_line_,
                               },  
            )
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__critical_message(self=None):
        """!
        **Testing simple log messages - critical**
        
        This also implicitly tests specification of log file
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
        
        # Specifying the log file
        log_file = str(Path(Config.TEST_SUPPORTING_DATA, 
                            f"{test}.log"))
        
        # Creating the logger
        logger_ = Logger(
            logger_name=f"{test}",
            log_file=log_file,
            )
        logger = logger_.get_logger()
        
        # Sending a test message
        logger.critical("Test critical")
        
        # Dynamically get the line no in script of above
        logger_line = inspect.getframeinfo(inspect.currentframe())
        logger_line_ = logger_line.lineno - 3  # offset is -3
        
        # Then retrieving data from the log file to check it
        with open(log_file, "r") as f:
            log_file_ = f.readlines()
        
        log_line = pyjson5.decode(log_file_[-1])
        
        MiscTest.process_returns(
            test_no=test, 
            result={"event": log_line["event"],
                    "level": log_line["level"],
                    "filename": log_line["filename"],
                    "func_name": log_line["func_name"],
                    "lineno": log_line["lineno"],
                    },
            expected_response={"event": "Test critical",
                               "level": "critical",
                               "filename": Path(__file__).name,
                               "func_name": test,
                               "lineno": logger_line_,
                               },  
            )
        
        
# %% Main
if __name__ == "__main__":
    
    # Setup for pytest
    outFileName = os.path.basename(__file__)[:-3]  # Remove the .py from end
    outFile = open(outFileName + ".log", "w")
    currScript = os.path.basename(__file__)
    
    # -------------------------------------------------------------------------
    # ---- PyTest execution
    pytest.main([currScript, '--html', outFileName + '_report.html'])
    # Comment the above to (de)activate pyTest

    # -------------------------------------------------------------------------
    # ---- Local python execution
    
    # Test__logging_module().test__instantiation()
    # Test__logging_module().test__debug_message()
    # Test__logging_module().test__info_message()
    # Test__logging_module().test__warning_message()
    # Test__logging_module().test__error_message()
    # Test__logging_module().test__critical_message()
    