import json
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid window popup
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
from scipy import stats

# Define the paths to the evaluation folders
GPT4O_EVAL_PATH = "../data/generated_data/result/gpt-3.5-turbo/eval"
O3_MINI_EVAL_PATH = "../data/generated_data/result/gpt-3.5-turbo1/eval"
OUTPUT_DIR = "../data/compare_data"

def ensure_output_dir():
    """Ensure the output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_evaluation_results(folder_path):
    """Load evaluation results from JSONL files in the specified folder."""
    results = {}
    
    # Get all JSON files in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        task_name = file_name.replace('.json', '')
        
        # Read JSONL file
        true_count = 0
        false_count = 0
        
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if data['result']:
                        true_count += 1
                    else:
                        false_count += 1
                except json.JSONDecodeError:
                    print(f"Error parsing line in {file_name}")
                    continue
        
        results[task_name] = {
            'true': true_count,
            'false': false_count,
            'total': true_count + false_count,
            'accuracy': true_count / (true_count + false_count) if (true_count + false_count) > 0 else 0
        }
    
    return results

def compare_models():
    """Compare evaluation results between GPT-4o and o3-mini models."""
    print("Loading GPT-4o evaluation results...")
    gpt4o_results = load_evaluation_results(GPT4O_EVAL_PATH)
    
    print("Loading o3-mini evaluation results...")
    o3_mini_results = load_evaluation_results(O3_MINI_EVAL_PATH)
    
    # Find common tasks
    common_tasks = set(gpt4o_results.keys()) & set(o3_mini_results.keys())
    print(f"\nFound {len(common_tasks)} common tasks between both models")
    
    # Print summary statistics
    print("\n" + "="*80)
    print("EVALUATION SUMMARY")
    print("="*80)
    
    for task in sorted(common_tasks):
        print(f"\nTask: {task}")
        print(f"  GPT-4o:  True={gpt4o_results[task]['true']:4d}, False={gpt4o_results[task]['false']:4d}, "
              f"Accuracy={gpt4o_results[task]['accuracy']:.3f}")
        print(f"  o3-mini: True={o3_mini_results[task]['true']:4d}, False={o3_mini_results[task]['false']:4d}, "
              f"Accuracy={o3_mini_results[task]['accuracy']:.3f}")
        print(f"  Difference in accuracy: {gpt4o_results[task]['accuracy'] - o3_mini_results[task]['accuracy']:.3f}")
    
    return gpt4o_results, o3_mini_results, common_tasks

def create_comparison_plots(gpt4o_results, o3_mini_results, common_tasks):
    """Create comparative visualizations for the two models."""
    ensure_output_dir()  # Make sure output directory exists
    
    tasks = sorted(common_tasks)
    
    # Prepare data for plotting
    gpt4o_true = [gpt4o_results[task]['true'] for task in tasks]
    gpt4o_false = [gpt4o_results[task]['false'] for task in tasks]
    o3_mini_true = [o3_mini_results[task]['true'] for task in tasks]
    o3_mini_false = [o3_mini_results[task]['false'] for task in tasks]
    
    gpt4o_accuracy = [gpt4o_results[task]['accuracy'] for task in tasks]
    o3_mini_accuracy = [o3_mini_results[task]['accuracy'] for task in tasks]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Comparison of GPT-4o vs o3-mini as Extractors', fontsize=16)
    
    # 1. Side-by-side bar chart for accuracy
    ax1 = axes[0, 0]
    x = np.arange(len(tasks))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, gpt4o_accuracy, width, label='GPT-4o', alpha=0.8)
    bars2 = ax1.bar(x + width/2, o3_mini_accuracy, width, label='o3-mini', alpha=0.8)
    
    ax1.set_xlabel('Task')
    ax1.set_ylabel('Accuracy')
    ax1.set_title('Accuracy Comparison by Task')
    ax1.set_xticks(x)
    ax1.set_xticklabels([task.replace('conf_ce_path_00_specific_', '') for task in tasks], rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
    
    # 2. Stacked bar chart for true/false counts
    ax2 = axes[0, 1]
    
    # Create stacked bars for GPT-4o
    bars1 = ax2.bar(x - width/2, gpt4o_true, width, label='GPT-4o True', color='green', alpha=0.8)
    bars2 = ax2.bar(x - width/2, gpt4o_false, width, bottom=gpt4o_true, label='GPT-4o False', color='red', alpha=0.8)
    
    # Create stacked bars for o3-mini
    bars3 = ax2.bar(x + width/2, o3_mini_true, width, label='o3-mini True', color='darkgreen', alpha=0.8)
    bars4 = ax2.bar(x + width/2, o3_mini_false, width, bottom=o3_mini_true, label='o3-mini False', color='darkred', alpha=0.8)
    
    ax2.set_xlabel('Task')
    ax2.set_ylabel('Count')
    ax2.set_title('True/False Count Distribution by Task')
    ax2.set_xticks(x)
    ax2.set_xticklabels([task.replace('conf_ce_path_00_specific_', '') for task in tasks], rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Accuracy difference plot
    ax3 = axes[1, 0]
    accuracy_diff = [gpt4o_accuracy[i] - o3_mini_accuracy[i] for i in range(len(tasks))]
    colors = ['green' if diff > 0 else 'red' for diff in accuracy_diff]
    
    bars = ax3.bar(x, accuracy_diff, color=colors, alpha=0.8)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax3.set_xlabel('Task')
    ax3.set_ylabel('Accuracy Difference (GPT-4o - o3-mini)')
    ax3.set_title('Accuracy Difference by Task')
    ax3.set_xticks(x)
    ax3.set_xticklabels([task.replace('conf_ce_path_00_specific_', '') for task in tasks], rotation=45, ha='right')
    ax3.grid(True, alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax3.annotate(f'{height:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height > 0 else -15),
                    textcoords="offset points",
                    ha='center', va='bottom' if height > 0 else 'top', fontsize=8)
    
    # 4. Overall statistics
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Calculate overall statistics
    total_gpt4o_true = sum(gpt4o_true)
    total_gpt4o_false = sum(gpt4o_false)
    total_o3_mini_true = sum(o3_mini_true)
    total_o3_mini_false = sum(o3_mini_false)
    
    overall_gpt4o_accuracy = total_gpt4o_true / (total_gpt4o_true + total_gpt4o_false)
    overall_o3_mini_accuracy = total_o3_mini_true / (total_o3_mini_true + total_o3_mini_false)
    
    stats_text = f"""Overall Statistics:
    
    GPT-4o Extractor:
    - Total True: {total_gpt4o_true}
    - Total False: {total_gpt4o_false}
    - Overall Accuracy: {overall_gpt4o_accuracy:.3f}
    
    o3-mini Extractor:
    - Total True: {total_o3_mini_true}
    - Total False: {total_o3_mini_false}
    - Overall Accuracy: {overall_o3_mini_accuracy:.3f}
    
    Difference:
    - Accuracy Difference: {overall_gpt4o_accuracy - overall_o3_mini_accuracy:.3f}
    - True Count Difference: {total_gpt4o_true - total_o3_mini_true}
    - False Count Difference: {total_gpt4o_false - total_o3_mini_false}
    """
    
    ax4.text(0.1, 0.5, stats_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='center', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'extractor_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    print(f"  - Saved comparison plot to: {output_path}")
    
    return accuracy_diff

def perform_statistical_analysis(gpt4o_results, o3_mini_results, common_tasks):
    """Perform statistical analysis to detect systemic bias."""
    tasks = sorted(common_tasks)
    
    # Prepare data for analysis
    gpt4o_accuracies = [gpt4o_results[task]['accuracy'] for task in tasks]
    o3_mini_accuracies = [o3_mini_results[task]['accuracy'] for task in tasks]
    
    print("\n" + "="*80)
    print("STATISTICAL ANALYSIS")
    print("="*80)
    
    # 1. Paired t-test (since we're comparing the same tasks)
    t_stat, p_value = stats.ttest_rel(gpt4o_accuracies, o3_mini_accuracies)
    print(f"\nPaired t-test:")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Significant difference? {'Yes' if p_value < 0.05 else 'No'} (α=0.05)")
    
    # 2. Wilcoxon signed-rank test (non-parametric alternative)
    w_stat, w_p_value = stats.wilcoxon(gpt4o_accuracies, o3_mini_accuracies)
    print(f"\nWilcoxon signed-rank test:")
    print(f"  W-statistic: {w_stat:.4f}")
    print(f"  p-value: {w_p_value:.4f}")
    print(f"  Significant difference? {'Yes' if w_p_value < 0.05 else 'No'} (α=0.05)")
    
    # 3. Effect size (Cohen's d)
    diff = np.array(gpt4o_accuracies) - np.array(o3_mini_accuracies)
    cohens_d = np.mean(diff) / np.std(diff, ddof=1)
    print(f"\nEffect size (Cohen's d): {cohens_d:.4f}")
    print(f"  Interpretation: ", end="")
    if abs(cohens_d) < 0.2:
        print("Small effect")
    elif abs(cohens_d) < 0.5:
        print("Medium effect")
    else:
        print("Large effect")
    
    # 4. Consistency analysis
    print("\n" + "-"*40)
    print("Consistency Analysis:")
    
    # Count how often each model performs better
    gpt4o_better = sum(1 for i in range(len(tasks)) if gpt4o_accuracies[i] > o3_mini_accuracies[i])
    o3_mini_better = sum(1 for i in range(len(tasks)) if o3_mini_accuracies[i] > gpt4o_accuracies[i])
    equal_performance = len(tasks) - gpt4o_better - o3_mini_better
    
    print(f"  GPT-4o performs better: {gpt4o_better}/{len(tasks)} tasks ({gpt4o_better/len(tasks)*100:.1f}%)")
    print(f"  o3-mini performs better: {o3_mini_better}/{len(tasks)} tasks ({o3_mini_better/len(tasks)*100:.1f}%)")
    print(f"  Equal performance: {equal_performance}/{len(tasks)} tasks ({equal_performance/len(tasks)*100:.1f}%)")
    
    # 5. Task-specific bias analysis
    print("\n" + "-"*40)
    print("Task-Specific Bias Analysis:")
    
    task_biases = {}
    for task in tasks:
        bias = gpt4o_results[task]['accuracy'] - o3_mini_results[task]['accuracy']
        task_biases[task] = bias
    
    # Sort tasks by bias magnitude
    sorted_biases = sorted(task_biases.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print("\nTasks with largest bias (top 3):")
    for i, (task, bias) in enumerate(sorted_biases[:3]):
        task_short = task.replace('conf_ce_path_00_specific_', '')
        print(f"  {i+1}. {task_short}: {bias:+.3f} ({'GPT-4o' if bias > 0 else 'o3-mini'} better)")
    
    return {
        'paired_t_test': {'t_stat': t_stat, 'p_value': p_value},
        'wilcoxon_test': {'w_stat': w_stat, 'p_value': w_p_value},
        'cohens_d': cohens_d,
        'model_comparison': {
            'gpt4o_better': gpt4o_better,
            'o3_mini_better': o3_mini_better,
            'equal': equal_performance
        },
        'task_biases': task_biases
    }

def suggest_further_analysis():
    """Suggest additional analyses for detecting systemic bias."""
    print("\n" + "="*80)
    print("SUGGESTED FURTHER ANALYSES")
    print("="*80)
    
    suggestions = """
