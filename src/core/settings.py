import os

# Define paths relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'src', 'data')
GENERATED_DATA_DIR = os.path.join(DATA_DIR, 'generated_data')
NAME_DATA_DIR = os.path.join(DATA_DIR, 'name_data')
PICKLE_DIR = os.path.join(GENERATED_DATA_DIR, 'pickle')
GRAPH_PNG_DIR = os.path.join(GENERATED_DATA_DIR, 'graph_png')

# Ensure directories exist
os.makedirs(PICKLE_DIR, exist_ok=True)
os.makedirs(GRAPH_PNG_DIR, exist_ok=True)

# Get API keys from environment variables with fallbacks to empty strings
DEFAULT_API_KEY = os.environ.get('OPENAI_API_KEY', '')
DEFAULT_EXTRACTOR_API_KEY = os.environ.get('OPENAI_API_KEY_EXTRACTOR', '')

# Define default models for different roles
DEFAULT_EXTRACTOR_MODEL = "gpt-4o"

def get_test_settings(idx):
    settings = [
        {
            "gpt-3.5-turbo": {  # 0
                "enable": True,
                "test_api_key": DEFAULT_API_KEY,
                "extractor_api_key": DEFAULT_EXTRACTOR_API_KEY,
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
            "gpt-3.5-turbo": {  # 1
                "enable": True,
                "test_api_key": DEFAULT_API_KEY,
                "extractor_api_key": DEFAULT_EXTRACTOR_API_KEY,
                "extractor_model": DEFAULT_EXTRACTOR_MODEL,
                "task": ["conf_ce_path", "conf_conf_ctrl", "cf_f_infer", "cf_cf_infer"],
                "graph_shape_group": "00",
                "graph_shape": ["00", "01", "02"],
                "name_type": ["bio", "che", "eco", "phy"],
                "prompt": [
                    "zero_shot",
                ],
                "test": True,
                "ans_ex": True,
                "eval": True,
            }
        },
        # Example configurations for other models
        {
            "gpt-4o": {  # 2 - GPT-4o example
                "enable": False,  # Set to True to enable testing with this model
                "test_api_key": DEFAULT_API_KEY,
                "extractor_api_key": DEFAULT_EXTRACTOR_API_KEY,
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
                "enable": False,
                "test_api_key": DEFAULT_API_KEY,
                "extractor_api_key": DEFAULT_EXTRACTOR_API_KEY,
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
            "gpt-4-turbo": {  # 4 - GPT-4 Turbo example
                "enable": False,
                "test_api_key": DEFAULT_API_KEY,
                "extractor_api_key": DEFAULT_EXTRACTOR_API_KEY,
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
