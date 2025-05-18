#!/usr/bin/env python3
"""
Script to run tests for the RGCI framework
"""
import os
import sys
import argparse

# Add the project root to the Python path to enable imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

def print_header():
    """Print a header for the script"""
    print("\n" + "="*80)
    print("RGCI: Tests for the Causal Reasoning Benchmarking Framework")
    print("="*80 + "\n")

def main():
    """Main entry point function for running tests"""
    parser = argparse.ArgumentParser(description="Run tests for the RGCI Framework")
    parser.add_argument('test_type', choices=['data_gen', 'eval', 'all'], 
                      help='Test type to run: data generation, evaluation, or both')
    parser.add_argument('--settings_index', type=int, default=1,
                      help='Index of settings to use from settings.py')
    parser.add_argument('--verbose', '-v', action='store_true', 
                      help='Enable verbose output')
    
    args = parser.parse_args()
    
    print_header()
    
    # Save original sys.argv because test scripts expect to receive settings_index as sys.argv[1]
    orig_argv = sys.argv.copy()
    # Replace with the settings index for test scripts
    sys.argv = [sys.argv[0], str(args.settings_index)]
    
    if args.test_type in ['data_gen', 'all']:
        print(f"Running data generation tests with settings index {args.settings_index}...")
        try:
            from src.tests.test_data_gen import main as data_gen_main
            data_gen_main()
        except Exception as e:
            print(f"Error running data generation tests: {e}")
        
    if args.test_type in ['eval', 'all']:
        print(f"Running evaluation tests with settings index {args.settings_index}...")
        try:
            from src.tests.test_eval import main as eval_main
            eval_main()
        except Exception as e:
            print(f"Error running evaluation tests: {e}")
    
    # Restore original sys.argv
    sys.argv = orig_argv
        
    print("\nTests completed!")

if __name__ == "__main__":
    main() 