"""
Entry point scripts for RGCI framework
"""
from src.entrypoints.run_data_gen import main as run_data_gen_main
from src.entrypoints.run_evaluation import main as run_evaluation_main
from src.entrypoints.run_rgci import main as run_rgci_main, print_header
from src.entrypoints.run_tests import main as run_tests_main

__all__ = [
    'run_data_gen_main',
    'run_evaluation_main',
    'run_rgci_main',
    'print_header',
    'run_tests_main'
] 