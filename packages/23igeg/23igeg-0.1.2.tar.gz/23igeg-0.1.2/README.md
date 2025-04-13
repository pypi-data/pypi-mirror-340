
# 23igeg

**23igeg** è una libreria Python dimostrativa per la registrazione dei tasti (keylogging) a scopo educativo e di ricerca sulla sicurezza informatica.

## Avvertenze

- Utilizza questo codice solo in ambienti di test controllati e per scopi legali ed etici.
- L'uso di questa libreria per raccogliere informazioni senza il consenso delle persone è **illegale**.

## Installazione

Per installare la libreria, usa pip:

```
pip install 23igeg
```

## Uso

```python
from 23igeg.logger import KeyLogger

# Inizia la registrazione dei tasti
logger = KeyLogger("demo_log.txt")
logger.start()

# Premere tasti per registrare, interrompere con CTRL+C
```
