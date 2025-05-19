import os
import json
import pandas as pd
import glob
from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

# Import from project modules
from src.utils.public_utils import read_jsonl
from src.core.paths import (
    RESULT_DIR, 
    safe_join_path,
    get_model_eval_dir,
    get_available_models
)

def analyze_model_results(model_name, eval_dir=None, output_format="text"):
    """
    Analyze evaluation results for a specific model.
    
    Args:
        model_name: Name of the model to analyze
        eval_dir: Path to evaluation directory (defaults to model's eval directory)
        output_format: Format for output ("text" or "csv")
    """
    # Set up default eval directory if not provided
    if eval_dir is None:
        eval_dir = get_model_eval_dir(model_name)
    
    # Check if directory exists
    if not os.path.exists(eval_dir):
        print(f"Error: Directory {eval_dir} does not exist")
        return
    
    # Get a list of all evaluation files
    eval_files = glob.glob(f"{eval_dir}/*.json")
    
    if len(eval_files) == 0:
        print(f"No evaluation files found in {eval_dir}")
        return
    
    # Process each file
    results = {}
    task_types = []
    graph_shapes = []
    name_types = []
    prompt_types = []
    
    # Process each file to extract test details and results
    for file_path in eval_files:
        file_name = Path(file_path).stem  # Gets filename without extension
        print(f"Processing {file_name}...")
        
        # Parse file name to extract test parameters
        # Format: task_graph-shape_name-type_prompt-type
        parts = file_name.split('_')
        if len(parts) < 4:
            print(f"Warning: File name {file_name} does not follow expected format. Skipping.")
            continue
        
        # Extract test parameters from filename
        if len(parts) == 4:
            task, graph_shape, name_type, prompt_type = parts
        else:
            # Handle case where task might contain underscores (like conf_ce_path)
            task_parts = parts[:-3]
            task = "_".join(task_parts)
            graph_shape, name_type, prompt_type = parts[-3:]
        
        # Update lists of unique values for each parameter
        if task not in task_types:
            task_types.append(task)
        if graph_shape not in graph_shapes:
            graph_shapes.append(graph_shape)
        if name_type not in name_types:
            name_types.append(name_type)
        if prompt_type not in prompt_types:
            prompt_types.append(prompt_type)
        
        # Read and process the data
        try:
            data = read_jsonl(file_path)
            df = pd.DataFrame(data)
            
            # Calculate success rate for boolean results
            if 'result' not in df.columns:
                print(f"Warning: 'result' column not found in {file_name}")
                continue
            
            # Count different result types
            result_counts = df['result'].value_counts().to_dict()
            
            # Calculate true rate (excluding net_err and unk)
            valid_results = df[df['result'].isin([True, False])]
            true_rate = valid_results['result'].mean() if len(valid_results) > 0 else 0
            
            # Calculate rates for different result types
            total_queries = len(df)
            true_count = result_counts.get(True, 0)
            false_count = result_counts.get(False, 0)
            net_err_count = result_counts.get("net_err", 0)
            unk_count = result_counts.get("unk", 0)
            
            # Store results
            results[file_name] = {
                'task': task,
                'graph_shape': graph_shape,
                'name_type': name_type,
                'prompt_type': prompt_type,
                'total_queries': total_queries,
                'true_count': true_count,
                'false_count': false_count,
                'net_err_count': net_err_count,
                'unk_count': unk_count,
                'true_rate': true_rate,
                'true_percentage': true_count / total_queries * 100,
                'false_percentage': false_count / total_queries * 100,
                'net_err_percentage': net_err_count / total_queries * 100,
                'unk_percentage': unk_count / total_queries * 100
            }
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    if not results:
        print("No results were successfully processed.")
        return
    
    # Convert dictionary to DataFrame for easier analysis
    results_df = pd.DataFrame.from_dict(results, orient='index')
    
    # Print summary statistics
    print(f"\n===== Summary for Model: {model_name} =====\n")
    
    # Display overall stats
    print(f"Total tests analyzed: {len(results_df)}")
    print(f"Overall average success rate: {results_df['true_rate'].mean():.2%}\n")
    
    # Prepare tables for each analysis dimension
    tables = []
    
    # Analysis by task type
    task_summary = results_df.groupby('task').agg({
        'true_rate': 'mean',
        'total_queries': 'sum',
        'true_count': 'sum',
        'false_count': 'sum',
        'net_err_count': 'sum',
        'unk_count': 'sum'
    }).reset_index()
    
    task_summary['success_rate'] = task_summary['true_count'] / task_summary['total_queries']
    tables.append(("Task Type", task_summary[['task', 'success_rate', 'total_queries', 'true_count', 'false_count', 'net_err_count', 'unk_count']]))
    
    # Analysis by prompt type
    prompt_summary = results_df.groupby('prompt_type').agg({
        'true_rate': 'mean',
        'total_queries': 'sum',
        'true_count': 'sum',
        'false_count': 'sum',
        'net_err_count': 'sum',
        'unk_count': 'sum'
    }).reset_index()
    
    prompt_summary['success_rate'] = prompt_summary['true_count'] / prompt_summary['total_queries']
    tables.append(("Prompt Type", prompt_summary[['prompt_type', 'success_rate', 'total_queries', 'true_count', 'false_count', 'net_err_count', 'unk_count']]))
    
    # Analysis by name type
    name_summary = results_df.groupby('name_type').agg({
        'true_rate': 'mean',
        'total_queries': 'sum',
        'true_count': 'sum',
        'false_count': 'sum',
        'net_err_count': 'sum',
        'unk_count': 'sum'
    }).reset_index()
    
    name_summary['success_rate'] = name_summary['true_count'] / name_summary['total_queries']
    tables.append(("Name Type", name_summary[['name_type', 'success_rate', 'total_queries', 'true_count', 'false_count', 'net_err_count', 'unk_count']]))
    
    # Analysis by graph shape
    graph_summary = results_df.groupby('graph_shape').agg({
        'true_rate': 'mean',
        'total_queries': 'sum',
        'true_count': 'sum',
        'false_count': 'sum',
        'net_err_count': 'sum',
        'unk_count': 'sum'
    }).reset_index()
    
    graph_summary['success_rate'] = graph_summary['true_count'] / graph_summary['total_queries']
    tables.append(("Graph Shape", graph_summary[['graph_shape', 'success_rate', 'total_queries', 'true_count', 'false_count', 'net_err_count', 'unk_count']]))
    
    # Task x Prompt analysis
    task_prompt_summary = results_df.groupby(['task', 'prompt_type']).agg({
        'true_rate': 'mean',
        'total_queries': 'sum',
        'true_count': 'sum',
        'false_count': 'sum'
    }).reset_index()
    
    task_prompt_summary['success_rate'] = task_prompt_summary['true_count'] / task_prompt_summary['total_queries']
    tables.append(("Task × Prompt", task_prompt_summary[['task', 'prompt_type', 'success_rate', 'total_queries', 'true_count', 'false_count']]))
    
    # Display tables
    for title, df in tables:
        print(f"\n----- {title} Analysis -----")
        # Format success rate as percentage
        if 'success_rate' in df.columns:
            df['success_rate'] = df['success_rate'].apply(lambda x: f"{x:.2%}")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
    # Detailed breakdown of each test
    print("\n----- Detailed Test Results -----")
    detail_df = results_df[['task', 'graph_shape', 'name_type', 'prompt_type', 'true_percentage', 'false_percentage', 'net_err_percentage', 'unk_percentage', 'total_queries']]
    detail_df = detail_df.sort_values(by=['task', 'prompt_type', 'name_type', 'graph_shape'])
    
    # Format percentages
    for col in ['true_percentage', 'false_percentage', 'net_err_percentage', 'unk_percentage']:
        detail_df[col] = detail_df[col].apply(lambda x: f"{x:.2f}%")
    
    print(tabulate(detail_df, headers='keys', tablefmt='grid', showindex=False))
    
    # Export to CSV if requested
    if output_format == "csv":
        csv_filename = f"{model_name}_evaluation_results.csv"
        results_df.to_csv(csv_filename)
        detail_df.to_csv(f"{model_name}_detailed_results.csv")
        print(f"\nResults exported to {csv_filename} and {model_name}_detailed_results.csv")
    
    # Generate plots
    try:
        # Plot success rate by task
        plt.figure(figsize=(10, 6))
        task_plot = task_summary.copy()
        task_plot['success_rate'] = task_plot['true_count'] / task_plot['total_queries'] * 100
        plt.bar(task_plot['task'], task_plot['success_rate'])
        plt.xlabel('Task Type')
        plt.ylabel('Success Rate (%)')
        plt.title(f'{model_name}: Success Rate by Task')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{model_name}_task_success.png")
        
        # Plot success rate by prompt type
        plt.figure(figsize=(10, 6))
        prompt_plot = prompt_summary.copy()
        prompt_plot['success_rate'] = prompt_plot['true_count'] / prompt_plot['total_queries'] * 100
        plt.bar(prompt_plot['prompt_type'], prompt_plot['success_rate'])
        plt.xlabel('Prompt Type')
        plt.ylabel('Success Rate (%)')
        plt.title(f'{model_name}: Success Rate by Prompt Type')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{model_name}_prompt_success.png")
        
        # Heatmap for task x prompt
        plt.figure(figsize=(12, 8))
        task_prompt_pivot = task_prompt_summary.pivot(index='task', columns='prompt_type', values='success_rate')
        
        # Convert to numerical values for heatmap
        heatmap_data = task_prompt_pivot.applymap(lambda x: x if isinstance(x, (int, float)) else 0)
        
        plt.imshow(heatmap_data, cmap='YlGn', interpolation='nearest', aspect='auto')
        plt.colorbar(label='Success Rate')
        plt.xticks(np.arange(len(task_prompt_pivot.columns)), task_prompt_pivot.columns, rotation=45)
        plt.yticks(np.arange(len(task_prompt_pivot.index)), task_prompt_pivot.index)
        plt.title(f'{model_name}: Task × Prompt Success Rate')
        
        # Add text annotations to the heatmap
        for i in range(len(task_prompt_pivot.index)):
            for j in range(len(task_prompt_pivot.columns)):
                value = heatmap_data.iloc[i, j]
                plt.text(j, i, f"{value:.2%}", ha='center', va='center', 
                         color='black' if value > 0.5 else 'white')
        
        plt.tight_layout()
        plt.savefig(f"{model_name}_task_prompt_heatmap.png")
        
        print(f"\nPlots saved as {model_name}_task_success.png, {model_name}_prompt_success.png, and {model_name}_task_prompt_heatmap.png")
    except Exception as e:
        print(f"Error generating plots: {str(e)}")
    
    return results_df

