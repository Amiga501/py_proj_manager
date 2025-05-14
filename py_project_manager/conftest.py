# -*- coding: utf-8 -*-
"""
Created on Wed May 14 21:31:51 2025

@author: brend
"""
import pytest

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
        