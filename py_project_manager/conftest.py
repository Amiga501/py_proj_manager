# -*- coding: utf-8 -*-
"""
Created on Wed May 14 21:31:51 2025

@author: brend

PyTest Configuration File

"""
# %% Global imports
from pathlib import Path

import logging
import pytest


# %% py_project_manager imports
from py_project_manager.lib.requirements_traceability import (
    RequirementsTraceability,
    )

from py_project_manager.config import (
    Config)


# -----------------------------------------------------------------------------
# pytest-html

def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Requirements</th>")

def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{report.requirements}</td>")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    
    requirements_ = [i.args for i in item.own_markers
                    if i.name == "requirements"]
    requirements = []
    for ent in requirements_: requirements.extend(ent)
    try:
        requirements_str = ", ".join(requirements) or "None declared"
    except:
        breakpoint()
        
    report = outcome.get_result()
    report.requirements = requirements_str
        

# -----------------------------------------------------------------------------
# pytest-json

def pytest_json_runtest_metadata(item, call):
    requirements_ = [i.args for i in item.own_markers
                    if i.name == "requirements"]
    requirements = []
    for ent in requirements_: requirements.extend(ent)
    try:
        requirements_str = ", ".join(requirements) or "None declared"
    except:
        breakpoint()
    
    return {"requirements": requirements_str}



def pytest_json_modifyreport(json_report):
    """!
    Modify the JSON report after completion of pytest
    
    """    
    logger = logging.getLogger(__name__)
    
    req_tracer = RequirementsTraceability(
        logger=logger,
        raw_report=json_report,
        )
    
    req_tracer.write_traces_by_requirements_to_excel(
        include_untraced_tests=True,
        full_filename=Path(Config.TEST_REPORTS, 
                           "test_trace.xlsx"),
        )
    
    # Add a key to the report
    json_report['foo'] = 'bar'
    # Delete the summary from the report
    del json_report['summary']

