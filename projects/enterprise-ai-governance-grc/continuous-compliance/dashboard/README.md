# Continuous Compliance Dashboard

From the `continuous-compliance` directory:

```bash
python tools/compliance_pipeline.py --sources data/source-findings.json --rules data/control-mappings.json --controls ../data/control-catalogue.json --output-dir reports
python -m http.server 8001
```

Open http://localhost:8001/dashboard/. The dashboard loads `reports/latest.json` from the local server. No remote scripts or services are used.
