# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:37:51 2025

@author: brendan


This module is a singluar route to the database for all consumers. This
abstracts all other code from the database.

"""
# TODO - need to add exceptions handler for operating behind a REST API

# %% Global imports
from collections.abc import Callable
from sqlalchemy.orm import sessionmaker

import sqlalchemy as db

# %% py_project_manager imports
from py_project_manager.config import Config

from py_project_manager.lib.logging_config import Logger

from py_project_manager.api.models.tables import (
    HumanResource,
    Organisation,
    Project,
    Task,
    TaskItem,
    )

# %% Module Config

# %% Functions

# %% Classes

# -------------------------------------------------------------------------
class DatabaseHandler:
    """!
    Handler for all database transactions
    
    """
    table_objects = [
        HumanResource,
        Organisation,
        Project,
        Task,
        TaskItem,
        ]
    
    # -------------------------------------------------------------------------
    def __init__(self, *,
                 logger: Callable,
                 ):
        """!
        **Instantiate the class**
        
        @param [in] logger [Callable] handle to the logger instance of the 
            calling module/class/method
    
        """
        self.logger = logger
        
        db_ = Config.DATABASE
        self.engine = db.create_engine(db_)
        self.conn = self.engine.connect()
        
        self.__create_tables()
        
    # -------------------------------------------------------------------------
    def __create_tables(self):
        """!
        **Create tables as required**

        This should only be needed at very first run. Otherwise tables should
        exist. Thus fire warnings for every table creation event.

        """
        for table_object in __class__.table_objects:
            table_name = table_object.__tablename__
            table_exist = \
                db.inspect(self.engine).has_table(table_name)

            if not table_exist:
                self.logger.warning(
                    f"The table ({table_name}) corresponding to object "
                    f"{table_object} doesn't exist, attempting to create")
                try:
                    table_object.__table__.create(
                        bind=self.engine,
                        checkfirst=True,
                        )
                except Exception as exception:
                    self.logger.error(
                        f"Unable to create {table_name} for object "
                        f"{table_object} due to {exception}"
                        )
    
    # -------------------------------------------------------------------------
    def create_organisation(self, *,
                            name: str,
                            logo_path: str = None,
                            ) -> Organisation:
        """!
        **Create an organisation**
        
        @param [in] name [str]
        @param [in] logo_path [str] Optional path to a logo file for display on
            GUI
        
        @return [Organisation]
        
        """
        # First, check does the organisation exist already
        organ_rtns = self.get_organisation(
            name=name)
        
        if organ_rtns:
            self.logger.warning(
                f"An organisation with name {name} already exists, cannot add "
                "another")
            if len(organ_rtns) > 1:
                # WTF - shouldn't be here
                self.logger.critical(
                    f"Duplicates exist for organisation name {name} - how??? "
                    " This will break code")
                return {}
            else:
                return organ_rtns[0]
        
        new_organisation = Organisation(
            **{"name": name,
               "logo_path": logo_path,
               })
        
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            session.add(new_organisation)
            session.commit()
        
        organ_rtns = self.get_organisation(
            name=name)
        return organ_rtns[0]
        
    # -------------------------------------------------------------------------
    def create_project(self, *,
                       name: str,
                       code: str,
                       organisation_name: str,
                       description: str,
                       ) -> Project:
        """!
        **Create a project**
        
        @param [in] name [str]
        @param [in] code [str]
        @param [in] organisation_name [str]
        @param [in] description [str]
        
        @return [Project] The entered (or retrieved if duplicate) object
        
        """
        # First, check does the code already exist - codes should be unique
        code_rtns = self.get_project(
            code=code,
            )
        if code_rtns:
            self.logger.warning(
                "A project already exists for that code, cannot add another")
            if len(code_rtns) > 1:
                # WTF - shouldn't be here
                self.logger.critical(
                    f"Duplicates exist for project code {code} - how??? "
                    " This will break code")
                return {}
            else:
                return code_rtns[0]
        
        # Check does the organisation name exist
        organ_rtns = self.get_organisation(
            name=name,
            )
        
        if not organ_rtns:
            self.logger.error(
                f"No organisation exists for name: {organisation_name}, "
                "cannot create project")
            return {}
        if len(organ_rtns) > 1:
            self.logger.critical(
                f"The organisation name ({organisation_name}) is not unique, "
                "cannot proceed to create a project")
            return {}
        organisation_id = organ_rtns[0]["id"]
        
        # Then check does the project name already exist - duplicate names may 
        # exist with separate codes, but it is a warning scenario incase of 
        # input error
        name_rtns = self.get_project(
            name=name,
            )
        if name_rtns:
            self.logger.warning(
                "The following project codes already have a project name of "
                f"{name}: {', '.join([i['name'] for i in name_rtns])}. Will "
                "continue to create the project.")
            
        new_project = Project(
            **{"name": name,
               "code": code,
               "organisation_id": organisation_id,
               "description": description,
               })
        
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            session.add(new_project)
            session.commit()
            
        proj_rtns = self.get_project(
            name=name,
            code=code,
            )
        return proj_rtns[0]
    
    # -------------------------------------------------------------------------
    def get_organisation(self, *,
                         name: str = None,
                         logo_path: str = None,
                         ) -> list:
        """!
        **Get an organisation from the DB given description provided**
        
        @param [in] name [str]
        @param [in] logo_path [str]
        
        @return [list]
        
        """
        # TODO - rework this with the optional list searching approach
        # TODO - should I return objects, or convert to dictionary?
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            rtn = session.query(
                Organisation).filter(
                    Organisation.name==name, 
                    Organisation.code==logo_path, 
                    ).all()
        return rtn
        
    # -------------------------------------------------------------------------
    def get_project(self, *, 
                    name: str = None,
                    code: str = None,
                    organisation_name: str = None,
                    description: str = None,
                    ) -> list:
        """!
        **Get a project from the DB given the description provided**
        
        @param [in] name [str]
        @param [in] code [str]
        @param [in] organisation_name [str]
        @param [in] description [str]
        
        @return [list]
        
        """
        # TODO - rework this with the optional list searching approach
        # TODO - should I return objects, or convert to dictionary?
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            rtn = session.query(
                Project).filter(
                    Project.name==name, 
                    Project.code==code, 
                    Project.organisation_name==organisation_name,
                    Project.description==description,
                    ).all()
        return rtn
        
        
                           