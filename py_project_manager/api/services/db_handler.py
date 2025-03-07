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
from typing import Union

import pyjson5
import sqlalchemy as db

# %% py_project_manager imports
from py_project_manager.config import Config

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


# TODO - move this to separate module
from sqlalchemy.exc import OperationalError, StatementError
from sqlalchemy.orm.query import Query as _Query
from time import sleep


# -----------------------------------------------------------------------------
class RetryingQuery(_Query):
    __max_retry_count = 3
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __iter__(self):
        attempts = 0
        
        while True:
            attempts += 1
            
            try: 
                return super().__iter__()
            except OperationalError as exception:
                if ("server closed the connection unexpectedly" 
                        not in str(exception)):
                    raise
                
                if attempts <= self.__max_retry_count__:
                    sleep_for = 2 ** (attempts - 1)
                    print(
                        "Database connection error: retrying Strategy => "
                        f"sleeping for {sleep_for} s and will retry "
                        f"(attempt #{attempts} of {self.__max_retry_count})"
                        f"\nDetailed query impacted: {exception}")
                    sleep(sleep_for)
                    continue
                else:
                    raise
                    
            except StatementError as exception:
                if ("reconnect until invalid transaction is rolled back" 
                        not in str(exception)):
                    raise
                self.sesson.rollback()


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
                 warning_on_table_creation: bool = False,
                 ):
        """!
        **Instantiate the class**
        
        @param [in] logger [Callable] handle to the logger instance of the 
            calling module/class/method
        @param [in] warning_on_table_creation [bool] True to make a logger 
            warning entry on table creation
    
        """
        self.logger = logger
        self.warning_on_table_creation = warning_on_table_creation
        
        db_ = Config.DATABASE
        self.engine = db.create_engine(db_)
        self.conn = self.engine.connect()
        
        self.__create_tables()
    
    # -------------------------------------------------------------------------
    def __check_duration_hrs_validity(self,
                                      duration_hrs: int
                                      ) -> int:
        # TODO - add check logic
        return duration_hrs
        
    # -------------------------------------------------------------------------
    def __check_progress_percent_validity(self, 
                                          progress_percent: float
                                          ) -> float:
        # TODO - add check logic
        return progress_percent
        
    # -------------------------------------------------------------------------
    def __check_task_precedents(self, 
                                precedent_task_ids: list[int] = None,
                                precedent_task_names: list[str] = None,
                                ) -> Union[list[int], None]:
        """!
        **Check are the supplied task identifiers valid**
        
        Ensuring all id and names actually exist
        
        @param [in] precedent_task_ids [list[int]]
        @param [in] precedent_task_names [list[str]]
        
        @return [list[int], None
        
        """
        if (not precedent_task_ids
                and not precedent_task_names):
            msg = ("No valid 'precedent_task_ids' or 'precedent_task_names' "
                   "supplied")
            self.logger.error(msg)
            return []
        
        all_task_ids = []
        
        n_precedent_task_ids = 0
        n_precedent_task_names = 0
        
        if precedent_task_ids:
            if isinstance(precedent_task_ids, int):
                precedent_task_ids = [precedent_task_ids]
            
            n_precedent_task_ids = len(precedent_task_ids)
            for id_ in precedent_task_ids:
                if not self.get_task(
                        id=id_,
                        ):
                    msg = (f"Invalid task id: {id_} supplied")
                    self.logger.error(msg)
                    return []
                all_task_ids.append(id_)
        
        if precedent_task_names:
            if isinstance(precedent_task_names, str):
                precedent_task_names = [precedent_task_names]
                
            n_precedent_task_names = len(precedent_task_names)
            for name_ in precedent_task_names:
                if not (tasks_ := self.get_task(
                        name=name_,
                        )):
                    msg = (f"Invalid task name: {name_} supplied, doesn't " 
                           "exist")
                    self.logger.error(msg)
                    return []
                if len(tasks_) > 1:
                    msg = (f"Ambiguous task name: {name_} supplied, returned "
                           f"{len(tasks_)}, cannot continue")
                    self.logger.error(msg)
                    return []
                all_task_ids.append(tasks_[0].id)
        
        all_task_ids_ = sorted(list(set(all_task_ids)))
        
        if len(all_task_ids_) < (n_precedent_task_ids
                                 + n_precedent_task_names):
            msg = ("The valid task ids are less than supplied ids and names, "
                   "this may be due to duplicates")
            self.logger.warning(msg)
            
        return all_task_ids_
    
    # -------------------------------------------------------------------------
    def __check_taskitem_precedents(self, 
                                precedent_taskitem_ids: list[int] = None,
                                precedent_taskitem_names: list[str] = None,
                                ) -> Union[list[int], None]:
        """!
        **Check are the supplied taskitem identifiers valid**
        
        Ensuring all id and names actually exist
        
        @param [in] precedent_taskitem_ids [list[int]]
        @param [in] precedent_taskitem_names [list[str]]
        
        @return [list[int], None
        
        """
        if (not precedent_taskitem_ids
                and not precedent_taskitem_names):
            msg = ("No valid 'precedent_taskitem_ids' or "
                   "'precedent_taskitem_names' supplied")
            self.logger.error(msg)
            return []
        
        all_taskitems_ids = []
        
        if precedent_taskitem_ids:
            for id_ in precedent_taskitem_ids:
                if not self.get_taskitem(
                        id=id_,
                        ):
                    msg = (f"Invalid taskitem id: {id_} supplied")
                    self.logger.error(msg)
                    return []
                all_taskitems_ids.append(id_)
        
        if precedent_taskitem_names:
            for name_ in precedent_taskitem_names:
                if not (tasks_ := self.get_taskitem(
                        name=name_,
                        )):
                    msg = (f"Invalid taskitem name: {name_} supplied, doesn't " 
                           "exist")
                    self.logger.error(msg)
                    return []
                if len(tasks_) > 1:
                    msg = (f"Ambiguous taskitem name: {name_} supplied, "
                           f"returned {len(tasks_)}, cannot continue")
                    self.logger.error(msg)
                    return []
                all_taskitems_ids.append(tasks_[0].id)
        
        all_taskitems_ids_ = sorted(list(set(all_taskitems_ids)))
        
        if len(all_taskitems_ids_) < (len(precedent_taskitem_ids)
                                 + len(precedent_taskitem_names)):
            msg = ("The valid taskitem ids are less than supplied ids and "
                   "names, this may be due to duplicates")
            self.logger.warning(msg)
            
        return all_taskitems_ids_
        
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
                if self.warning_on_table_creation:
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
    def __create_task(self, 
                      name: str,
                      project_id: int,
                      precedent_task_ids: list[int],
                      precedent_taskitem_ids: list[int],
                      ) -> Task:
        """!
        **Create a task object and submit to DB**
        
        @param [in] name [str]
        @param [in] project_id [int]
        @param [in] precedent_task_ids [list[int]]
        @param [in] precedent_taskitem_ids [list[int]]
        
        @return [Task]
        
        """
        precedent_task_ids_ = pyjson5.encode(precedent_task_ids)
        precedent_taskitem_ids_ = pyjson5.encode(precedent_taskitem_ids)
        new_task = Task(
            **{"name": name,
               "project_id": project_id,
               "precedent_task_ids": precedent_task_ids_,
               "precedent_taskitem_ids": precedent_taskitem_ids_
               })
        
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            session.add(new_task)
            session.commit()
        
        task_rtns = self.get_task(
            name=name,
            project_id=project_id,
            )
        return task_rtns[0]
    
    # -------------------------------------------------------------------------
    def __create_taskitem(self, 
                          name: str,
                          duration_hrs: int,
                          progress_percent: float,
                          task_id: int,
                          human_resource_id: int,
                          precedent_taskitem_ids: list,
                          ):
        """!
        **Create a taskitem object and submit to DB**
        
        @param [in] name [str]
        @param [in] duration_hrs [int]
        @param [in] progress_percent [float]
        @param [in] task_id [int]
        @param [in] human_resource_id [int]
        @param [in] precedent_taskitem_ids [list[int]]
        
        @return [TaskItem]
        
        """
        precedent_taskitem_ids_ = pyjson5.encode(precedent_taskitem_ids)
        new_taskitem = TaskItem(
            **{"name": name,
               "duration_hrs": duration_hrs,
               "progress_percent": progress_percent,
               "task_id": task_id,
               "human_resource_id": human_resource_id,
               "precedent_taskitem_ids": precedent_taskitem_ids_,
               
               })
        
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            session.add(new_taskitem)
            session.commit()
        
        taskitem_rtns = self.get_taskitem(
            name=name,
            task_id=task_id,
            )
        return taskitem_rtns[0]
    
    # -------------------------------------------------------------------------
    def __get_unique_human_resource_id(self,
                                       human_resource_id: int = None,
                                       human_resource_email: str = None,
                                       ) -> Union[int, None]:
        """!
        **Get a unique human resource ID given the descriptions provided**
        
        Serves as a check for potential multiple source entries for a project
        identifier
        
        @param [in] human_resource_id [int]
        @param [in] human_resource_email [str]
        
        @return [int, None]
        
        """
        if (not human_resource_id
                and not human_resource_email):
            msg = ("At least one of 'human_resource_id' or "
                   "'human_resource_email' must be supplied")
            self.logger.error(msg)
            return None
        
        hr_id_rtns = []
        if human_resource_id:
            temp = self.get_human_resource(id=human_resource_id)
            if temp:
                hr_id_rtns.append(temp[0].id)
                # The resource id is unique, so will always be at most 1 
                # return
            else:
                msg = ("A human resource id has been specified "
                       f"({human_resource_id}), but it does not exist")
                self.logger.error(msg)
                return None
            
        if human_resource_email:
            temp = self.get_human_resource(email=human_resource_email)
            if temp:
                hr_id_rtns.append(temp[0].id)
                # The resource id is unique, so will always be at most 1 
                # return
            else:
                msg = ("A human resource email has been specified "
                       f"({human_resource_email}), but it does not exist")
                self.logger.error(msg)
                return None    
            
        if len(set(hr_id_rtns)) > 1:
            msg = ("Ambiguous human resource descriptors provided, there are "
                   f"{len(set(hr_id_rtns))} human resources identified")
            return None
        elif len(set(hr_id_rtns)) == 0:
            msg = ("Invalid human resource descriptors provided, no associated"
                   " resources have been identified")
            return None
        
        return hr_id_rtns[0]
             
    # -------------------------------------------------------------------------
    def __get_unique_project_id(self, 
                                project_code: str = None,
                                project_id: int = None,
                                project_name: str = None,
                                ) -> Union[int, None]:
        """!
        **Get a unqiue project ID given the descriptions provided**
        
        Serves as a check for potential multiple source entries for a project
        identifier
        
        @param [in] project_code [str] Optionally supply the code of the 
            project holding the task
        @param [in] project_id [int] Optionally supply the id of the project
            holding the task
        @param [in] project_name [str] Optionally supply the name of the 
            project (as long as its unique) holding the task
        
        At least one valid project_code, project_id or project_name must be
        provided. If two or more are provided, a conflict check is performed.
        A provided project_name must be unique.
        
        @return [int, None]
        
        """
        if (not project_code
                and not project_id
                and not project_name):
            msg = ("At least one entry for 'project_code', 'project_id' or "
                   "'project_name' must be supplied")
            self.logger.error(msg)
            return None
        
        project_id_rtns = []
        if project_code:
            temp = self.get_project(code=project_code)
            if temp:
                project_id_rtns.append(temp[0].id)
                # The project code is unique, so will always be at most 1 
                # return
            else:
                msg = (f"A project code has been specified ({project_code}), "
                       "but it does not exist")
                self.logger.error(msg)
                return None
        
        if project_id:
            temp = self.get_project(id=project_id)
            if temp:
                project_id_rtns.append(temp[0].id)
                # The project id will be unique, so will always be at most 1 
                # return
            else:
                msg = (f"A project id has been specified ({project_id}), "
                       "but it does not exist")
                self.logger.error(msg)
                return None
        
    
        if project_name:
            temp = self.get_project(name=project_name)
            if len(temp) != 1:
                msg = (f"The supplied project name: {project_name} yielded "
                       f"{len(temp)} projects, these being (by code): "
                       f"{', '.join([i.code for i in temp])}")
                self.logger.error(msg)
                return None
            project_id_rtns.append(temp[0].id)
        
        if len(set(project_id_rtns)) > 1:
            msg = ("Ambiguous project descriptors provided, there are "
                   f"{len(set(project_id_rtns))} projects identified")
            return None
        elif len(set(project_id_rtns)) == 0:
            msg = ("Invalid project descriptors provided, no associated "
                   "projects have been identified")
            return None
        
        return project_id_rtns[0]
    
    # -------------------------------------------------------------------------
    def __get_unique_task_id(self, 
                             task_id: int = None,
                             project_code: str = None,
                             task_name: str = None,
                             ) -> Union[int, None]:
        """!
        **Get a unique task id given the description provided**
        
        @param [in] task_id [int] 
        @param [in] project_code [str]
        @param [in] task_name [str]
        
        At least one valid task_id or project_code + task_name must be
        provided. If both are provided, a conflict check is performed.
                
        @return [int, None]
        
        """
        task_id_rtns = []
        if task_id:
            temp = self.get_task(
                id=task_id
                )
            if temp:
                task_id_rtns.append(temp[0].id)                
                # The task id is unique, so will always be at most 1 
                # return
            else:
                msg = (f"A task id has been specified ({task_id}), "
                       "but it does not exist")
                self.logger.error(msg)
                return None
        
        _project_id = None
        if project_code:
            if not task_name:
                msg = (f"A project code ({project_code}) has been specified, "
                       "but no corresponding task name specified")
                self.logger.error(msg)
                return None
            _project_ids = self.get_project(
                code=project_code,
                )
            if not _project_ids:
                msg = (f"A project code ({project_code}) has been specified, "
                       "but it does not exist in the system")
                self.logger.error(msg)
                return None
            _project_id = _project_ids[0]
            # The project code is unique, so will always be at most 1 
            # return
        
        if task_name:
            if not project_code:
                msg = (f"A task name ({task_name}) has been specified, "
                       "but no corresponding project code specified")
                self.logger.error(msg)
                return None
            
        if task_name and project_code:
            temp = self.get_task(
                name=task_name,
                project_id=_project_id,
                )
            if temp:
                task_id_rtns.append(temp[0].id)                
                # The task_name is unique within every project, so will always 
                # be at most 1 return
            else:
                msg = (f"A project code ({project_code}) and task name "
                       f"({task_name}) have been specified, the project exists" 
                       ", but no corresponding task exists")
                self.logger.error(msg)
                return None
            
        if len(set(task_id_rtns)) > 1:
            msg = ("Ambiguous task descriptors provided, there are "
                   f"{len(set(task_id_rtns))} tasks identified")
            return None
        elif len(set(task_id_rtns)) == 0:
            msg = ("Invalid task descriptors provided, no associated tasks "
                   "have been identified")
            return None
        
        return task_id_rtns[0]
    
    # -------------------------------------------------------------------------
    def __run_query(self, *, 
                    obj,
                    kwargs: dict,
                    ) -> list:
        """!
        **Run a read query to the database**
        
        @param [in] obj: The table object being queried
        @param [in] kwargs [dict] The
        
        """        
        filter_ = []
        keys = [i for i in dir(obj)
                if i[:1] != "_"
                and i not in ["metadata", "registry"]]
        
        for key in keys:
            if key in kwargs and kwargs[key]:
                if isinstance(kwargs[key], list):
                    filter_.append(
                        getattr(obj, key).in_(kwargs[key])
                        )
                else:
                    filter_.append(
                        getattr(obj, key) == kwargs[key]
                        )
        
        all_matches = None
        with sessionmaker(bind=self.engine,
                          query_cls=RetryingQuery,
                          expire_on_commit=False,
                          )() as session:
            
            all_matches = session.query(obj).filter(*filter_).all()

        # Can convert to dict using the below
        #all_matches_ = [{k: v for k, v in i.__dict__.items() if k[:1] != "_"}
        #                for i in all_matches]
        
        all_matches_ = sorted(all_matches, key = lambda d: d.id)
        
        return all_matches_
    
    # -------------------------------------------------------------------------
    def create_human_resource(self, *,
                              forename: str,
                              surname: str,
                              email: str,
                              division: str,
                              working_week_hrs: float,
                              ) -> dict:
        """!
        **Create a human resource**
        
        @param [in] forename [str]
        @param [in] surname [str]
        @param [in] email [str] Must be unique
        @param [in] division [str]
        @param [in] working_week_hrs [float] Minimum of 8.0, max of 80.
            Including the max of 80.0 for overtime, but may amend that to a 
            temporary surge option. Maybe move these numbers to a config file
            item?
            
        @return [HumanResource]
        
        """
        # TODO Move week_hrs limits to config file
        
        # Check email doesn't already exist - as its a unique item
        email_check = self.get_human_resource(
            email=email)
        if email_check:
            msg = ("When trying to create a new HumanResource, the supplied "
                   f"email: {email} is not unique, already exists. Cannot "
                   "create new resource and will return nothing")
            self.logger.warning(msg)
            return None
        
        # Check working_week_hrs is >= 8 <= 80
        if working_week_hrs < 8.0:
            msg = (f"Specified weekly working hours ({working_week_hrs}) is "
                   f"too small for user {email}, minimum is 8.0 hrs, setting "
                   "to minimum")
            self.logger.warning(msg)
            working_week_hrs = 8.0
        elif working_week_hrs > 80.0:
            msg = (f"Specified weekly working hours ({working_week_hrs}) is "
                   f"too large for user {email}, maximum is 80.0 hrs, setting "
                   "to maximum")
            self.logger.error(msg)
            working_week_hrs = 80.0
        
        new_human_resource = HumanResource(
            **{"forename": forename,
               "surname": surname,
               "email": email,
               "division": division,
               "working_week_hrs": working_week_hrs,
               })
        
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            session.add(new_human_resource)
            session.commit()
        
        hr_rtns = self.get_human_resource(
            email=email)
        
        return hr_rtns[0]
        
    # -------------------------------------------------------------------------
    def create_organisation(self, *,
                            name: str,
                            logo_path: str = None,
                            ) -> dict:
        """!
        **Create an organisation**
        
        @param [in] name [str]
        @param [in] logo_path [str] Optional path to a logo file for display on
            GUI
        
        @return [dict]
        
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
                return None
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
                       organisation_id: int = None,
                       organisation_name: str = None,
                       description: str,
                       ) -> dict:
        """!
        **Create a project**
        
        @param [in] name [str]
        @param [in] code [str]
        @param [in] organisation_name [str]
        @param [in] description [str]
        
        @return [dict] The entered (or retrieved if duplicate) dict of obj
        
        """
        # Get the organisation id
        if not organisation_id and not organisation_name:
            self.logger.error(
                "Need to supply either 'organisation_name' or "
                "'organisation_id' when attempting to create a project")
            return None
        if not organisation_id:
            rtn_ = self.get_organisation(name=organisation_name)
            if len(rtn_) != 1:
                self.logger.error(
                    f"Invalid organisation name {organisation_name} supplied, "
                    "doesn't exist, cannot create project")
                return None
            organisation_id = rtn_[0].id
        
        # Check does the code already exist - codes should be unique
        code_rtns = self.get_project(
            code=code,
            )
        if code_rtns:
            if len(code_rtns) > 1:
                # WTF - shouldn't be here
                self.logger.critical(
                    f"Duplicates exist for project code {code} - how??? "
                    " This will break code")
                return None
            else:
                rtn = code_rtns[0]
                if (rtn.name == name 
                        and rtn.organisation_id == organisation_id):                      
                    self.logger.warning(
                        "A project already exists for that code, name and " 
                        "organisation, cannot add another")
                    return rtn
                else:
                    other_org_name = self.get_organisation(
                        id=rtn.organisation_id)[0].name
                    
                    self.logger.error(
                        "A project already exists for that code, but with "
                        f"different name: {rtn.name} or different organisation"
                        f" {other_org_name}, not adding")
                    return None
                    
        # Then check does the project name already exist - duplicate names may 
        # exist with separate codes, but it is a warning scenario incase of 
        # input error
        name_rtns = self.get_project(
            name=name,
            )
        if name_rtns:
            self.logger.warning(
                "The following project codes already have a project name of "
                f"{name}: {', '.join([i.name for i in name_rtns])}. Will "
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
    def create_task(self, *,
                    name: str,
                    project_code: str = None,
                    project_id: int = None,
                    project_name: str = None,
                    precedent_task_ids: list[int] = None,
                    precedent_task_names: list[str] = None,
                    precedent_taskitem_ids: list[int] = None,
                    precedent_taskitem_names: list[str] = None,
                    ) -> dict:
        """!
        **Create a task**
        
        @param [in] name [str] The name of this task
        
        @param [in] project_code [str] Optionally supply the code of the 
            project holding the task
        @param [in] project_id [int] Optionally supply the id of the project
            holding the task
        @param [in] project_name [str] Optionally supply the name of the 
            project (as long as its unique) holding the task
        
        At least one valid project_code, project_id or project_name must be
        provided. If two or more are provided, a conflict check is performed.
        A provided project_name must be unique.
        
        @param [in] precedent_task_ids [list[int]] An optional list of 
            precedent task ids
        @param [in] precedent_task_names [list[str]] An optional list of 
            precedent task names
        @param [in] precedent_taskitem_ids [list[int]] An optional list of 
            precedent taskitem ids
        @param [in] precedent_taskitem_names [list[int]] An optional list of 
            precedent taskitem names
        
        Conflict checks will be performed on each precedent item submitted. A
        supplied task or task item as a precedent cannot in turn have this task 
        as a precedent - but since this task has not existed before now, that
        link has not been possible to create so is not checked here.
        
        @return [dict] Of the database entry if successful submission
        
        """
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check the project description provided is unique and valid
        if not (_project_id := self.__get_unique_project_id(
                project_code,
                project_id,
                project_name,
                )):
            msg = ("Unable to create task due to invalid project description "
                   f"provided, check logs. Not creating task: {name} ")
            self.logger.error(msg)
            return None
                
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check the precedent tasks are valid
        _precedent_task_ids = []
        if precedent_task_ids or precedent_task_names:
            if not (_precedent_task_ids := self.__check_task_precedents(
                    precedent_task_ids,
                    precedent_task_names,
                    )):
                msg = ("Unable to create task due to invalid precedent task "
                       "descriptions provided, check logs. Not creating task "
                       f"{name}")
                self.logger.error(msg)
                return None
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check the precedent tasksitems are valid
        _precedent_taskitem_ids = []
        if precedent_taskitem_ids or precedent_taskitem_names:
            if not (_precedent_taskitem_ids := \
                    self.__check_taskitem_precedents(
                        precedent_taskitem_ids,
                        precedent_taskitem_names,
                    )):
                msg = ("Unable to create task due to invalid precedent "
                       "taskitem descriptions provided, check logs. Not "
                       f"creating task {name}")
                self.logger.error(msg)
                return None
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check does the task name already exist within the project
        if (existing_tasks := self.get_task(
                name=name,
                project_id=_project_id,
                )):
            project_ = self.get_project(
                id=existing_tasks[0].project_id)[0]
            
            
            msg = (f"The supplied task {name} already exists for the project "
                   f"{project_.name}, cannot add another task of same name"
                   )
            self.logger.error(msg)
            return None
            
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Create the task       
        return self.__create_task(name,
                                  _project_id,
                                  _precedent_task_ids,
                                  _precedent_taskitem_ids,
                                  )
    
    # -------------------------------------------------------------------------
    def create_taskitem(self, *,
                        name: str,
                        duration_hrs: int,
                        progress_percent: float = 0.0,
                        task_id: int = None,
                        project_code: str = None,
                        task_name: str = None,
                        human_resource_id: int = None,
                        human_resource_email: str = None,
                        precedent_taskitem_ids: list[int] = None,
                        precedent_taskitem_names: list[str] = None,
                        ) -> dict:
        """!
        **Create a TaskItem**
        
        @param [in] name [str]
        @param [in] duration_hrs [int]
        @param [in] progress_percent [float]
        
        @param [in] task_id [int]
        @param [in] project_code [str]
        @param [in] task_name [str]
        
        If task_id is not supplied, then a valid project_code + task_name may
        be used to link the TaskItem to its parent task instead
        
        @param [in] human_resource_id [int] May be null at start
        @param [in] human_resource_email [str] May be null at start
        
        Either of id or email may be used to identify the human resource that 
        is responsible for the TaskItem
        
        @param [in] precedent_taskitem_ids [list[int]]
        @param [in] precedent_taskitem_names [list[str]]
        
        To use precedent_taskitem_names, the project_code must be supplied
        
        @return [dict]
        
        """
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check the task description provided is unique and valid
        if not (_task_id := self.__get_unique_task_id(
                task_id,
                project_code,
                task_name,
                )):
            msg = ("Unable to create taskitem due to invalid task description "
                   "provided, check logs. Not creating taskitem: {name} ")
            self.logger.error(msg)
            return None
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check the human resource description provided is unique and valid
        if not human_resource_id and not human_resource_email:
            msg = ("Creating taskitem without a human resource provided, "
                   "time management capabilities will be limited")
            self.logger.warning(msg)
            _human_resource_id = None
            
        elif not (_human_resource_id := self.__get_unique_human_resource_id(
                human_resource_id,
                human_resource_email,
                )):
            msg = ("An entry for either 'human_resource_id' or "
                   "'human_resource_email' has been provided, but its invalid,"
                   " so not creating TaskItem")
            self.logger.error(msg)
            return None
            
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check the duration_hrs is valid
        if not (_duration_hrs := self.__check_duration_hrs_validity(
                duration_hrs,
                ) is not None):
            msg = ("Unable to create taskitem due to invalid duration in hrs"
                   "provided, check logs. Not creating taskitem: {name} ")
            self.logger.error(msg)
            return None
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check the progress_percent is valid
        if not (_progress_percent := self.__check_progress_percent_validity(
                progress_percent,
                ) is not None):
            msg = ("Unable to create taskitem due to invalid progress "
                   "provided, check logs. Not creating taskitem: {name} ")
            self.logger.error(msg)
            return None
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check the precedent_taskitems are valid
        _precedent_taskitem_ids = []
        if precedent_taskitem_ids or precedent_taskitem_names:
            if not (_precedent_taskitem_ids := \
                    self.__check_taskitem_precedents(
                        precedent_taskitem_ids,
                        precedent_taskitem_names,
                    )):
                msg = ("Unable to create taskitem due to invalid precedent "
                       "taskitem descriptions provided, check logs. Not "
                       f"creating taskitem {name}")
                self.logger.error(msg)
                return None
            
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check does the task item name already exist within the task
        if self.get_taskitem(
                name=name,
                task_id=_task_id,
                ):            
            task_ = self.get_task(
                id=_task_id)[0]
            
            msg = (f"The supplied taskitem {name} already exists for the task "
                   f"{task_.name}, cannot add another task of same name"
                   )
            self.logger.error(msg)
            return None
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Create the taskitem
        return self.__create_taskitem(name,
                                      _duration_hrs,
                                      _progress_percent,
                                      _task_id,
                                      _human_resource_id,
                                      _precedent_taskitem_ids,
                                      )
    
    # -------------------------------------------------------------------------
    def get_human_resource(self, *, 
                           id: int = None,
                           forename: str = None,
                           surname: str = None,
                           email: str = None,
                           division: str = None,
                           working_week_hrs: float = None,
                           ) -> list[dict]:
        """!
        **Get Human Resources from the DB given description provided**
        
        
        @param [in] forename [str]
        @param [in] surname [str]
        @param [in] email [str] 
        @param [in] division [str]
        @param [in] working_week_hrs [float]
        
        @return [list[dict]]
        
        """        
        all_matches = self.__run_query(
            obj=HumanResource,
            kwargs=locals(),
            )
        
        return all_matches
    
    # -------------------------------------------------------------------------
    def get_organisation(self, *,
                         id: int = None,
                         name: str = None,
                         logo_path: str = None,
                         ) -> list[dict]:
        """!
        **Get an organisation from the DB given description provided**
        
        @param [in] name [str]
        @param [in] logo_path [str]
        
        @return [list[dict]]
        
        """
        all_matches = self.__run_query(
            obj=Organisation,
            kwargs=locals(),
            )
        
        return all_matches
        
    # -------------------------------------------------------------------------
    def get_project(self, *, 
                    id: int = None,
                    name: str = None,
                    code: str = None,
                    organisation_name: str = None,
                    description: str = None,
                    ) -> list[dict]:
        """!
        **Get a project from the DB given the description provided**
        
        @param [in] name [str]
        @param [in] code [str]
        @param [in] organisation_name [str]
        @param [in] description [str]
        
        @return [list[dict]]
        
        """
        all_matches = self.__run_query(
            obj=Project,
            kwargs=locals(),
            )
        
        return all_matches
        
    # -------------------------------------------------------------------------
    def get_task(self, *, 
                 id: int = None,
                 name: str = None,
                 project_id: int = None,
                 precedent_task_ids: list[int] = None,
                 precedent_taskitem_ids: list[int] = None,
                 ) -> list[dict]:
        """!
        **Get a task from the DB given the description provided**
        
        @param [in] id [int]
        @param [in] name [str]
        @param [in] project_id [int]
        @param [in] precedent_task_ids [list[int]]
        @param [in] precedent_taskitem_ids [list[int]]
        
        @return [list[dict]]
        
        """
        all_matches = self.__run_query(
            obj=Task,
            kwargs=locals(),
            )
        
        return all_matches
    
    # -------------------------------------------------------------------------
    def get_taskitem(self, *, 
                     id: int = None,
                     name: str = None,
                     duration_hrs: int = None,
                     progress_percent: float = None,
                     task_id: int = None,
                     human_resource_id: int = None,
                     precedent_taskitem_ids: list[int] = None,
                     ) -> list[dict]:
        """!
        **Get a taskitem from the DB given the description provided**
        
        @param [in] id [int]
        @param [in] name [str]
        @param [in] duration_hrs [int]
        @param [in] precedent_task_ids [list[int]]
        @param [in] precedent_taskitem_ids [list[int]]
        
        @return [list[dict]]
        
        """
        all_matches = self.__run_query(
            obj=TaskItem,
            kwargs=locals(),
            )
        
        return all_matches
    