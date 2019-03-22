from celery.schedules import crontab

BROKER_URL = "redis://localhost:6379/0"  # 指定 Broker  #192.168.30.152:6381
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"  # 指定 Backend

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC
# CELERY_TIMEZONE='UTC'

CELERY_IMPORTS = (  # 指定导入的任务模块
    'celery_app.task1',
    'celery_app.task2'
)

#定时任务
# schedules
CELERYBEAT_SCHEDULE = {
    'task1_scheduler': {
        'task': 'celery_app.task1.task_add',
        'schedule': 10, #每隔10秒执行x1任务
        'args': (5, 8)  # 任务函数参数
    },
    'task2_scheduler': {
        'task': 'celery_app.task2.multiple_add',
        'schedule': crontab(hour=12, minute=12),  # 每天早上 9 点 50 分执行一次
        'args': (3, 7)  # 任务函数参数
    }
}