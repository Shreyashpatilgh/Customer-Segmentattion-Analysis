# Airlines Customer Segmentation

Streamlit application for airline customer analytics, segmentation, prediction,
ticket management, and administrative reporting.

## Run locally

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SMTP_EMAIL="your-email@gmail.com"
$env:SMTP_APP_PASSWORD="your-gmail-app-password"
streamlit run app.py
```

Large generated CSV files and local SQLite databases are excluded from Git.
