#celery配置
import djcelery
from celery.schedules import crontab

djcelery.setup_loader()
CELERY_QUEUES = {
    #定时任务时用的队列
    'beat_tasks':{
        'exchange': 'beat_tasks',
        'exchange_type':'direct',
        'binding_key':'beat_tasks'
    },
    #普通任务时用的队列
    'work_queue': {
        'exchange': 'work_queue',
        'exchange_type': 'direct',
        'binding_key': 'work_queue'
    },
}
CELERY_DEFAULT_QUEUE = 'work_queue'

BROKER_BACKEND = 'redis'
BROKER_URL = "redis://192.168.30.152:6381/0"  #"redis://:123456789@10.110.1.230:6379/0"
CELERY_RESULT_BACKEND = "redis://192.168.30.152:6381/1"
CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC


CELERY_IMPORTS = (  # 指定导入的任务模块
    'celerydemo.task1',
)

#防止死锁
CELERYD_FORCE_EXECV = True

#设置并发的Worker数量
CELERYD_CONCURRENCY = 4

#允许重试
CELERY_ACKS_LATE = True

#每个worker最多执行100个任务后被销毁，防止内存泄漏
CELERYD_MAX_TASKS_PER_CHILD = 100

#单个任务的最大运行时间
CELERYD_TASK_TIME_LIMIT = 12 *30

#定时任务
# schedules
CELERYBEAT_SCHEDULE = {
    'task1_scheduler': {
        'task': 'cycle-task',
        'schedule': 10, #每隔10秒执行x1任务 注意不能为浮点型数据
        'args': (5, 8), # 任务函数参数
        #指定队列：
        'options':{
            'queue':'beat_tasks',
        }
    },
    'task2_scheduler': {
        'task': 'time-task',
        'schedule': crontab(hour=12, minute=12),  # 每天早上 9 点 50 分执行一次
        'args': ('HELLO', 'WORLD')  # 任务函数参数
    }
}


