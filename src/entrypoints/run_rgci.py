#!/usr/bin/env python3
"""
Main entry point script for the RGCI framework
"""
import sys
import os
import argparse

# Add the project root to the Python path to enable imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Load environment variables from the correct location
from src.utils.env_utils import load_env_variables
load_env_variables()

def print_header():
    """Print a header for the script"""
    print("\n" + "="*80)
    print("RGCI: Reproducing GCI - A Benchmarking Framework for Causal Reasoning")
    print("="*80 + "\n")

def main():
    """Main entry point function"""
    parser = argparse.ArgumentParser(description="RGCI Framework for Causal Reasoning Benchmarking")
    parser.add_argument('action', choices=['generate', 'evaluate', 'both'], 
                        help='Action to perform: generate data, evaluate models, or both')
    parser.add_argument('settings_index', type=int, 
                        help='Index of settings to use from settings.py')
    parser.add_argument('--verbose', '-v', action='store_true', 
                        help='Enable verbose output')
    
    args = parser.parse_args()
    
    print_header()
    
    if args.action in ['generate', 'both']:
        print(f"Generating test data with settings index {args.settings_index}...")
        # Import data generation function lazily to avoid circular imports
        orig_argv = sys.argv.copy()
        sys.argv = ['run_data_gen.py', str(args.settings_index)]
        
        # Use lazy import to avoid circular dependency
        from src.entrypoints.run_data_gen import main as data_gen_main
        data_gen_main()
        
        sys.argv = orig_argv
    
    if args.action in ['evaluate', 'both']:
        print(f"Running evaluation with settings index {args.settings_index}...")
        # Import evaluation function lazily to avoid circular imports
        orig_argv = sys.argv.copy()
        sys.argv = ['run_evaluation.py', str(args.settings_index)]
        
        # Use lazy import to avoid circular dependency
        from src.entrypoints.run_evaluation import main as eval_main
        eval_main()
        
        sys.argv = orig_argv
    
    print("\nCompleted!")

if __name__ == "__main__":
    main() 