#!/usr/bin/env python3
"""
Main entry point script for the RGCI framework
"""
import sys
import os
import argparse
from dotenv import load_dotenv

# Add the parent directory to the Python path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try to load environment variables from config directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

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
        # Import and run data generation with settings index
        import scripts.run_data_gen
        # Set sys.argv for the import
        sys.argv = ['run_data_gen.py', str(args.settings_index)]
        scripts.run_data_gen.main()
    
    if args.action in ['evaluate', 'both']:
        print(f"Running evaluation with settings index {args.settings_index}...")
        # Import and run evaluation with settings index
        import scripts.run_evaluation
        # Set sys.argv for the import
        sys.argv = ['run_evaluation.py', str(args.settings_index)]
        scripts.run_evaluation.main()
    
    print("\nCompleted!")

if __name__ == "__main__":
    main() 