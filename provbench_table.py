#!/usr/bin/env python3
"""provbench_table.py — Generate arXiv paper table from provbench canonical bound.

Structures the table from provbench-canonical-bound.json for the arXiv paper.

Usage:
    python3 provbench_table.py
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"


def load_canonical_bound() -> dict:
    """Load the canonical bound from provbench results."""
    path = RESULTS / "provbench-canonical-bound.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def generate_table() -> str:
    """Generate LaTeX table for arXiv paper."""
    data = load_canonical_bound()
    if not data:
        return "% No provbench-canonical-bound.json found"
    
    canonical = data["canonical"]
    
    table = r"""
\begin{table}[t]
\centering
\caption{Provenance Survival: C2PA Binding Survival Under Real-World Transforms}
\label{tab:provbench}
\begin{tabular}{lcc}
\toprule
\textbf{Metric} & \textbf{Value} & \textbf{95\% CI} \\
\midrule
Assets tested & \multicolumn{2}{c}{""" + str(canonical["n_assets"]) + r"""} \\
Survived (binding-intact) & """ + str(canonical["k"]) + r""" / """ + str(canonical["n_assets"]) + r""" & --- \\
\midrule
\multicolumn{3}{l}{\textit{Upper bound on survival rate (rule-of-three)}} \\
Rule-of-three (one-sided) & \multicolumn{2}{c}{""" + f"{canonical['rule_of_three_upper']:.1%}" + r"""} \\
Wilson (one-sided) & \multicolumn{2}{c}{""" + f"{canonical['wilson_one_sided_upper']:.1%}" + r"""} \\
Wilson (two-sided) & \multicolumn{2}{c}{""" + f"{canonical['wilson_two_sided_upper']:.1%}" + r"""} \\
\midrule
\multicolumn{3}{l}{\textit{Reconciliation with prior measurements}} \\
DR-0001 n=12 one-sided 24.2\% & \multicolumn{2}{c}{superseded by 11.9\%} \\
DR-0001 n=108 cell 3.43\% & \multicolumn{2}{c}{independence assumption invalid} \\
DR-0001 n=12 two-sided 22.1\% & \multicolumn{2}{c}{superseded by 16.1\%} \\
\bottomrule
\end{tabular}
\end{table}
"""
    return table


def generate_markdown() -> str:
    """Generate Markdown table for README/docs."""
    data = load_canonical_bound()
    if not data:
        return "No provbench-canonical-bound.json found"
    
    canonical = data["canonical"]
    
    table = f"""## Provenance Survival: C2PA Binding Survival Under Real-World Transforms

| Metric | Value | 95% CI |
|--------|-------|--------|
| Assets tested | {canonical['n_assets']} | --- |
| Survived (binding-intact) | {canonical['k']} / {canonical['n_assets']} | --- |
| **Upper bound on survival rate** | | |
| Rule-of-three (one-sided) | {canonical['rule_of_three_upper']:.1%} | --- |
| Wilson (one-sided) | {canonical['wilson_one_sided_upper']:.1%} | --- |
| Wilson (two-sided) | {canonical['wilson_two_sided_upper']:.1%} | --- |

### Reconciliation with prior measurements

| Prior measurement | Status |
|-------------------|--------|
| DR-0001 n=12 one-sided 24.2% | superseded by 11.9% |
| DR-0001 n=108 cell 3.43% | independence assumption invalid |
| DR-0001 n=12 two-sided 22.1% | superseded by 16.1% |
"""
    return table


def main():
    # Generate LaTeX table
    latex = generate_table()
    latex_path = RESULTS / "provbench_table.tex"
    latex_path.write_text(latex)
    print(f"LaTeX table written to: {latex_path}")
    
    # Generate Markdown table
    markdown = generate_markdown()
    md_path = RESULTS / "provbench_table.md"
    md_path.write_text(markdown)
    print(f"Markdown table written to: {md_path}")
    
    # Print summary
    data = load_canonical_bound()
    if data:
        c = data["canonical"]
        print(f"\nSummary:")
        print(f"  Assets: {c['n_assets']}")
        print(f"  Survived: {c['k']}")
        print(f"  Rule-of-three upper: {c['rule_of_three_upper']:.1%}")
        print(f"  Wilson one-sided: {c['wilson_one_sided_upper']:.1%}")


if __name__ == "__main__":
    main()
