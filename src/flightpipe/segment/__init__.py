"""Stage 2: flight segmentation.

Purpose: split each aircraft's stream into flights by time gap, ground transitions and
callsign change. Justify the gap threshold in DECISIONS.md.

Exit criteria: `flights` table with sensible duration/length distributions.
"""
