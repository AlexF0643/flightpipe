# flightpipe: Project Plan

An end-to-end ADS-B pipeline over OpenSky data: resilient ingestion, SQL storage, cleaning and
feature extraction, unsupervised trajectory anomaly detection evaluated against hand-labelled
data, served by FastAPI with a small front end and CI. Budget: **40 hours**.

**Rule:** do not start a stage until the previous stage's exit criteria pass.

## Success criteria

- [ ] A fresh clone runs `ingest -> clean -> features -> score` from the README.
- [ ] Tests run green in CI on every push.
- [ ] At least 300 hand-labelled trajectories are committed, with precision, recall, PR-AUC and
      false positives per 1,000 flights reported (with confidence intervals).
- [ ] The API serves "most anomalous flights" and a per-flight trajectory view.
- [ ] A short write-up states honestly what the model does and does not catch.

## Architecture

```
OpenSky API -> ingest -> raw_states (append-only, never edited)
                            |
                         clean -> clean_states + quarantine (reason codes)
                            |
                        segment -> flights
                            |
                        features -> flight_features
                            |
                    model + labels -> anomaly_scores
                            |
                     FastAPI -> front end
```

Principle: `raw_states` is immutable. Every later stage is reproducible from it, and every
cleaning decision is logged rather than silently applied.

## Stack decisions

| Decision | Choice |
|---|---|
| Database | SQLite first, schema kept Postgres-portable |
| Tools | Python 3.11+, httpx, pandas, SQLAlchemy, scikit-learn, FastAPI, pytest, ruff, GitHub Actions |
| Region | One bounded box (to be chosen in Stage 0) |
| Front end | Plain HTML + Leaflet |

## Stages

### Stage 0: Setup and reconnaissance (3 h)
- [ ] Environment, `ruff`, `pytest`; CI green on the smoke test
- [ ] OpenSky account; read current API docs (auth, credits, history limits: verify, don't assume)
- [ ] One manual API call; save the raw response under `data/`
- [ ] Choose region and compute the daily credit budget

**Exit:** green CI badge and one saved raw response.

### Stage 1: Ingestion and storage (8 h)
- [ ] Schema: `raw_states`, `ingest_runs`
- [ ] Client: retry with exponential backoff + jitter, 429 / `Retry-After`, credit tracker
- [ ] Idempotent inserts (unique key on `icao24, time_position, fetched_at`)
- [ ] Polling loop for the bounding box
- [ ] Tests with mocked HTTP: 429, timeouts, malformed JSON, nulls

**Exit:** collector runs unattended 24 h with a clean `ingest_runs` log; failure modes tested.
Start collecting early and leave it running while building later stages.

### Stage 2: Cleaning and segmentation (6 h)
- [ ] Profile the mess in a notebook (null, duplicate, out-of-order, gap, jump rates)
- [ ] Rules: dedupe, ordering, plausibility (speed, climb rate, implied ground speed),
      baro/geo altitude reconciliation, `on_ground` handling
- [ ] Each rule is a function with a unit test and a log counter
- [ ] Quarantine table with reason codes
- [ ] Segmentation by time gap, ground transitions, callsign change; justify threshold

**Exit:** data-quality report and a `flights` table with sensible distributions.

### Stage 3: Feature extraction (5 h)
- [ ] Vertical rate (derived vs reported), turn rate (angle wrapping), acceleration
- [ ] Rule-based flight phase with hysteresis
- [ ] Per-flight summary features
- [ ] Synthetic-trajectory tests (constant climb, 360-degree circle)

**Exit:** `flight_features` table; phase plots look right by eye.

### Stage 4: Labelling and evaluation harness (5 h)
- [ ] Written labelling rubric in the repo
- [ ] Labelling tool (map + altitude profile)
- [ ] Stratified sampling with recorded weights; label blind to model scores
- [ ] 300+ labels committed to `labels/labels.csv`
- [ ] Synthetic injected-anomaly validation set (kept separate)
- [ ] `evaluate.py`: precision, recall, PR-AUC, precision@k, FP per 1,000, bootstrap CIs

**Exit:** labels committed and the harness runs on any score column.

### Stage 5: Anomaly model (6 h)
- [ ] Baseline: threshold / z-score rules
- [ ] Isolation Forest, LOF, GMM (stretch: sequence autoencoder)
- [ ] Split by date or airport, not random rows
- [ ] Per-category results and failure analysis of top false positives and misses
- [ ] Scores saved to `anomaly_scores` with a model version

**Exit:** results table (baseline vs models) with CIs, plus a limitations paragraph.

### Stage 6: API and front end (4 h)
- [ ] `GET /flights`, `GET /flights/{id}`, `GET /health`
- [ ] Pydantic response models; `TestClient` tests on a fixture database
- [ ] Table + map + altitude profile; show top contributing features per flag

**Exit:** `uvicorn` serves a working demo from README instructions.

### Stage 7: CI, docs, write-up (3 h)
- [ ] CI: lint, tests, pipeline smoke test on a small committed fixture (never live API calls)
- [ ] README: architecture, quickstart, data-quality findings, results, limitations
- [ ] Dockerfile; optional free-tier deploy
- [ ] One-page write-up

## Hour budget

| Stage | Hours |
|---|---|
| 0 Setup | 3 |
| 1 Ingestion and storage | 8 |
| 2 Cleaning and segmentation | 6 |
| 3 Features | 5 |
| 4 Labelling and evaluation | 5 |
| 5 Model | 6 |
| 6 API and front end | 4 |
| 7 CI, docs, write-up | 3 |
| **Total** | **40** |

No slack. Cut the autoencoder and the Postgres move first if Stages 1-2 overrun.

## Risks

1. **Historical data access.** The free API mostly offers current states with limited history;
   deep history needs approved researcher access. Confirm in Stage 0. Fallbacks: collect your own
   history over weeks, or apply for researcher access.
2. **API credit limits.** Compute the budget before choosing the polling interval.
3. **Terms of use.** Check OpenSky's redistribution terms; commit only small fixtures or derived
   data, never raw dumps.
4. **Too few real anomalies.** Use stratified sampling and report counts openly.
5. **Cleaning artefacts masquerading as anomalies.** Likely in failure analysis; say so.
6. **Label bias and small sample.** State confidence interval widths.

## Working split (you write, Claude reviews)

| Stage | You write | Claude helps with |
|---|---|---|
| 1 | Schema, client, retry logic | Edge cases, test mocks, credit math |
| 2 | Rules and segmentation | Profiling ideas, adversarial test cases |
| 3 | Features and phase classifier | Angle wrapping, hysteresis pitfalls, synthetic trajectories |
| 4 | The labelling itself | Sampling design, harness, bootstrap CIs |
| 5 | Model choice and interpretation | Scaffolding, failure-analysis structure |
| 6 | Endpoints | Front-end boilerplate |
| 7 | README prose | CI YAML, Dockerfile |
