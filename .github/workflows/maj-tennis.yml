"""Lancé par GitHub Actions : met à jour les cotes françaises, les pronostics et les résultats."""
from db import init_db
import cotes
import suivi

init_db()
try:
    print("cotes :", cotes.maj_cotes())
except Exception as e:  # noqa: BLE001
    print("cotes : erreur", repr(e))
print("suivi :", suivi.cycle())

