"""Stages 4-5: labels, evaluation and anomaly model.

Purpose: baseline threshold detector, then Isolation Forest / LOF / GMM. Labels are used only
for evaluation. Evaluation reports precision, recall, PR-AUC, precision@k, false positives per
1,000 flights, with bootstrap CIs. Split by date or airport, not random rows.

Exit criteria: results table (baseline vs models) plus a limitations paragraph.
"""
