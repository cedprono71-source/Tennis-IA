from db import init_db
import cotes
import suivi

init_db()
try:
    print("cotes :", cotes.maj_cotes())
except Exception as e:
    print("cotes : erreur", repr(e))
print("suivi :", suivi.cycle())
