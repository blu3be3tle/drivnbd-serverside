# api/wsgi.py — Vercel serverless entrypoint that reuses your Django WSGI app
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # add project root to PYTHONPATH
from drivnbd.wsgi import app  # imports the `app` alias from your real wsgi