1. Error Pattern Analysis:
   - Analyze the types of errors each model makes
   - Check if certain question patterns lead to consistent failures
   - Look for correlations between error types and extractor models

2. Confidence Score Analysis (if available):
   - Compare confidence scores between extractors
   - Check if one model is systematically more/less confident
   - Analyze correlation between confidence and accuracy

3. Response Time Analysis:
   - Compare processing times between models
   - Check if speed-accuracy trade-offs differ

4. Cross-validation Study:
   - Use different base models (not just GPT-3.5-turbo)
   - Test on different question types or domains
   - Perform k-fold cross-validation

5. Bias Detection Metrics:
   - Calculate fairness metrics (e.g., demographic parity)
   - Perform adversarial testing
   - Check for systematic biases in specific question categories

6. Longitudinal Analysis:
   - Track performance over time
   - Check for drift in model behavior
   - Analyze consistency across different API versions

7. Feature Importance Analysis:
   - Identify which question features correlate with extractor disagreement
   - Use interpretability techniques to understand decision patterns
   - Perform ablation studies on question components
"""
    print(suggestions)

def save_analysis_report(gpt4o_results, o3_mini_results, stats_results, common_tasks):
    """Save analysis report as a markdown file."""
    ensure_output_dir()
    
    tasks = sorted(common_tasks)
    
    # Calculate overall statistics
    total_gpt4o_true = sum(gpt4o_results[task]['true'] for task in tasks)
    total_gpt4o_false = sum(gpt4o_results[task]['false'] for task in tasks)
    total_o3_mini_true = sum(o3_mini_results[task]['true'] for task in tasks)
    total_o3_mini_false = sum(o3_mini_results[task]['false'] for task in tasks)
    
    overall_gpt4o_accuracy = total_gpt4o_true / (total_gpt4o_true + total_gpt4o_false)
    overall_o3_mini_accuracy = total_o3_mini_true / (total_o3_mini_true + total_o3_mini_false)
    
    report_content = f"""# Extractor Bias Analysis Report

