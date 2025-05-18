# -*- coding: utf-8 -*-
"""
Created on Fri May 16 21:06:24 2025

@author: brendan

A module for generating requirements traceability from a call from pytest-json

[Docstrings are in Doxygen format]

This could be integrated with pytest-spiratest to check requirements assigned 
in Spira are addressed or push further requirements back to Spira
See: https://github.com/Inflectra/spira-testing-pytest
The model to follow is *probably* single software requirement per .py
If there were low level design requirements, then possibly per test class 
within the .py

"""
# %% Global modules
from collections.abc import Callable
from copy import deepcopy
# from openpyxl import Workbook  # Import moved to only methods that need it
from pathlib import Path

import pandas as pd


# %% Package modules


# %% Module level configuration


# %% Functions


# %% Classes

# -----------------------------------------------------------------------------
class RequirementsTraceability:
    """!
    Class for generating requirements trace items
    
    """
    
    # -------------------------------------------------------------------------
    def __init__(self, 
                 logger: Callable,
                 raw_report: dict,
                 ):
        """!
        **Instantiate**
        
        @param [in] logger [Callable]
        @param [in] json_report [dict]
        
        """
        self.logger = logger
        
        self.raw_report = raw_report
        
        self.__isolate_requirements_and_tests()
        
    # -------------------------------------------------------------------------
    def __create_full_trace_matrix(self):
        """!
        **Create a full trace matrix**
        
        """
        all_reqs = self.traces_by_requirement.keys()
        all_tests = self.traces_by_test.keys()
        fall_tests_abbr = [f"{i.split('::')[-2]}.{i.split('::')[-1]}" 
                                for i in all_tests]
        
        req_keys = [i for i in all_reqs
                    if i not in ["None declared"]]
        sorted_req_keys = sorted(req_keys)  # TODO import packaging Version
        
        trace_arrays = {}
        for req in sorted_req_keys:
            trace_arrays[req] = []
            for test in all_tests:
                trace_arrays[req].append(
                    "Y" if req in self.traces_by_test[test] else "")    
                
        df = pd.DataFrame(trace_arrays)
        df = df.transpose()
        df.columns = list(fall_tests_abbr)
        
        self.trace_matrix = df
        
    # -------------------------------------------------------------------------
    def __isolate_requirements_and_tests(self):
        """!
        **Isolate the requirements and tests**
        
        Do so oriented by both requirements and by test
        
        """
        self.traces_by_requirement = {}
        self.traces_by_test = {}
        
        if not self.raw_report.get("tests"):
            self.logger.warning(
                "No entry for 'tests' found in report passed to "
                f"{__class__.__name__}, no trace will be generated")
            return
        
        n_tests = len(self.raw_report['tests'])
        for idx, test in enumerate(self.raw_report["tests"]):
            if not (test_case := test.get("nodeid")):
                self.logger.warning(
                    f"No entry found for nodeid within test: {idx} of "
                    f"{n_tests}, skipping...")
                continue
            
            test_case_names = test_case.split("::")
            test_case_name = f"{test_case_names[-2]}.{test_case_names[-1]}"
            test_script = f"{test_case.split('.py')[0]}.py"
            
            if not (meta_data := test.get("metadata")):
                self.logger.warning(
                    f"No metadata found within test: {idx} of "
                    f"{n_tests}, skipping...")
                continue
            
            if not (requirements := meta_data.get("requirements")):
                self.logger.warning(
                    f"No requirements tags found within test: {idx} of "
                    f"{n_tests}, skipping...")
                continue
            
            requirements = requirements.split(", ")
            
            for requirement in requirements:
                if requirement not in self.traces_by_requirement:
                    self.traces_by_requirement[requirement] = []
                
                entry = {"test_script": test_script,
                         "test_case": test_case_name,
                         }
                self.traces_by_requirement[requirement].append(entry)
                if test_case in self.traces_by_test:
                    self.logger.critical(
                        f"Duplicate entries detected for {test_case}, "
                        "full traceability will be lost!")
                self.traces_by_test[test_case] = \
                    requirements
                    
    # -------------------------------------------------------------------------
    def get_traces_by_requirements(
            self, *, 
            include_untraced_tests: bool = True,
            ) -> dict:
        """!
        **Return the traces oriented by requirements**
        
        @param [in] include_untraced_tests [bool] True to include test that 
            have no requirements tagged to them - which will be 'None declared'
            entries
            
        @return [dict] key'd by requirement tag
        
        """
        traces_by_requirement = deepcopy(self.traces_by_requirement)
        if not include_untraced_tests:
            if traces_by_requirement.get("None declared"):
                del traces_by_requirement["None declared"]
        
        return traces_by_requirement
    
    # -------------------------------------------------------------------------
    def get_traces_by_tests(self) -> dict:
        """!
        **Return the traces oriented by tests**
        
        @return [dict] key'd by test
        
        """
        return deepcopy(self.traces_by_test)
        
    # -------------------------------------------------------------------------
    def write_traces_by_requirements_to_excel(
            self, *,
            include_untraced_tests: bool = True,
            full_filename: str,
            ) -> bool:
        """!
        **Write the traces oriented by requirements to excel**
        
        @param [in] include_untraced_tests [bool] True to include test that 
            have no requirements tagged to them - which will be 'None declared'
            entries
        @param [in] full_filename [str] The full filepath (inc filename) to
            write trace file to
        
        @return [bool] True if successful, False otherwise
        
        """
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter
        from openpyxl.utils.dataframe import dataframe_to_rows
        # Import moved here to minimise footprint for users that don't need the
        # excel output
        self.__create_full_trace_matrix()
        
        # Just incase the specified path does not exist, make it now
        if Path(full_filename).suffix != ".xlsx":
            self.logger.error(
                "Invalid full filename specified, must end in .xlsx, "
                f"currently: {full_filename}")
            return False
        try:
            Path(full_filename.parent).mkdir(parents=True, exist_ok=True)
        except Exception as exception:
            self.logger.error(
                f"Unable to make directory to hold report {full_filename} due "
                f"to {exception}"
                )
            return False
        
        wb = Workbook()
        ws = wb.active
        
        rows = dataframe_to_rows(self.trace_matrix)
        
        for r_idx, row in enumerate(rows, 1):
            for c_idx, value in enumerate(row, 1):
                ws.cell(row=r_idx, column=c_idx, value=value)
                if not c_idx % 2:
                    ws.cell(row=r_idx, column=c_idx).fill = PatternFill(
                        start_color="00CCFFFF", 
                        end_color="00CCFFFF",
                        fill_type = "solid")    
                else:
                    ws.cell(row=r_idx, column=c_idx).fill = PatternFill(
                        start_color="00CCFFCC", 
                        end_color="00CCFFCC",
                        fill_type = "solid")    
                    
        for iCol in range(1, len(self.traces_by_test.keys()) + 2):
            ws[f"{get_column_letter(iCol)}1"].alignment = Alignment(
                textRotation=90,
                )
        
        ws["A1"] = "Requirements"
        
        try:
            wb.save(full_filename)
        except Exception as exception:
            self.logger.error(
                f"Unable to save trace matrix as xlsx due to {exception}")
            return False
        return True