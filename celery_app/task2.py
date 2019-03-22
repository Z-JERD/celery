import time
from celery_app import app
@app.task
def multiple_add(args1,args2):
    print('Enter the function of multiple_add')
    time.sleep(4)
    result = args1 + args2
    return result
