# flightpipe

End-to-end ADS-B flight data pipeline: resilient OpenSky ingestion, SQL storage, cleaning and
feature extraction, unsupervised trajectory anomaly detection evaluated against hand-labelled
data, served via FastAPI.

> **Status:** early development. See [PLAN.md](PLAN.md) for the staged plan and
> [DECISIONS.md](DECISIONS.md) for design decisions.

## Layout

```
src/flightpipe/
  ingest/    OpenSky client, retry and rate-limit handling
  db/        schema and storage
  clean/     cleaning rules and quarantine
  segment/   splitting streams into flights
  features/  vertical rate, turn rate, flight phase
  model/     anomaly detection and evaluation
  api/       FastAPI service
tests/       pytest suite
labels/      hand-labelled trajectories
frontend/    small map front end
```

## Development

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -e ".[dev]"
ruff check .
pytest
```

## Results

To be filled in once the evaluation harness exists: data-quality findings, precision / recall
against the hand-labelled set, false positive rate, and limitations.

## Licence

MIT