def compare_models(model_names, eval_base_dir=None):
    """
    Compare results across multiple models.
    
    Args:
        model_names: List of model names to compare
        eval_base_dir: Base directory containing model result folders (defaults to RESULT_DIR)
    """
    if eval_base_dir is None:
        eval_base_dir = RESULT_DIR
        
    if not model_names:
        print("No models specified for comparison")
        return
    
    # Collect results for each model
    model_results = {}
    for model in model_names:
        eval_dir = safe_join_path(safe_join_path(eval_base_dir, model), 'eval')
        if not os.path.exists(eval_dir):
            print(f"Warning: Directory {eval_dir} does not exist. Skipping {model}.")
            continue
        
        print(f"Analyzing {model}...")
        results_df = analyze_model_results(model, eval_dir, output_format="text")
        if results_df is not None:
            model_results[model] = results_df
    
    if len(model_results) < 2:
        print("Not enough valid models for comparison")
        return
    
    # Generate comparison report
    print("\n===== Model Comparison =====")
    
    # Compare overall success rates
    overall_rates = {model: df['true_rate'].mean() for model, df in model_results.items()}
    print("\n----- Overall Success Rates -----")
    overall_df = pd.DataFrame({'Model': list(overall_rates.keys()), 
                              'Success Rate': [f"{rate:.2%}" for rate in overall_rates.values()]})
    print(tabulate(overall_df, headers='keys', tablefmt='grid', showindex=False))
    
    # Compare by task
    task_comparison = {}
    for model, df in model_results.items():
        task_summary = df.groupby('task')['true_rate'].mean()
        for task, rate in task_summary.items():
            if task not in task_comparison:
                task_comparison[task] = {}
            task_comparison[task][model] = rate
    
    task_comp_df = pd.DataFrame(task_comparison).T
    task_comp_df = task_comp_df.applymap(lambda x: f"{x:.2%}" if pd.notnull(x) else "N/A")
    
    print("\n----- Task Performance Comparison -----")
    print(tabulate(task_comp_df, headers='keys', tablefmt='grid'))
    
    # Compare by prompt type
    prompt_comparison = {}
    for model, df in model_results.items():
        prompt_summary = df.groupby('prompt_type')['true_rate'].mean()
        for prompt, rate in prompt_summary.items():
            if prompt not in prompt_comparison:
                prompt_comparison[prompt] = {}
            prompt_comparison[prompt][model] = rate
    
    prompt_comp_df = pd.DataFrame(prompt_comparison).T
    prompt_comp_df = prompt_comp_df.applymap(lambda x: f"{x:.2%}" if pd.notnull(x) else "N/A")
    
    print("\n----- Prompt Performance Comparison -----")
    print(tabulate(prompt_comp_df, headers='keys', tablefmt='grid'))
    
    # Export comparison to CSV
    comparison_file = "model_comparison.csv"
    with open(comparison_file, 'w', encoding='utf-8') as f:
        f.write("Overall Success Rates\n")
        f.write(overall_df.to_csv(index=False))
        f.write("\nTask Performance Comparison\n")
        f.write(task_comp_df.to_csv())
        f.write("\nPrompt Performance Comparison\n")
        f.write(prompt_comp_df.to_csv())
    
    print(f"\nComparison data exported to {comparison_file}")
    
    # Generate comparison plots
    try:
        # Plot overall success rates
        plt.figure(figsize=(10, 6))
        bars = plt.bar(overall_rates.keys(), [rate * 100 for rate in overall_rates.values()])
        plt.xlabel('Model')
        plt.ylabel('Success Rate (%)')
        plt.title('Overall Success Rate Comparison')
        plt.xticks(rotation=45)
        
        # Add percentage labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig("model_comparison_overall.png")
        
        # Plot task comparison
        numeric_task_comp = pd.DataFrame({model: [float(str(rate).strip('%'))/100 
                                                if rate != "N/A" else 0 
                                                for rate in task_comp_df[model]] 
                                        for model in task_comp_df.columns})
        numeric_task_comp.index = task_comp_df.index
        
        plt.figure(figsize=(12, 8))
        numeric_task_comp.plot(kind='bar', figsize=(12, 8))
        plt.xlabel('Task')
        plt.ylabel('Success Rate')
        plt.title('Success Rate by Task Across Models')
        plt.legend(title='Model')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("model_comparison_by_task.png")
        
        # Plot prompt comparison
        numeric_prompt_comp = pd.DataFrame({model: [float(str(rate).strip('%'))/100 
                                                if rate != "N/A" else 0 
                                                for rate in prompt_comp_df[model]] 
                                        for model in prompt_comp_df.columns})
        numeric_prompt_comp.index = prompt_comp_df.index
        
        plt.figure(figsize=(12, 8))
        numeric_prompt_comp.plot(kind='bar', figsize=(12, 8))
        plt.xlabel('Prompt Type')
        plt.ylabel('Success Rate')
        plt.title('Success Rate by Prompt Type Across Models')
        plt.legend(title='Model')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("model_comparison_by_prompt.png")
        
        print(f"Comparison plots saved as model_comparison_overall.png, model_comparison_by_task.png, and model_comparison_by_prompt.png")
    except Exception as e:
        print(f"Error generating comparison plots: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analyze RGCI evaluation results')
    parser.add_argument('--model', type=str, help='Model name to analyze', default=None)
    parser.add_argument('--compare', type=str, nargs='+', help='List of models to compare')
    parser.add_argument('--dir', type=str, help='Custom evaluation directory', default=None)
    parser.add_argument('--format', choices=['text', 'csv'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    # Check if required dependencies are installed
    try:
        import tabulate
    except ImportError:
        print("The tabulate package is required. Please install it with:")
        print("pip install tabulate")
        return
    
    if args.compare:
        compare_models(args.compare)
    elif args.model:
        analyze_model_results(args.model, args.dir, args.format)
    else:
        # If no specific arguments, try to find available models
        models = get_available_models()
        if models:
            print(f"Available models: {', '.join(models)}")
            print("Use --model [MODEL_NAME] to analyze a specific model")
            print("Use --compare [MODEL1] [MODEL2] ... to compare models")
        else:
            print(f"No model directories found in {RESULT_DIR}")
            print("Please specify a model with --model or models to compare with --compare")

if __name__ == "__main__":
    main() 