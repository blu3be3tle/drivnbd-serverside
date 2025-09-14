# api/wsgi.py — Vercel entrypoint that wraps your Django project
import os
import sys

# Ensure project root is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from drivnbd.wsgi import application as app  # Vercel expects `app`