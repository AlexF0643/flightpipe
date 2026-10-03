"""Stage 1: schema and storage.

Purpose: tables `raw_states` (immutable, append-only), `ingest_runs`, `clean_states`,
`quarantine`, `flights`, `flight_features`, `anomaly_scores`. Keep SQL Postgres-portable.

Exit criteria: schema created from code; unique key makes re-ingest idempotent.
"""
