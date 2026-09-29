# Web Interface (Flask)

A small Flask front end for the Stage 1 order price calculator
(`price_calculator.py`). Enter number of items, unit price, country, and
an optional order date; get back the same priced-order breakdown as the
CLI `--interactive` mode, rendered as a receipt.

This wraps the existing `process_4_priced_order()` — no pricing logic is
duplicated here.

## Run locally

It's recommended to use a virtual environment so these packages don't
get installed globally.

**Windows (PowerShell)**

```
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**macOS / Linux**

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

To leave the virtual environment when you're done: `deactivate`

`app.run(debug=True)` is used for local development only.

## Files

- `app.py` — Flask app: one route (`/`) handling GET (show form) and POST
  (validate input, calculate, show receipt).
- `templates/index.html` — form + receipt table.
- `static/style.css` — styling.

## Notes

- Only Stage 1 (single-order calculator) is exposed. The Stage 2 report
  (`index.html`, sales history, charts) is still generated separately by
  `stage2_run_all.py` and viewed as a static file.
- The dev server (`flask run` / `app.run(debug=True)`) is not meant for
  production. Deployment to an Azure VM (production WSGI server, etc.)
  will be covered separately once ready.
