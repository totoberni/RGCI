# RGCI - Reproducing GCI: A Benchmarking Framework for Causal Reasoning

This repository contains a framework for benchmarking Large Language Models (LLMs) on causal reasoning tasks. It generates synthetic causal graphs, creates test queries, evaluates model performance, and analyzes results.

## Directory Structure

```
RGCI/
├── .git/                      # Git repository data
├── generated_data/            # Output directory for generated test data
│   ├── graph_png/             # Visualizations of generated causal graphs
│   └── pickle/                # Serialized data for graphs, queries, and node names
├── name_data/                 # Domain-specific entity names for causal graph nodes
│   ├── bio.txt                # Biology domain entity names
│   ├── che.txt                # Chemistry domain entity names
│   ├── eco.txt                # Economics domain entity names
│   └── phy.txt                # Physics domain entity names
├── .gitattributes             # Git attributes configuration
├── api_request_utils.py       # Utilities for making API requests to LLMs
├── cf_utils.py                # Counterfactual reasoning utilities
├── conf_utils.py              # Confounding/causal relationship utilities
├── eval_utils.py              # Evaluation utilities for LLM responses
├── graph_utils.py             # Graph generation and manipulation utilities
├── public_utils.py            # General utility functions
├── settings.py                # Configuration settings for tests and data generation
├── test_data_gen.py           # Test data generation script
├── test_eval.py               # Test evaluation script
└── test_utils.py              # Testing utilities
```

## Environment Setup

### Sample .env File

Create a `.env` file in the RGCI directory with the following contents:

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

You can save this as `.env.example` in your repository and instruct users to copy it to `.env` with their actual API keys.

### Requirements

Create a `requirements.txt` file in the RGCI directory with the following dependencies:

```
numpy>=1.24.0
graphviz>=0.20.1
matplotlib>=3.7.1
pandas>=2.0.0
python-dotenv>=1.0.0
http.client
json
pickle
os
sys
datetime
random
string
```

## Use Cases and Documentation

### 1. Generate Test Data

The framework generates causal graphs with various configurations, creates node names with domain-specific terminology, and formulates causal reasoning queries.

```bash
python test_data_gen.py <settings_index>
```

Where `<settings_index>` is an integer referring to the configuration in `settings.py`.

### 2. Run Tests on LLMs

Test LLMs on causal reasoning tasks including:
- Causal path identification
- Confounding control
- Counterfactual inference
- Factual inference

```bash
python test_eval.py <settings_index>
```

### 3. Task Types

The system supports four main causal reasoning task types:
- **conf_ce_path**: Identifying causal paths
- **conf_conf_ctrl**: Controlling for confounders
- **cf_f_infer**: Factual inference
- **cf_cf_infer**: Counterfactual inference

### 4. Data Generation Parameters

The data generation process can be configured through `settings.py`:
- Graph shapes and complexity
- Number of nodes and edges
- Connection probabilities
- Domain-specific naming conventions

### 5. Evaluation Process

1. Generate causal graphs and test queries
2. Send prompts to LLMs via API
3. Extract structured answers from model responses
4. Evaluate correctness against ground truth
5. Generate performance metrics and visualizations

## API Integration

The system is designed to work with OpenAI API-compatible models. Configure the API settings in the `.env` file and in `settings.py` before running tests.

### Configuring API Keys in settings.py

To use the framework, you need to update the API keys in `settings.py`:

```python
{
    "gpt-3.5-turbo": {
        "enable": True,
        "test_api_key": "Bearer YOUR_OPENAI_API_KEY",  # Replace with your key
        "extractor_api_key": "Bearer YOUR_EXTRACTOR_API_KEY",  # Replace with your key
        # other settings...
    }
}
```

## Code Overview

- **api_request_utils.py**: Handles API communication with LLM providers
- **conf_utils.py**: Generates and processes confounding/causal relationship queries
- **cf_utils.py**: Generates and processes counterfactual reasoning queries
- **graph_utils.py**: Creates and manipulates directed acyclic graphs (DAGs)
- **public_utils.py**: Provides general utility functions for graph visualization, path finding, and naming
- **test_data_gen.py**: Orchestrates the generation of test data based on configuration
- **test_eval.py**: Runs the evaluation pipeline on LLM responses
- **eval_utils.py**: Analyzes and scores model responses against ground truth 