"""
Entry point scripts for RGCI framework
"""

# Use function references to avoid circular imports
__all__ = [
    'run_data_gen_main',
    'run_evaluation_main',
    'run_rgci_main',
    'print_header',
    'run_tests_main'
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