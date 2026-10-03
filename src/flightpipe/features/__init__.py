"""Stage 3: feature extraction.

Purpose: per-point vertical rate, turn rate (angle wrapping!), acceleration; rule-based flight
phase with hysteresis; per-flight summary features.

Exit criteria: `flight_features` table; synthetic-trajectory tests pass (constant climb,
360-degree circle); phase plots look right by eye.
"""
