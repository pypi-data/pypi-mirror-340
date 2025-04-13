
from 23igeg.logger import KeyLogger
import time

def test_keylogger():
    logger = KeyLogger("test_log.txt")
    logger.start()
    
    time.sleep(2)  # Tempo per registrare i tasti
    
    logger.stop()
    log_data = logger.read_log()
    
    assert len(log_data) > 0, "Il log è vuoto!"
    print("Test superato!")
    
test_keylogger()
