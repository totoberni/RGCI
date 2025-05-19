import os
from dotenv import load_dotenv
from src.utils.env_utils import load_env_variables

# Load environment variables using our centralized utility function
load_env_variables()

# Import paths from the paths module
from src.core.paths import (
    PROJECT_ROOT,
    DATA_DIR,
    GENERATED_DATA_DIR,
    NAME_DATA_DIR,
    PICKLE_DIR,
    GRAPH_PNG_DIR,
    RESULT_DIR,
    ensure_directories
)

# Ensure directories exist
ensure_directories()

# Define default models for different roles
DEFAULT_EXTRACTOR_MODEL = "gpt-4o"
SECONDARY_EXTRACTOR_MODEL = "o4-mini"

def get_test_settings(idx):
    # Get API keys directly from environment to ensure we have the most current values
    api_key = os.environ.get('OPENAI_API_KEY', '')
    extractor_api_key = os.environ.get('OPENAI_API_KEY_EXTRACTOR', '')
    
    settings = [
        {
            "gpt-3.5-turbo": {  # 0
                "enable": True,
                "test_api_key": api_key,
                "extractor_api_key": extractor_api_key,
                "extractor_model": DEFAULT_EXTRACTOR_MODEL,
                "task": ["conf_ce_path", "conf_conf_ctrl", "cf_f_infer", "cf_cf_infer"],
                "graph_shape_group": "00",
                "graph_shape": ["00", "01", "02"],
                "name_type": ["specific"],
                "prompt": [
                    "zero_shot",
                    "one_shot",
                    "two_shot",
                    "zero_cot",
                    "one_cot",
                    "two_cot",
                    "mis_hint",
                ],
                "test": True,
                "ans_ex": True,
                "eval": True,
            }
        },
        {
            "gpt-3.5-turbo": {  # 1 with o4-mini
                "enable": True,
                "test_api_key": api_key,
                "extractor_api_key": extractor_api_key,
                "extractor_model": SECONDARY_EXTRACTOR_MODEL,
                "task": ["conf_ce_path", "conf_conf_ctrl", "cf_f_infer", "cf_cf_infer"],
                "graph_shape_group": "00",
                "graph_shape": ["00", "01", "02"],
                "name_type": ["bio", "che", "eco", "phy"],
                "prompt": [
                    "zero_shot",
                    "one_shot",
                    "two_shot",
                    "zero_cot",
                    "one_cot",
                    "two_cot",
                    "mis_hint",
                ],
                "test": True,
                "ans_ex": True,
                "eval": True,
            }
        },
        # Example configurations for other models
        {
            "gpt-4o": {  # 2 - GPT-4o example
                "enable": True,  # Set to True to enable testing with this model
                "test_api_key": api_key,
                "extractor_api_key": extractor_api_key,
                "extractor_model": DEFAULT_EXTRACTOR_MODEL,
                "task": ["conf_ce_path", "conf_conf_ctrl", "cf_f_infer", "cf_cf_infer"],
                "graph_shape_group": "00",
                "graph_shape": ["00", "01", "02"],
                "name_type": ["specific"],
                "prompt": ["zero_shot", "zero_cot"],
                "test": True,
                "ans_ex": True,
                "eval": True,
            }
        },
        {
            "gpt-4": {  # 3 - GPT-4 example
                "enable": True,
                "test_api_key": api_key,
                "extractor_api_key": extractor_api_key,
                "extractor_model": "DEFAULT_EXTRACTOR_MODEL",
                "task": ["conf_ce_path", "conf_conf_ctrl", "cf_f_infer", "cf_cf_infer"],
                "graph_shape_group": "00",
                "graph_shape": ["00", "01", "02"],
                "name_type": ["specific"],
                "prompt": ["zero_shot", "zero_cot"],
                "test": True,
                "ans_ex": True,
                "eval": True,
            }
        },
        {
            "gpt-4-turbo": {  # 4 - GPT-4 Turbo example
                "enable": True,
                "test_api_key": api_key,
                "extractor_api_key": extractor_api_key,
                "extractor_model": DEFAULT_EXTRACTOR_MODEL,
                "task": ["conf_ce_path", "conf_conf_ctrl", "cf_f_infer", "cf_cf_infer"],
                "graph_shape_group": "00",
                "graph_shape": ["00", "01", "02"],
                "name_type": ["specific"],
                "prompt": ["zero_shot", "zero_cot"],
                "test": True,
                "ans_ex": True,
                "eval": True,
            }
        }
    ]
    return settings[idx]


def get_data_gen_settings(idx):
    settings = [
        {
            "gs_indicator": 0,
            "graph_shape": [[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3]],
            "graph_shape_group": "00",
            "path_iter_n": [3, 4, 5, 6],
            "graph_p": [[0.1, 0.1, 0.1]],
            "graph_n_per_condition": 50,
            "conf_ce_d": [1],
            "cf_whatif_n": [1, 2, 3],
            "name_type": ["bio", "che", "eco", "phy"],
        },
        {
            "gs_indicator": 1,
            "graph_shape": [[1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 3]],
            "graph_shape_group": "10",
            "path_iter_n": [3, 4, 5, 6],
            "graph_p": [[0.1, 0.1, 0.1]],
            "graph_n_per_condition": 50,
            "conf_ce_d": [1, 0.5],
            "cf_whatif_n": [1, 2, 3],
            "name_type": ["bio", "che", "eco", "phy"],
        },
        {
            "gs_indicator": 2,
            "graph_shape": [[1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2]],
            "graph_shape_group": "20",
            "path_iter_n": [3, 4, 5, 6],
            "graph_p": [[0.1, 0.1, 0.1]],
            "graph_n_per_condition": 50,
            "conf_ce_d": [1, 0.5],
            "cf_whatif_n": [1, 2, 3],
            "name_type": ["bio", "che", "eco", "phy"],
        },
        {
            "gs_indicator": 3,
            "graph_shape": [[1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2]],
            "graph_shape_group": "30",
            "path_iter_n": [3, 4, 5, 6],
            "graph_p": [[0.1, 0.1, 0.1]],
            "graph_n_per_condition": 50,
            "conf_ce_d": [1, 0.75, 0.5],
            "cf_whatif_n": [1, 2, 3],
            "name_type": ["bio", "che", "eco", "phy"],
        },
    ]
    return settings[idx]
