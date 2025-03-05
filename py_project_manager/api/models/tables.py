# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:18:59 2025

@author: brendan

This module outlines the tables within the sqlite database that provides 
persistent data

Thoughts: Do I need to actively track dependents? Can I leave precedents as the
single point of truth? The calculation of Critical Path will require knowing 
the dependents, but am I better building that dynamically at that point?

Yeah, will do that, and take advantage of reduced db complexity to add 
precedent task items to a task as well to allow better fidelity contruction of 
critical path.

"""
# %% Global imports
from pathlib import Path
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase

import pyjson5

# %% py_project_manager imports
from py_project_manager.lib.logging_config import Logger

from py_project_manager.config import Config


# %% Module level configuration

# declarative base class
class Base(DeclarativeBase):
    pass

log_name = f"{Path(__file__).stem}"
logger_ = Logger(logger_name=log_name,
                log_file=Path(Config.LOG_DIR,
                              f"{log_name}.log"),
                log_level="DEBUG",
                )
logger = logger_.get_logger()


# %% Classes (objects)


# -----------------------------------------------------------------------------
class HumanResource(Base):
    """!
    A human resource is a person that will perform Tasks / TaskItems
    
    """
    
    __tablename__ = "human_resources"
    
    id: int = Column(Integer, primary_key=True)
    
    forename: str = Column(String)
    surname: str = Column(String)
    email: str = Column(String)
    division: str = Column(String)
    working_week_hrs: float = Column(Float)
    
    # -------------------------------------------------------------------------
    def __init__(self, *,
                 id: int = None,
                 forename: str,
                 surname: str,
                 email: str,
                 division: str,
                 working_week_hrs: float,
                 ):
        self.id = id
        self.forename = forename
        self.surname = surname
        self.email = email
        self.division = division
        self.working_week_hrs = working_week_hrs
    
    # -------------------------------------------------------------------------
    def as_dict(self):
        return {"id": self.id,
                "forename": self.forename,
                "surname": self.surname,
                "email": self.email,
                "division": self.division,
                "working_week_hrs": self.working_week_hrs,
                }


# -----------------------------------------------------------------------------
class Organisation(Base):
    """!
    The organisation is a hub for Projects and Resources
    
    """
    
    __tablename__ = "organisations"
    
    id: int = Column(Integer, primary_key=True)
    
    name: str = Column(String)
    logo_path: str = Column(String, nullable = True)
    
    # -------------------------------------------------------------------------
    def __init__(self, *,
                 id: int = None,
                 name: str,
                 logo_path: str,
                 ):
        self.id = id
        self.name = name
        self.logo_path = logo_path
    
    # -------------------------------------------------------------------------
    def as_dict(self):
        return {"id": self.id,
                "name": self.name,
                "logo_path": self.logo_path,
                }


# -----------------------------------------------------------------------------
class Project(Base):
    """!
    A Project will consist of Tasks that are performed by Resources
    
    """
    
    __tablename__ = "projects"
    
    id: int = Column(Integer, primary_key=True)
    
    name: str = Column(String)
    code: str = Column(String)
    organisation_id: int = Column(Integer)  # Could make this a foreign key
    description: str = Column(String)
    
    # -------------------------------------------------------------------------
    def __init__(self, *,
                 id: int = None,
                 name: str,
                 code: str,
                 organisation_id: int,
                 description: str,
                 ):
        self.id = id
        self.name = name
        self.code = code
        self.organisation_id = organisation_id
        self.description = description
    
    # -------------------------------------------------------------------------
    def as_dict(self):
        return {"id": self.id,
                "name": self.name,
                "code": self.code,
                "organisation_id": self.organisation_id,
                "description": self.description,
                }
    

# -----------------------------------------------------------------------------
class Task(Base):
    """!
    A task is a piece of work within a project that will consist of TaskItems
    
    """
    
    __tablename__ = "task"
    
    id: int = Column(Integer, primary_key=True)
    
    name: str = Column(String)
    project_id: int = Column(Integer)  # Could make this a foreign key
    precedent_task_ids: str = Column(String, nullable=True)  
    # Will be a json packed list
    
    # Could also have task items here - for instances where a task can commence
    # part way through a related task?
    precedent_taskitem_ids: str = Column(String, nullable=True)  
    # Will be a json packed list
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, *,
                 id: int = None,
                 name: str,
                 project_id: int,
                 precedent_task_ids: str,
                 precedent_taskitem_ids: str,
                 ):
        """!
        **Instantiate the object**
        
        """
        self.id = id        
        self.name = name
        self.project_id = project_id
        self.precedent_task_ids = precedent_task_ids
        self.precedent_taskitem_ids = precedent_taskitem_ids
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_precedent_taskitem_id(self, id_to_add: int) -> bool:
        """!
        **Add a precedent TaskItem id to the TaskItem**
        
        @param [in] id_to_add [int]
        
        @return [bool] True if successfully added
        
        """
        if not isinstance(id_to_add, int):
            logger.error(
                f"Request to add task item id {id_to_add} to {self.name} as a "
                "precedent abandoned as supplied entry is not an 'int'")
            return False
        
        if id_to_add in self.get_precedent_taskitem_ids():
            logger.error(
                f"Request to add task item id {id_to_add} to {self.name} as a "
                "precedent abandoned as it is already a precedent")
            return False
        
        precedent_ids = self.get_precedent_taskitem_ids()
        precedent_ids.append(id_to_add)
        
        self.precedent_taskitem_ids = pyjson5.encode(sorted(precedent_ids))
        
        return id_to_add in self.get_precedent_taskitem_ids()
    
    # -------------------------------------------------------------------------
    def as_dict(self):
        return {"id": self.id,
                "name": self.name,
                "project_id": self.project_id,
                "precedent_task_ids": self.precedent_task_ids,
                "precedent_taskitem_ids": self.precedent_taskitem_ids,
                }
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def delete_precedent_taskitem_id(self, id_to_delete: int) -> bool:
        """!
        **Delete a precedent TaskItem id from the TaskItem**
        
        @param [in] id_to_delete [int]
        
        @return [bool] True if successfully deleted
        
        """
        if not isinstance(id_to_delete, int):
            logger.error(
                f"Request to delete task id {id_to_delete} from {self.name} "
                "dependents abandoned as supplied entry is not an 'int'")
            return False
        
        if id_to_delete not in self.get_precedent_taskitem_ids():
            logger.error(
                f"Request to delete task id {id_to_delete} from {self.name} "
                "precedents abandoned as it does not exist in precedents")
            return False
        
        precedent_ids = self.get_precedent_taskitem_ids()
        precedent_ids = [i for i in precedent_ids if i != id_to_delete]
        
        self.precedent_taskitem_ids = pyjson5.encode(sorted(precedent_ids))
        
        return id_to_delete not in self.get_precedent_taskitem_ids()
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_precedent_taskitem_ids(self) -> list:
        """!
        **Return the precedent ids as a list**
        
        @return [list]
        
        """
        return pyjson5.decode(self.precedent_taskitem_ids)
    
    
# -----------------------------------------------------------------------------
class TaskItem(Base):
    """!
    A task item is a piece of work within a task and is performed by a Resource
    
    """
    
    __tablename__ = "task_item"
    
    id: int = Column(Integer, primary_key=True)
    
    name: str = Column(String)
    duration_hrs: int = Column(Integer)
    progress_percent: float = Column(Float, nullable=True)
    task_id: int = Column(Integer)
    human_resource_id: int = Column(Integer, nullable=True)
    precedent_taskitem_ids: str = Column(String, nullable=True)  
    # Will be a json packed list
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, *,
                 id: int = None,
                 name: str,
                 duration_hrs: int,
                 progress_percent: float = None,
                 task_id: int,
                 human_resource_id: int = None,
                 precedent_taskitem_ids: str = None,
                 ):
        """!
        **Instantiate the object**
        
        """
        self.id = id  # TODO: Check this performs as expected!
        self.name = name
        self.duration_hrs = duration_hrs
        self.progress_percent = progress_percent
        self.task_id = task_id
        self.human_resource_id = human_resource_id
        self.precedent_taskitem_ids = precedent_taskitem_ids
                
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_precedent_taskitem_id(self, id_to_add: int) -> bool:
        """!
        **Add a precedent TaskItem id to the TaskItem**
        
        @param [in] id_to_add [int]
        
        @return [bool] True if successfully added
        
        """
        if not isinstance(id_to_add, int):
            logger.error(
                f"Request to add task item id {id_to_add} to {self.name} as a "
                "precedent abandoned as supplied entry is not an 'int'")
            return False
        
        if id_to_add in self.get_precedent_taskitem_ids():
            logger.error(
                f"Request to add task item id {id_to_add} to {self.name} as a "
                "precedent abandoned as it is already a precedent")
            return False
        
        precedent_ids = self.get_precedent_taskitem_ids()
        precedent_ids.append(id_to_add)
        
        self.precedent_taskitem_ids = pyjson5.encode(sorted(precedent_ids))
        
        return id_to_add in self.get_precedent_taskitem_ids()
    
    # -------------------------------------------------------------------------
    def as_dict(self):
        return {"id": self.id,
                "name": self.name,
                "duration_hrs": self.duration_hrs,
                "progress_percent": self.progress_percent,
                "task_id": self.task_id,
                "human_resource_id": self.human_resource_id,
                "precedent_taskitem_ids": self.precedent_taskitem_ids,
                }
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def delete_precedent_taskitem_id(self, id_to_delete: int) -> bool:
        """!
        **Delete a precedent TaskItem id from the TaskItem**
        
        @param [in] id_to_delete [int]
        
        @return [bool] True if successfully deleted
        
        """
        if not isinstance(id_to_delete, int):
            logger.error(
                f"Request to delete task id {id_to_delete} from {self.name} "
                "dependents abandoned as supplied entry is not an 'int'")
            return False
        
        if id_to_delete not in self.get_precedent_taskitem_ids():
            logger.error(
                f"Request to delete task id {id_to_delete} from {self.name} "
                "precedents abandoned as it does not exist in precedents")
            return False
        
        precedent_ids = self.get_precedent_taskitem_ids()
        precedent_ids = [i for i in precedent_ids if i != id_to_delete]
        
        self.precedent_taskitem_ids = pyjson5.encode(sorted(precedent_ids))
        
        return id_to_delete not in self.get_precedent_taskitem_ids()
            
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_precedent_taskitem_ids(self) -> list:
        """!
        **Return the precedent ids as a list**
        
        @return [list]
        
        """
        return pyjson5.decode(self.precedent_taskitem_ids)
    
    
    
        