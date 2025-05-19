# RGCI - Reproducing GCI: A Benchmarking Framework for Causal Reasoning

This repository implements the replication of the GCI (Graph-based Causal Inference) benchmark introduced by Chen Wang et al. in their paper ["Do LLMs Have the Generalization Ability in Conducting Causal Inference?"](https://arxiv.org/abs/2410.11385). The framework systematically evaluates Large Language Models (LLMs) on causal reasoning tasks by generating synthetic causal graphs, creating test queries, evaluating model performance, and analyzing results.

## Directory Structure

```
RGCI/
├── config/                    # Configuration settings
│   ├── __init__.py            # Package initialization and environment loading
│   └── .env                   # Environment variables (API keys, etc.)
├── scripts/                   # Helper scripts
│   ├── setup_env.bat          # Windows environment setup
│   ├── setup_env.sh           # Unix environment setup
│   ├── stop.bat               # Windows environment cleanup
│   └── stop.sh                # Unix environment cleanup
├── src/                       # Source code organized as Python packages
│   ├── __init__.py            # Package initialization
│   ├── api/                   # API integration with LLMs
│   │   └── api_request_utils.py # OpenAI API utilities
│   ├── core/                  # Core functionality for causal reasoning
│   │   ├── settings.py        # Configuration parameters
│   │   ├── graph_utils.py     # Graph generation utilities
│   │   ├── conf_utils.py      # Confounding reasoning utilities
│   │   └── cf_utils.py        # Counterfactual reasoning utilities
│   ├── data/                  # Input data for the system
│   │   ├── generated_data/    # Generated intermediate data
│   │   │   ├── pickle/        # Serialized data files
│   │   │   ├── graph_png/     # Visualized causal graphs
│   │   │   └── result/        # Evaluation results
│   │   └── name_data/         # Domain-specific entity names for causal graph nodes
│   ├── entrypoints/           # Entry point scripts for running the system
│   │   ├── run_data_gen.py    # Data generation script
│   │   ├── run_evaluation.py  # Evaluation script
│   │   ├── run_rgci.py        # Main entry point
│   │   └── run_tests.py       # Test runner
│   ├── evaluation/            # Evaluation utilities
│   │   └── eval_utils.py      # Evaluation functions
│   ├── tests/                 # Test modules
│   │   ├── test_data_gen.py   # Test data generation
│   │   ├── test_eval.py       # Test evaluation
│   │   └── test_utils.py      # Testing utilities
│   └── utils/                 # General utility functions
│       └── public_utils.py    # Shared utility functions
└── .gitattributes             # Git attributes configuration
```

## Environment Setup

### Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

The requirements include:
```
numpy>=1.24.0
graphviz>=0.20.1
matplotlib>=3.7.1
pandas>=2.0.0
python-dotenv>=1.0.0
openai~=1.0.0
```

### Environment Configuration

Use the provided setup scripts to initialize the environment:

**For Windows:**
```bash
scripts/setup_env.bat
```

**For Unix/Linux/MacOS:**
```bash
./scripts/setup_env.sh
```

### Getting an OpenAI API Key

This project uses the OpenAI API for evaluating LLMs. To obtain an API key:

1. Create an account on the [OpenAI platform](https://platform.openai.com/signup)
2. Navigate to the [API keys page](https://platform.openai.com/account/api-keys)
3. Click "Create new secret key" and provide a name for your key
4. Copy the key immediately (you won't be able to see it again)

### API Configuration

Create a `.env` file in the `config` directory with your API keys and settings:

```
# OpenAI API Keys
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_API_KEY_EXTRACTOR=sk-your-openai-api-key-for-extraction

# Optional: Custom data directory path
# OUTPUT_PATH=path/to/custom/data/directory
```

The setup script will create a template `.env` file that you can customize with your API keys.

### Testing API Connectivity

To verify that your API keys are working correctly and to test connectivity with the OpenAI models:

```bash
# Test the base GPT-3.5-turbo model and all extractor models
python scripts/test_api.py

# Test with just the default extractor model (gpt-4o)
python scripts/test_api.py --model default

# Test with just the secondary extractor model (gpt-4o-mini)
python scripts/test_api.py --model secondary

# Test with a specific model
python scripts/test_api.py --model gpt-4
```

This tool helps verify that:
- Your API keys are valid
- The environment variables are loaded correctly
- The specified models are accessible through the API

If you encounter any errors, the script provides detailed debug information to help troubleshoot connectivity issues.

### Path Configuration

The framework uses a centralized path management system in `src/core/paths.py`. You can customize where data is stored by setting the `OUTPUT_PATH` environment variable in your `.env` file:

```
# Store data in a custom location (absolute path)
OUTPUT_PATH=C:/Users/username/Documents/RGCI_data

# Or use a relative path (relative to project root)
OUTPUT_PATH=custom_data
```

If `OUTPUT_PATH` is not specified, data will be stored in the default location at `src/data/`.

## Usage

### Main Entry Point

Use the main script for standard operations:

```bash
python -m src.entrypoints.run_rgci [generate|evaluate|both] <settings_index>
```

Where:
- First argument specifies what action to perform: generate data, evaluate models, or both.
- `<settings_index>` is an integer referring to the configuration in `src/core/settings.py`.

### Individual Operations

#### 1. Generate Test Data

Generate causal graphs with various configurations, create node names with domain-specific terminology, and formulate causal reasoning queries:

```bash
python -m src.entrypoints.run_data_gen <settings_index>
```

#### 2. Run Evaluations on LLMs

Test LLMs on causal reasoning tasks:

```bash
python -m src.entrypoints.run_evaluation <settings_index>
```

### Running Tests

To run tests for the framework:

```bash
python -m src.entrypoints.run_tests [data_gen|eval|all]
```

### Cleaning Up the Environment

To remove the virtual environment and clean up dependencies:

**For Windows:**
```bash
scripts\stop.bat
```

**For Unix/Linux/MacOS:**
```bash
./scripts/stop.sh
```

These scripts will:
- Deactivate the virtual environment if active
- Remove the virtual environment directory
- Clean the pip cache
- Note that the .env file in the config directory is not removed automatically

## Task Types

The system supports four main causal reasoning task types:
- **conf_ce_path**: Identifying causal paths
- **conf_conf_ctrl**: Controlling for confounders
- **cf_f_infer**: Factual inference
- **cf_cf_infer**: Counterfactual inference

## Model Configuration and Customization

The framework is designed to evaluate multiple LLMs with different configurations. The testing settings are defined in `src/core/settings.py`.

### Model Types and Roles

Two types of models are used in the evaluation process:

1. **Testing Models**: These are the models being evaluated on causal reasoning tasks (e.g., GPT-3.5-turbo, GPT-4, etc.)
2. **Extractor Model**: A separate model (typically GPT-4o) used to extract structured answers from the testing models' responses

### Parallel Model Evaluation

The system supports running multiple evaluation instances with the same model name but different configurations:

- When running an evaluation, if a result directory for the specified model already exists, a new unique directory name is automatically created (e.g., `gpt-3.5-turbo1`, `gpt-3.5-turbo2`)
- This allows parallel testing of the same model with different extractors or settings without overwriting previous results
- The naming pattern follows `model_name` → `model_name1` → `model_name2` and so on

To run parallel evaluations:

```bash
# Run first evaluation with index 0
python -m src.entrypoints.run_evaluation 0

# Simultaneously run another evaluation with index 1
# Results will be stored in a separate directory
python -m src.entrypoints.run_evaluation 1
```

### Configuring Models

Models and their settings are configured in `src/core/settings.py` in the `get_test_settings()` function:

```python
def get_test_settings(idx):
    settings = [
        {
            "gpt-3.5-turbo": {
                "enable": True,                         # Enable/disable this model
                "test_api_key": DEFAULT_API_KEY,        # API key for the testing model
                "extractor_api_key": DEFAULT_EXTRACTOR_API_KEY,  # API key for the extractor
                "extractor_model": DEFAULT_EXTRACTOR_MODEL,      # Model to use for extraction
                "task": ["conf_ce_path", "conf_conf_ctrl", "cf_f_infer", "cf_cf_infer"],  # Tasks to evaluate
                "graph_shape_group": "00",              # Graph complexity group
                "graph_shape": ["00", "01", "02"],      # Specific graph shapes
                "name_type": ["specific"],              # Node naming conventions
                "prompt": ["zero_shot", "one_shot"],    # Prompt types to test
                "test": True,                           # Run testing phase
                "ans_ex": True,                         # Run answer extraction phase
                "eval": True,                           # Run evaluation phase
            }
        },
        # Additional configuration presets...
    ]
    return settings[idx]
```

### Adding New Models

To add a new model for testing:

1. Add a new dictionary entry to the settings list in `get_test_settings()`
2. Configure the model parameters as shown above
3. Make sure to provide a valid API key that works with your chosen model

### Customizing Evaluation Settings

You can customize various aspects of the evaluation process:

- **Tasks**: Choose which causal reasoning tasks to evaluate
- **Graph Complexity**: Select graph shape groups and specific shapes
- **Naming Conventions**: Choose domain-specific terminology for nodes
- **Prompt Types**: Select from zero-shot, one-shot, two-shot, etc.
- **Process Stages**: Enable/disable testing, answer extraction, and evaluation phases

## Data Generation Parameters

The data generation process can be configured through `src/core/settings.py` in the `get_data_gen_settings()` function:

```python
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
        # Additional generation configurations...
    ]
    return settings[idx]
```

Parameters include:
- Graph shapes and complexity
- Number of nodes and tiers
- Connection probabilities
- Domain-specific naming conventions 