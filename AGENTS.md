# Agent Guide — app-dakota-eviction

## Scope
Quad-lingual interactive eviction defense system for Dakota County, Minnesota tenants.
English, Spanish, Somali, Arabic.

## Key paths
- `semptify_dakota_eviction/app/` — FastAPI app
- `semptify_dakota_eviction/app/main.py` — entry point
- `semptify_dakota_eviction/app/routes/` — flows and forms
- `semptify_dakota_eviction/app/services/` — i18n, PDF, ZIP
- `run.py` — launcher

## Working rules
- This is a Semptify-adjacent module: public-service, no accounts, no tracking, no dark patterns.
- Do not hardcode court URLs or resource phone numbers; keep them in config/data files.
- No PII or case data in commits.

## Local run
```powershell
pip install -r requirements.txt
python run.py
```
Server starts at `http://localhost:8001`.
