#!/usr/bin/env python3
"""
Script to evaluate LLM performance on causal reasoning tasks
"""
import os
import sys
import pickle
import json
from datetime import datetime

# Add the project root to the Python path to enable imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.tests.test_utils import test_llm
from src.evaluation.eval_utils import extract_answer, eval_llm
from src.core.settings import get_test_settings, DEFAULT_EXTRACTOR_MODEL
from src.core.paths import (
    GENERATED_DATA_DIR, 
    PICKLE_DIR, 
    get_model_result_dirs, 
    get_file_path, 
    file_exists, 
    safe_join_path,
    wait_for_file
)

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.entrypoints.run_evaluation <settings_index>")
        sys.exit(1)
    
    settings_index = int(sys.argv[1])
    
    data_folder = PICKLE_DIR
    settings = get_test_settings(settings_index)
    
    print(datetime.now(), "work start...", flush=True)
    for model in settings.keys():
        if settings[model]['enable']:
            test_api_key = settings[model]['test_api_key']
            extractor_api_key = settings[model]['extractor_api_key']
            extractor_model = settings[model].get('extractor_model', DEFAULT_EXTRACTOR_MODEL)
            graph_shape_group = settings[model]['graph_shape_group']
            graph_shape = settings[model]['graph_shape']
            
            # Get model-specific result directories
            model_dir, test_dir, ans_ex_dir, eval_dir = get_model_result_dirs(model)
            
            # Create directories if they don't exist
            for directory in [test_dir, ans_ex_dir, eval_dir]:
                os.makedirs(directory, exist_ok=True)
        
            for t in settings[model]['task']:
                for n in settings[model]['name_type']:
                    for p in settings[model]['prompt']:
                        print('─' * 60)
                        print(datetime.now(), f"currently at: {model} | {t}_{graph_shape_group}_{n}_{p}", flush=True)
                        
                        # Construct file paths using the helper function
                        test_file = get_file_path(test_dir, t, graph_shape_group, n, p)
                        ans_ex_file = get_file_path(ans_ex_dir, t, graph_shape_group, n, p)
                        eval_file = get_file_path(eval_dir, t, graph_shape_group, n, p)
                        
                        # Check if test file exists before proceeding
                        if settings[model]['test']:
                            print(datetime.now(), "start test...", flush=True)
                            test_llm(test_api_key, model, t, graph_shape_group, graph_shape, n, p, data_folder, test_file)
                            print(datetime.now(), "test done", flush=True)
                        elif not file_exists(test_file):
                            print(f"WARNING: Test file does not exist: {test_file}")
                            print(f"Skipping this task", flush=True)
                            continue
                        
                        # Extract answers if enabled
                        if settings[model]['ans_ex']:
                            print(datetime.now(), "start answer extraction...", flush=True)
                            try:
                                # Wait for test file to be fully written
                                if wait_for_file(test_file):
                                    extract_answer(extractor_api_key, extractor_model, t, test_file, ans_ex_file)
                                    print(datetime.now(), "answer extraction done", flush=True)
                                else:
                                    print(f"ERROR: Test file not available after waiting: {test_file}")
                                    print(f"Skipping to next task", flush=True)
                                    continue
                            except FileNotFoundError as e:
                                print(f"ERROR: File not found during extraction: {str(e)}")
                                print(f"Skipping to next task", flush=True)
                                continue
                        elif not file_exists(ans_ex_file):
                            print(f"WARNING: Answer extraction file does not exist: {ans_ex_file}")
                            print(f"Skipping to next task", flush=True)
                            continue
                        
                        # Evaluate if enabled
                        if settings[model]['eval']:
                            print(datetime.now(), "start evaluation...", flush=True)
                            try:
                                # Wait for ans_ex file to be fully written
                                if wait_for_file(ans_ex_file):
                                    eval_llm(t, graph_shape_group, n, data_folder, ans_ex_file, eval_file)
                                    print(datetime.now(), "evaluation done", flush=True)
                                else:
                                    print(f"ERROR: Answer extraction file not available after waiting: {ans_ex_file}")
                                    print(f"Skipping to next task", flush=True)
                                    continue
                            except FileNotFoundError as e:
                                print(f"ERROR: File not found during evaluation: {str(e)}")
                                print(f"Skipping to next task", flush=True)
                                continue

    print('─' * 60)
    print(datetime.now(), "all finished", flush=True)

if __name__ == "__main__":
    main() 