## Executive Summary

Analysis of potential bias in using different LLM extractors (GPT-4o vs o3-mini) for causal reasoning experiments with GPT-3.5-turbo.

### Key Findings

1. **Statistical Significance**: p-value = {stats_results['paired_t_test']['p_value']:.4f} (paired t-test)
2. **Effect Size**: Cohen's d = {stats_results['cohens_d']:.4f}
3. **Consistency**: GPT-4o performs better in {stats_results['model_comparison']['gpt4o_better']}/{len(tasks)} tasks

## Overall Performance Metrics

| Metric | GPT-4o | o3-mini | Difference |
|--------|--------|---------|------------|
| Total True | {total_gpt4o_true} | {total_o3_mini_true} | {total_gpt4o_true - total_o3_mini_true:+d} |
| Total False | {total_gpt4o_false} | {total_o3_mini_false} | {total_gpt4o_false - total_o3_mini_false:+d} |
| Overall Accuracy | {overall_gpt4o_accuracy:.3f} | {overall_o3_mini_accuracy:.3f} | {overall_gpt4o_accuracy - overall_o3_mini_accuracy:+.3f} |

## Task-by-Task Comparison

| Task | GPT-4o Accuracy | o3-mini Accuracy | Difference |
|------|-----------------|------------------|------------|
"""
    
    for task in tasks:
        task_short = task.replace('conf_ce_path_00_specific_', '')
        report_content += f"| {task_short} | {gpt4o_results[task]['accuracy']:.3f} | {o3_mini_results[task]['accuracy']:.3f} | {gpt4o_results[task]['accuracy'] - o3_mini_results[task]['accuracy']:+.3f} |\n"
    
    report_content += f"""
