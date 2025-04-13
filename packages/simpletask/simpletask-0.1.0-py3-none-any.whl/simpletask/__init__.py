from .scheduler import TaskScheduler

# Singleton global para simplificar el uso
_scheduler = TaskScheduler()

def task(interval=None, daily_at=None):
    def decorator(func):
        _scheduler.add_task(func, interval=interval, daily_at=daily_at)
        return func
    return decorator

def start_scheduler():
    _scheduler.start()

def stop_scheduler():
    _scheduler.stop()

__all__ = ["task", "start_scheduler", "stop_scheduler"]