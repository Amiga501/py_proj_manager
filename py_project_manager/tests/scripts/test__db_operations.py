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
import sqlalchemy as db
import sys
import time


# %% py_project_manager imports
from py_project_manager.config import Config
# Need this to know where to add our test ruleset file

from py_project_manager.lib.loggers import ( 
    tests_logger as LOGGER,
    )

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
def reset_database( 
        db_handler: Callable,
        ):
    """!
    **Reset the database to original state**
    
    Does this by dropping all tables. The ORM will recreate the tables afresh
    upon conenction for next test
    
    """
    for table in db_handler.table_objects:
        table_name = table.__tablename__
        table_exist = \
            db.inspect(db_handler.engine).has_table(table_name)
        if table_exist:
            table.metadata.drop_all(bind=db_handler.engine)
        

# %% Pre testing configuration


# %% Classes

# -----------------------------------------------------------------------------
class Test__HumanResource:
    """!
    Class for testing the HumanResource database handler methods
    
    """
    
    db_handler = DatabaseHandler(
        )
    
    reset_database(db_handler)
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_human_resource(self=None):
        """!
        Testing simple human resource
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                 
        db_handler = DatabaseHandler(
            logger=LOGGER,
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
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__non_unique_email(self=None):
        """!
        Testing double email
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
                
        created_1 = db_handler.create_human_resource(
            forename="Darth",
            surname="Vader",
            email="darth.vader@galactic-empires.com",
            division="Sith Lords",
            working_week_hrs=40,
            )
                
        retrieved_ = db_handler.get_human_resource(
            email="darth.vader@galactic-empires.com")
        
        created_2 = db_handler.create_human_resource(
            forename="Darth_",
            surname="Vader_",
            email="darth.vader@galactic-empires.com",
            division="Something else",
            working_week_hrs=41,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_2,
            expected_response=None,
            )
        
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()

    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__below_min_hrs(self=None):
        """!
        Testing below minimum hours
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
                
        created_1 = db_handler.create_human_resource(
            forename="Darth",
            surname="Vader",
            email="darth.vader@galactic-empires.com",
            division="Sith Lords",
            working_week_hrs=7,
            )
                
        retrieved_ = db_handler.get_human_resource(
            email="darth.vader@galactic-empires.com")
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.working_week_hrs,
            expected_response=8.0,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__at_min_hrs(self=None):
        """!
        Testing at minimum hours
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
                
        created_1 = db_handler.create_human_resource(
            forename="Darth",
            surname="Vader",
            email="darth.vader@galactic-empires.com",
            division="Sith Lords",
            working_week_hrs=8,
            )
                
        retrieved_ = db_handler.get_human_resource(
            email="darth.vader@galactic-empires.com")
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.working_week_hrs,
            expected_response=8.0,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__at_max_hrs(self=None):
        """!
        Testing at maximum hours
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
                
        created_1 = db_handler.create_human_resource(
            forename="Darth",
            surname="Vader",
            email="darth.vader@galactic-empires.com",
            division="Sith Lords",
            working_week_hrs=80,
            )
                
        retrieved_ = db_handler.get_human_resource(
            email="darth.vader@galactic-empires.com")
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.working_week_hrs,
            expected_response=80.0,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__above_max_hrs(self=None):
        """!
        Testing above maximum hours
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
                
        created_1 = db_handler.create_human_resource(
            forename="Darth",
            surname="Vader",
            email="darth.vader@galactic-empires.com",
            division="Sith Lords",
            working_week_hrs=81,
            )
                
        retrieved_ = db_handler.get_human_resource(
            email="darth.vader@galactic-empires.com")
                
        retrieved = retrieved_[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.working_week_hrs,
            expected_response=80.0,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__unique_emails_different_names(self=None):
        """!
        Testing double email
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
                
        created_1 = db_handler.create_human_resource(
            forename="Darth",
            surname="Vader",
            email="darth.vader@galactic-empires.com",
            division="Sith Lords",
            working_week_hrs=40,
            )
        
        created_2 = db_handler.create_human_resource(
            forename="Darth",
            surname="Vader",
            email="darth.vader2@galactic-empires.com",
            division="Sith Lords",
            working_week_hrs=41,
            )
        
        retrieved_1 = db_handler.get_human_resource(
            email="darth.vader@galactic-empires.com")
        retrieved1 = retrieved_1[0]
        
        retrieved_2 = db_handler.get_human_resource(
            email="darth.vader2@galactic-empires.com")
        retrieved2 = retrieved_2[0]
        
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved1.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved2.as_dict(),
            expected_response=created_2.as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()    
    
    # -------------------------------------------------------------------------
    


# -----------------------------------------------------------------------------
class Test__Organisation:
    """!
    Class for testing the Organisation database handler methods
    
    """
    
    db_handler = DatabaseHandler(
        logger=logger,
        )
    
    reset_database(db_handler)
    
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
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__duplicate_organisation(self=None):
        """!
        Testing duplicate name of organisation
        
        2nd attempt to create an identical organisation name will return 
        original
        
        """        
        test = inspect.stack()[0][3]  # The name of this function (test)
        print(f"{test}()")
                
        logger = get_logger(test)
        
        db_handler = DatabaseHandler(
            logger=logger,
            )
                
        created_1 = db_handler.create_organisation(
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
            expected_response=created_1.as_dict(),
            )
        
        created_2 = db_handler.create_organisation(
            name="Test Organ #1",
            logo_path="ExampleLogo.png")
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_2.id,
            expected_response=1,
            )
                
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------
class Test__Project:
    """!
    Class for testing the Project database handler methods
    
    """
    
    db_handler = DatabaseHandler(
        logger=logger,
        )
    
    reset_database(db_handler)
    
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
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__duplicate_project_code_1(self=None):
        """!
        Duplicate project code, name and organisation
        
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
    
        retrieved_1 = db_handler.get_project(
            name="Test Proj #1",
            )
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=1,
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
        
        created_2 = db_handler.create_project(
            name="Test Proj #1",
            code="XXX_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
                
        MiscTest.process_returns(
            test_no=test, 
            result=created_2.id,
            expected_response=1,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__duplicate_project_code_2(self=None):
        """!
        Duplicate project code and organisation, disparate name
        
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
    
        retrieved_1 = db_handler.get_project(
            name="Test Proj #1",
            )
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=1,
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
        
        created_2 = db_handler.create_project(
            name="Test Proj #2",
            code="XXX_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
                
        MiscTest.process_returns(
            test_no=test, 
            result=created_2,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__duplicate_project_code_3(self=None):
        """!
        Duplicate project code and name, disparate organisation
        
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
        
        _ = db_handler.create_organisation(
            name="Test Organ Name #2",
            logo_path="ExampleLogo.png")
        
        _ = db_handler.create_project(
            name="Test Proj #1",
            code="XXX_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
    
        retrieved_1 = db_handler.get_project(
            name="Test Proj #1",
            )
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=1,
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
        
        created_2 = db_handler.create_project(
            name="Test Proj #1",
            code="XXX_",
            organisation_name="Test Organ Name #2",
            description="blah blah",
            )
                
        MiscTest.process_returns(
            test_no=test, 
            result=created_2,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__invalid_organisation(self=None):
        """!
        Invalid organisation name supplied
        
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
            organisation_name="Test Organ Name #2",
            description="blah blah",
            )
    
        retrieved_1 = db_handler.get_project(
            name="Test Proj #1",
            )
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=0,
            )
                
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__duplicate_names_different_codes(self=None):
        """!
        Duplicate project names, different project codes
        
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
        
        created_1 = db_handler.create_project(
            name="Test Proj #1",
            code="XXX_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
    
        retrieved_1 = db_handler.get_project(
            name="Test Proj #1",
            )
        
        created_2 = db_handler.create_project(
            name="Test Proj #1",
            code="XXY_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
    
        retrieved_2 = db_handler.get_project(
            name="Test Proj #1",
            )
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_2),
            expected_response=2,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved_2[0].as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved_2[1].as_dict(),
            expected_response=created_2.as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    

# -----------------------------------------------------------------------------
class Test__Task:
    """!
    Class for testing the Task database handler methods
    
    """
    
    db_handler = DatabaseHandler(
        logger=logger,
        )
    
    reset_database(db_handler)
    
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_project_by_code(self=None):
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
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_project_by_id(self=None):
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
                
        created_proj = db_handler.create_project(
            name="Test Proj #1",
            code="XXX_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
        
        created_ = db_handler.create_task(
            name="Test Task #1",
            project_id=created_proj.id,
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
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_project_by_name(self=None):
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
            project_name="Test Proj #1",
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
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_with_precedent_task(self=None):
        """!
        Testing simple task with a precedent
        
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
        
        created_1 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_1 = db_handler.get_task(
            id=created_1.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=1,
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_1[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        created_2 = db_handler.create_task(
            name="Test Task #2",
            project_code="XXX_",
            precedent_task_ids=[created_1.id,],
            )
        
        retrieved_2 = db_handler.get_task(
            id=created_2.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_2),
            expected_response=1,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_with_precedent_task_and_taskitems(self=None):
        """!
        Testing simple task with precedent task and task items
        
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
        
        created_1 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_1 = db_handler.get_task(
            id=created_1.id,
            )
        
        _ = db_handler.create_taskitem(
            task_id=created_1.id,
            name="Test TaskItem #1",
            duration_hrs=40,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=1,
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_1[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        created_2 = db_handler.create_task(
            name="Test Task #2",
            project_code="XXX_",
            precedent_task_ids=[created_1.id,],
            )
        
        retrieved_2 = db_handler.get_task(
            id=created_2.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_2),
            expected_response=1,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__wrong_project_code(self=None):
        """!
        Testing attempted creation with wrong project code
        
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
            project_code="XXY_",
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__wrong_project_name(self=None):
        """!
        Testing attempted creation with wrong project name
        
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
            project_name="Test Proj #2",
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__wrong_project_id(self=None):
        """!
        Testing attempted creation with wrong project id
        
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
            project_id=2,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__conflicting_project_code_name(self=None):
        """!
        Testing attempted creation with conflicting project code & names
        
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
        
        _ = db_handler.create_project(
            name="Test Proj #2",
            code="XXY_",
            organisation_name="Test Organ Name #1",
            description="blah blah",
            )
        
        created_ = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            project_name="Test Proj #2",
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_with_invalid_precedent_id(self=None):
        """!
        Testing simple task with an invalid precedent by id
        
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
        
        created_1 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_1 = db_handler.get_task(
            id=created_1.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=1,
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_1[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        created_2 = db_handler.create_task(
            name="Test Task #2",
            project_code="XXX_",
            precedent_task_ids=[2,],
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_2,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_with_invalid_precedent_name(self=None):
        """!
        Testing simple task with an invalid precedent by name
        
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
        
        created_1 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_1 = db_handler.get_task(
            id=created_1.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=1,
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_1[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        created_2 = db_handler.create_task(
            name="Test Task #2",
            project_code="XXX_",
            precedent_task_names=["Test Task #2"],
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_2,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_with_duplicate_precedent_hybrid_id_name(self=None):
        """!
        Testing simple task with a predecent specified by both name and id
        
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
        
        created_1 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_1 = db_handler.get_task(
            id=created_1.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_1),
            expected_response=1,
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_1[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        created_2 = db_handler.create_task(
            name="Test Task #2",
            project_code="XXX_",
            precedent_task_names=["Test Task #1"],
            precedent_task_ids=[1,],
            )
        
        retrieved_2 = db_handler.get_task(
            id=created_2.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_2.as_dict(),
            expected_response=retrieved_2[0].as_dict(),
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_with_precedent_task_invalid_taskitem_id(self = None):
        """!
        Testing simple task with precedent task and invalid task item id
        
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
        
        created_1 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_1 = db_handler.get_task(
            id=created_1.id,
            )
        
        _ = db_handler.create_taskitem(
            task_id=created_1.id,
            name="Test TaskItem #1",
            duration_hrs=40,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_1.as_dict(),
            expected_response=retrieved_1[0].as_dict(),
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_1[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        created_2 = db_handler.create_task(
            name="Test Task #2",
            project_code="XXX_",
            precedent_task_ids=[5,],
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_2,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_with_precedent_task_invalid_taskitem_nm(self = None):
        """!
        Testing simple task with precedent task and invalid task item name
        
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
        
        created_1 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_1 = db_handler.get_task(
            id=created_1.id,
            )
        
        _ = db_handler.create_taskitem(
            task_id=created_1.id,
            name="Test TaskItem #1",
            duration_hrs=40,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_1.as_dict(),
            expected_response=retrieved_1[0].as_dict(),
            )
        
        if len(retrieved_1) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        retrieved = retrieved_1[0]
        MiscTest.process_returns(
            test_no=test, 
            result=retrieved.as_dict(),
            expected_response=created_1.as_dict(),
            )
        
        created_2 = db_handler.create_task(
            name="Test Task #2",
            project_code="XXX_",
            precedent_task_names=["Test TaskItem #2",],
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=created_2,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()
        
    # -------------------------------------------------------------------------
    # @pytest.mark.skip(reason="Reason not declared - user choice to skip")
    def test__create_task_duplicate_name(self=None):
        """!
        Testing task with duplicate name
        
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
        
        created_1 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        retrieved_ = db_handler.get_task(
            id=created_1.id,
            )
        
        MiscTest.process_returns(
            test_no=test, 
            result=len(retrieved_),
            expected_response=1,
            )
        
        created_2 = db_handler.create_task(
            name="Test Task #1",
            project_code="XXX_",
            )
        
        if len(retrieved_) != 1:
            print("Exiting due to unexpected length of return from "
                  "get_project()")
            reset_database(db_handler)
            MiscTest.demark_test()
            return
                
        MiscTest.process_returns(
            test_no=test, 
            result=created_2,
            expected_response=None,
            )
        
        reset_database(db_handler)
        MiscTest.demark_test()    


# -----------------------------------------------------------------------------
class Test__TaskItem:
    """!
    Class for testing the TaskItem database handler methods
    
    """
    
    db_handler = DatabaseHandler(
        logger=logger,
        )
    
    reset_database(db_handler)
    
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
    # Test__Organisation().test__duplicate_organisation()
    
    # Test__HumanResource().test__create_human_resource()
    # Test__HumanResource().test__non_unique_email()
    # Test__HumanResource().test__below_min_hrs()
    # Test__HumanResource().test__at_min_hrs()
    # Test__HumanResource().test__at_max_hrs()
    # Test__HumanResource().test__above_max_hrs()
    # Test__HumanResource().test__unique_emails_different_names()
    
    # Test__Project().test__create_project()
    # Test__Project().test__duplicate_project_code_1()
    # Test__Project().test__duplicate_project_code_2()
    # Test__Project().test__duplicate_project_code_3()
    # Test__Project().test__invalid_organisation()
    # Test__Project().test__duplicate_names_different_codes()
    
    # Test__Task().test__create_task_project_by_code()
    # Test__Task().test__create_task_project_by_id()
    # Test__Task().test__create_task_project_by_name()
    # Test__Task().test__create_task_with_precedent_task()
    # Test__Task().test__create_task_with_precedent_task_and_taskitems()
    # Test__Task.test__wrong_project_code()
    # Test__Task.test__wrong_project_id()
    # Test__Task.test__wrong_project_name()
    # Test__Task.test__conflicting_project_code_name()
    # Test__Task().test__create_task_with_invalid_precedent_id()
    # Test__Task().test__create_task_with_invalid_precedent_name()
    # Test__Task().test__create_task_with_duplicate_precedent_hybrid_id_name()
    # Test__Task().test__create_task_with_precedent_task_invalid_taskitem_id()
    # Test__Task().test__create_task_with_precedent_task_invalid_taskitem_nm()
    
    # Test__TaskItem.test__create_task_item()
    