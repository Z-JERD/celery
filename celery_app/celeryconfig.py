from kombu import Queue
from celery.schedules import crontab

BROKER_URL = "redis://localhost:6379/0"                     # 指定 Broker  #192.168.30.152:6381
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"          # 指定 Backend    redis://:xxxxx@localhost:6379/1,

CELERY_TIMEZONE = 'Asia/Shanghai'                           # 指定时区，默认是 UTC
CELERY_ENABLE_UTC = True                                    # 启动时区设置
CELERY_TASK_SERIALIZER = 'msgpack'                          # 任务序列化和反序列化使用msgpack方案
CELERY_RESULT_SERIALIZER = 'json'                           # 读取任务结果

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24                   # 任务过期时间
CELERYD_CONCURRENCY = 50                                    # celery worker的并发数
CELERYD_PREFETCH_MULTIPLIER = 4                             # celery worker每次去redis取任务的数量，默认值就是4
CELERYD_MAX_TASKS_PER_CHILD = 200                           # 每个worker执行了多少任务就会死掉，默认是无限的
CELERY_DEFAULT_QUEUE = "default"                            # 默认的队列名称

# 定义任务队列
CELERY_QUEUES = (  # 定义任务队列
    Queue("default", routing_key="task.#"),                 # 路由键以“task.”开头的消息都进default队列
    Queue("tasks_add", routing_key="A.task"),               # 路由键为“A.task”的消息都进tasks_add队列
    Queue("tasks_multiple_add", routing_key="B.task"),      # 路由键以“B.task”开头的消息都进tasks_multiple_add队列
)

# 为不同的task指派不同的队列
CELERY_ROUTES = {
    'celery_app.task1.task_add': {
        'queue': "tasks_add",
        'routing_key': 'A.task',
    },
    'celery_app.task2.multiple_add': {
        'queue': 'tasks_multiple_add',
        'routing_key': 'B.task',
    }
}

# Celery在启动时 会自动找到这些模块， 并导入模块内的task
CELERY_IMPORTS = (
    'celery_app.task1',
    'celery_app.task2'
)

# 定时任务
CELERYBEAT_SCHEDULE = {

    'task1_scheduler': {                                    # 计划任务名称
        'task': 'celery_app.task1.task_add',                # 执行计划任务的函数
        'schedule': 10,                                     # 计划任务的执行时间  每隔10秒
        'args': (5, 8)                                      # 任务函数参数
    },
    'task2_scheduler': {
        'task': 'celery_app.task2.multiple_add',
        'schedule': crontab(hour=12, minute=12),            # 每天12 点 12 分执行一次  crontab更详细的配置参考文档
        'args': (3, 7)                                      # 任务函数参数
    }
}
