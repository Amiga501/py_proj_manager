# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:10:35 2025

@author: brend

# A tester for the db_handler module

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

from py_project_manager.tests.lib.test_misc import MiscTest
# This .py contains generic functions used across testing

from py_project_manager.lib.logging_config import Logger
# The logger

# The table objects
from py_project_manager.api.models.tables import (
    HumanResource,
    Organisation,
    Project,
    Task,
    TaskItem,
    )

# The component under test
from py_project_manager.api.services.db_handler import (
    DatabaseHandler,
    )


# %% Module config


# %% Objects




# %% Functions

# -----------------------------------------------------------------------------
def get_logger(test_name: str ) -> Callable:
    """!
    **Get a logger handle**
    
    """
    logger_ = Logger(
        logger_name=f"{test_name}",
        log_file=str(Path(Config.TEST_SUPPORTING_DATA, 
                          f"{test_name}.log")),
        )
    logger = logger_.get_logger()
    
    return logger

# -----------------------------------------------------------------------------
def reset_database( 
        db_handler: Callable,
        ):
    """!
    **Reset the database to original state**
    
    Does this by dropping all tables. The ORM will recreate the tables afresh
    upon conenction for next test
    
    """
    for table in db_handler.table_objects:
        table.metadata.drop_all(bind=db_handler.engine)


# %% Pre testing configuration

logger = get_logger("PreTestConfig")


# %% Classes

# -----------------------------------------------------------------------------
class Test__HumanResource:
    """!
    Class for testing the HumanResource database handler methods
    
    """
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_human_resource(self=None):
        """!
        Testing simple human resource
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
        
        created_ = db_handler.create_human_resource(
            forename="Darth",
            surname="Vader",
            email="darth.vader@galactic-empires.com",
            division="Sith Lords",
            working_week_hrs=40,
            )
                
        retrieved_ = db_handler.get_human_resource(
            email="darth.vader@galactic-empires.com")
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_),
            expected_response=1,
            )
        
        if len(retrieved_) != 1:
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_.as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------

# -----------------------------------------------------------------------------
class Test__Organisation:
    """!
    Class for testing the Organisation database handler methods
    
    """
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_organisation(self=None):
        """!
        Testing simple organisation
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
        
        created_ = db_handler.create_organisation(
            name="Test Organ #1",
            logo_path="ExampleLogo.png")
                
        retrieved_ = db_handler.get_organisation(
            name="Test Organ #1")
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_),
            expected_response=1,
            )
        
        if len(retrieved_) != 1:
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_.as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------
class Test__Project:
    """!
    Class for testing the Project database handler methods
    
    """
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_project(self=None):
        """!
        Testing simple project
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
        
        _ = db_handler.create_organisation(
            name="Test Organ Name #1",
            logo_path="ExampleLogo.png")
        
        created_ = db_handler.create_project(
            name="Test Proj #1",
            code="XXX_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
    
        retrieved_ = db_handler.get_project(
            name="Test Proj #1",
            )
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_),
            expected_response=1,
            )
        
        if len(retrieved_) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_.as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    

# -----------------------------------------------------------------------------
class Test__Task:
    """!
    Class for testing the Task database handler methods
    
    """
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task(self=None):
        """!
        Testing simple task
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
        
        
        _ = db_handler.create_organisation(
            name="Test Organ Name #1",
            logo_path="ExampleLogo.png")
                
        _ = db_handler.create_project(
            name="Test Proj #1",
            code="XXX_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
        
        created_ = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_ = db_handler.get_task(
            id=created_.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_),
            expected_response=1,
            )
        
        if len(retrieved_) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_.as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    

# -----------------------------------------------------------------------------
class Test__TaskItem:
    """!
    Class for testing the TaskItem database handler methods
    
    """
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_item(self=None):
        """!
        Testing simple task item
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
        
        _ = db_handler.create_organisation(
            name="Test Organ Name #1",
            logo_path="ExampleLogo.png")
                
        _ = db_handler.create_project(
            name="Test Proj #1",
            code="XXX_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
        
        task_ = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        created_ = db_handler.create_taskitem(
            name="Test TaskItem #1",
            duration_hrs=8,
            task_id=task_.id,
            )
        
        retrieved_ = db_handler.get_taskitem(
            id=created_.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_),
            expected_response=1,
            )
        
        if len(retrieved_) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_.as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    
    
        
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
    
    # Test__Organisation().test__create_organisation()
    # Test__HumanResource().test__create_human_resource()
    # Test__Project().test__create_project()
    # Test__Task().test__create_task()
    # Test__TaskItem.test__create_task_item()
    