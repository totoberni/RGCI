# RGCI - Reproducing GCI: A Benchmarking Framework for Causal Reasoning

This repository implements the replication of the GCI (Graph-based Causal Inference) benchmark introduced by Chen Wang et al. in their paper ["Do LLMs Have the Generalization Ability in Conducting Causal Inference?"](https://arxiv.org/abs/2410.11385). The framework systematically evaluates Large Language Models (LLMs) on causal reasoning tasks by generating synthetic causal graphs, creating test queries, evaluating model performance, and analyzing results.

## Directory Structure

```
RGCI/
├── config/                    # Configuration settings
│   ├── __init__.py            # Package initialization
│   ├── requirements.txt       # Package dependencies 
│   └── settings.py            # Configuration parameters
├── data/                      # Input data for the system
│   ├── generated_data/        # Generated intermediate data
│   │   └── pickle/            # Serialized data files
│   └── name_data/             # Domain-specific entity names for causal graph nodes
├── scripts/                   # Scripts for running various system components
│   ├── run_data_gen.py        # Data generation script
│   ├── run_evaluation.py      # Evaluation script
│   ├── run_rgci.py            # Main entry point
│   ├── run_tests.py           # Test runner
│   ├── setup_env.bat          # Windows environment setup
│   └── setup_env.sh           # Unix environment setup
├── src/                       # Source code organized as Python packages
│   ├── __init__.py            # Package initialization
│   ├── api/                   # API integration with LLMs
│   ├── core/                  # Core functionality for causal reasoning
│   ├── evaluation/            # Evaluation utilities
│   └── utils/                 # General utility functions
├── tests/                     # Test files
│   ├── __init__.py            # Package initialization
│   ├── test_data_gen.py       # Test data generation
│   ├── test_eval.py           # Test evaluation
│   └── test_utils.py          # Testing utilities
└── .gitattributes             # Git attributes configuration
```

## Environment Setup

### Requirements

The requirements file is located in the `config` directory. Install dependencies using:

```bash
pip install -r config/requirements.txt
```

The requirements include:
```
numpy>=1.24.0
graphviz>=0.20.1
matplotlib>=3.7.1
pandas>=2.0.0
python-dotenv>=1.0.0
openai ~=1.0.0
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

# API Connection Settings
API_HOST=api.openai.com
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
CONTENT_TYPE=application/json

# Output Directories
OUTPUT_PATH=./generated_data
```

The setup script will create a template `.env` file that you can customize with your API keys.

## Usage

### Main Entry Point

Use the main script for standard operations:

```bash
python scripts/run_rgci.py [generate|evaluate|both] <settings_index>
```

Where:
- First argument specifies what action to perform: generate data, evaluate models, or both.
- `<settings_index>` is an integer referring to the configuration in `config/settings.py`.

### Individual Operations

#### 1. Generate Test Data

Generate causal graphs with various configurations, create node names with domain-specific terminology, and formulate causal reasoning queries:

```bash
python scripts/run_data_gen.py <settings_index>
```

#### 2. Run Evaluations on LLMs

Test LLMs on causal reasoning tasks:

```bash
python scripts/run_evaluation.py <settings_index>
```

### Running Tests

To run tests for the framework:

```bash
python scripts/run_tests.py [data_gen|eval|all]
```

## Task Types

The system supports four main causal reasoning task types:
- **conf_ce_path**: Identifying causal paths
- **conf_conf_ctrl**: Controlling for confounders
- **cf_f_infer**: Factual inference
- **cf_cf_infer**: Counterfactual inference

## Data Generation Parameters

The data generation process can be configured through `config/settings.py`:
- Graph shapes and complexity
- Number of nodes and edges
- Connection probabilities
- Domain-specific naming conventions

## Evaluation Process

1. Generate causal graphs and test queries
2. Send prompts to LLMs via API
3. Extract structured answers from model responses
4. Evaluate correctness against ground truth
5. Generate performance metrics and visualizations

## API Integration

The system uses the official OpenAI Python SDK to interact with models. The framework is configured to support the following models:
- GPT-3.5-turbo 
- GPT-4 models (when available)

Configure the API settings in the `.env` file in the `config` directory and ensure the model configurations in `config/settings.py` are properly set up. 