## Statistical Analysis

- **Paired t-test**: t = {stats_results['paired_t_test']['t_stat']:.4f}, p = {stats_results['paired_t_test']['p_value']:.4f}
- **Wilcoxon test**: W = {stats_results['wilcoxon_test']['w_stat']:.4f}, p = {stats_results['wilcoxon_test']['p_value']:.4f}
- **Effect Size (Cohen's d)**: {stats_results['cohens_d']:.4f}

## Model Comparison Summary

- GPT-4o performs better: {stats_results['model_comparison']['gpt4o_better']} tasks
- o3-mini performs better: {stats_results['model_comparison']['o3_mini_better']} tasks
- Equal performance: {stats_results['model_comparison']['equal']} tasks

## Conclusion

The analysis reveals a {'significant' if stats_results['paired_t_test']['p_value'] < 0.05 else 'non-significant'} systematic bias when using different LLM models as extractors in causal reasoning experiments.
"""
    
    # Save report
    report_path = os.path.join(OUTPUT_DIR, 'analysis_report.md')
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"  - Saved analysis report to: {report_path}")

def main():
    """Main function to run the complete analysis."""
    print("Starting Extractor Bias Analysis...")
    print("="*80)
    
    # Load and compare results
    gpt4o_results, o3_mini_results, common_tasks = compare_models()
    
    # Create visualizations
    print("\nCreating comparison plots...")
    accuracy_diff = create_comparison_plots(gpt4o_results, o3_mini_results, common_tasks)
    
    # Perform statistical analysis
    stats_results = perform_statistical_analysis(gpt4o_results, o3_mini_results, common_tasks)
    
    # Save analysis report
    print("\nSaving analysis report...")
    save_analysis_report(gpt4o_results, o3_mini_results, stats_results, common_tasks)
    
    # Suggest further analyses
    suggest_further_analysis()
    
    print("\nAnalysis complete!")
    print(f"Results saved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main() 