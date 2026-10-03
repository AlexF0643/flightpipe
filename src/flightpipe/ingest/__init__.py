"""Stage 1: OpenSky ingestion.

Purpose: fetch state vectors with retry/backoff, 429 + Retry-After handling and a credit
budget, then append them idempotently to `raw_states`.

Exit criteria: collector runs unattended for 24h with a clean `ingest_runs` log; tests cover
429, timeouts, malformed JSON and null fields.
"""
