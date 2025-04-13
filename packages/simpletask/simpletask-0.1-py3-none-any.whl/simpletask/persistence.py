# Base para futuras integraciones con PostgreSQL/MySQL
class BasePersistor:
    def save_task_state(self, task):
        raise NotImplementedError

class SQLitePersistor(BasePersistor):
    # ... (similar al código en scheduler.py)
    pass