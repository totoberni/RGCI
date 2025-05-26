# Extractor Bias Analysis Report

## Executive Summary

Analysis of potential bias in using different LLM extractors (GPT-4o vs o3-mini) for causal reasoning experiments with GPT-3.5-turbo.

### Key Findings

1. **Statistical Significance**: p-value = 0.0005 (paired t-test)
2. **Effect Size**: Cohen's d = 2.6129
3. **Consistency**: GPT-4o performs better in 7/7 tasks

## Overall Performance Metrics

| Metric | GPT-4o | o3-mini | Difference |
|--------|--------|---------|------------|
| Total True | 877 | 729 | +148 |
| Total False | 3323 | 3471 | -148 |
| Overall Accuracy | 0.209 | 0.174 | +0.035 |

## Task-by-Task Comparison

| Task | GPT-4o Accuracy | o3-mini Accuracy | Difference |
|------|-----------------|------------------|------------|
| mis_hint | 0.202 | 0.165 | +0.037 |
| one_cot | 0.235 | 0.182 | +0.053 |
| one_shot | 0.227 | 0.213 | +0.013 |
| two_cot | 0.228 | 0.183 | +0.045 |
| two_shot | 0.227 | 0.203 | +0.023 |
| zero_cot | 0.163 | 0.122 | +0.042 |
| zero_shot | 0.180 | 0.147 | +0.033 |

## Statistical Analysis

- **Paired t-test**: t = 6.9131, p = 0.0005
- **Wilcoxon test**: W = 0.0000, p = 0.0156
- **Effect Size (Cohen's d)**: 2.6129

## Model Comparison Summary

- GPT-4o performs better: 7 tasks
- o3-mini performs better: 0 tasks
- Equal performance: 0 tasks

## Conclusion

The analysis reveals a significant systematic bias when using different LLM models as extractors in causal reasoning experiments.
