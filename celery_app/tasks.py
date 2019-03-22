from celery import Celery

CELERY_BROKER_URL = 'redis://localhost:6379/0'
#BROKER_URL = 'redis://:密码@主机地址:端口号/数据库号'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

celeryapp= Celery('task0', broker=CELERY_BROKER_URL,backend=CELERY_RESULT_BACKEND)
#任何你需要作为后台任务的函数需要用 celery.task 装饰器装饰
@celeryapp.task
def my_background_task(arg1, arg2):
    result = arg1 + arg2
    return result

