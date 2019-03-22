import time
from celery_app import app
@app.task
def task_add(arg1, arg2):
    print('Enter the function of task_add')
    time.sleep(3)
    result = arg1 + arg2
    return result