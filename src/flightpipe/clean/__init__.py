"""Stage 2: cleaning.

Purpose: dedupe, repair ordering, plausibility filters (speed, climb rate, position jumps),
baro/geo altitude reconciliation. Every rule is a tested function with a logged counter;
rejected rows go to quarantine with a reason code, never silently deleted.

Exit criteria: data-quality report (counts by reason code).
"""
