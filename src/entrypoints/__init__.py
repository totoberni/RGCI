"""
Entry point modules for the RGCI framework.

This package contains the main execution scripts for running different aspects
of the framework, including data generation, evaluation, and testing.
"""

from src.entrypoints.run_data_gen import main as run_data_gen
from src.entrypoints.run_evaluation import main as run_evaluation
from src.entrypoints.run_tests import main as run_tests
from src.entrypoints.run_rgci import main as run_rgci
from src.entrypoints.eval_results_analyzer import main as run_analysis

__all__ = [
    'run_data_gen',
    'run_evaluation',
    'run_tests',
    'run_rgci',
    'run_analysis'
]

# Functions to lazily import and return the main functions
def run_data_gen_main(*args, **kwargs):
    from src.entrypoints.run_data_gen import main
    return main(*args, **kwargs)

def run_evaluation_main(*args, **kwargs):
    from src.entrypoints.run_evaluation import main
    return main(*args, **kwargs)

def run_rgci_main(*args, **kwargs):
    from src.entrypoints.run_rgci import main
    return main(*args, **kwargs)

def print_header(*args, **kwargs):
    from src.entrypoints.run_rgci import print_header as ph
    return ph(*args, **kwargs)

def run_tests_main(*args, **kwargs):
    from src.entrypoints.run_tests import main
    return main(*args, **kwargs) 