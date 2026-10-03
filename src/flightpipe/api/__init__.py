"""Stage 6: FastAPI service.

Purpose: GET /flights (filter by score/date), GET /flights/{id} (trajectory, features, score,
explanation), GET /health. Pydantic response models.

Exit criteria: `uvicorn` serves a working demo; TestClient tests run on a fixture database.
"""
