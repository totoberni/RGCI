#!/usr/bin/env python3
"""
Script to evaluate LLM performance on causal reasoning tasks
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the parent directory to the Python path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try to load environment variables from config directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

from tests.test_utils import test_llm
from src.evaluation.eval_utils import extract_answer, eval_llm
from config.settings import get_test_settings, GENERATED_DATA_DIR, PICKLE_DIR


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_evaluation.py <settings_index>")
        sys.exit(1)
    
    settings_index = int(sys.argv[1])
    
    data_folder = PICKLE_DIR
    output_folder = os.path.join(GENERATED_DATA_DIR, "result")
    settings = get_test_settings(settings_index)
    extractor_model = "gpt-4o"

    print(datetime.now(), "work start...", flush=True)
    for model in settings.keys():
        if settings[model]['enable']:
            test_api_key = settings[model]['test_api_key']
            extractor_api_key = settings[model]['extractor_api_key']
            graph_shape_group = settings[model]['graph_shape_group']
            graph_shape = settings[model]['graph_shape']
            model_folder = os.path.join(output_folder, model)
            test_folder = os.path.join(model_folder, 'test')
            ans_ex_folder = os.path.join(model_folder, 'ans_ex')
            eval_folder = os.path.join(model_folder, 'eval')
            os.makedirs(test_folder, exist_ok=True)
            os.makedirs(ans_ex_folder, exist_ok=True)
            os.makedirs(eval_folder, exist_ok=True)
        
            for t in settings[model]['task']:
                for n in settings[model]['name_type']:
                    for p in settings[model]['prompt']:
                        indicators = [t, graph_shape_group, n, p]
                        file_name = "_".join(indicators)
                        print('─' * 60)
                        print(datetime.now(), f"currently at: {model} | {file_name}", flush=True)
                        
                        print(datetime.now(), "start test...", flush=True)
                        if settings[model]['test']:
                            output_path = os.path.join(test_folder, f"{file_name}.json")
                            test_llm(test_api_key, model, t, graph_shape_group, graph_shape, n, p, data_folder, output_path)
                        print(datetime.now(), "test done", flush=True)
                        
                        print(datetime.now(), "start answer extraction...", flush=True)
                        if settings[model]['ans_ex']:
                            res_path = os.path.join(test_folder, f"{file_name}.json")
                            output_path = os.path.join(ans_ex_folder, f"{file_name}.json")
                            extract_answer(extractor_api_key, extractor_model, t, res_path, output_path)
                        print(datetime.now(), "answer extraction done", flush=True)
                        
                        print(datetime.now(), "start evaluation...", flush=True)
                        if settings[model]['eval']:
                            ans_ex_path = os.path.join(ans_ex_folder, f"{file_name}.json")
                            output_path = os.path.join(eval_folder, f"{file_name}.json")
                            eval_llm(t, graph_shape_group, n, data_folder, ans_ex_path, output_path)
                        print(datetime.now(), "evaluation done", flush=True)

    print('─' * 60)
    print(datetime.now(), "all finished", flush=True)

if __name__ == "__main__":
    main() 