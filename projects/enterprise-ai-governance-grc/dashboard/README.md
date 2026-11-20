# Dashboard

From the project root, generate the report and serve the folder:

```bash
python tools/governance_engine.py --inventory data/ai-inventory.json --controls data/control-catalogue.json --output-dir reports
python -m http.server 8000
```

Open http://localhost:8000/dashboard/. The page reads the generated `reports/latest.json` file through the local HTTP server. It uses no external libraries or remote services.
