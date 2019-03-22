celery4.0 以上的已经不支持windows了
安装 pip3 install celery==3.1
### 参考文档:http://docs.celeryproject.org/en/latest/userguide/application.html
         http://www.pythondoc.com/flask-celery/first.html
### mooc视频：https://www.imooc.com/video/17957
          https://github.com/cnych/celery-learning/blob/master/imooc/conf/
## celery的使用
1.celery是什么？
    Celery是由Python开发的一个简单、灵活、可靠的分布式任务队列，它不仅支持实时处理也支持任务调度。依赖于消息队列

2.Celery的架构:
    Celery由三部分组成。消息中间件（message broker），任务执行单元（worker）和任务执行结果存储（task result store）
    每当应用程序调用celery的异步任务的时候，会向broker传递消息，而后celery的worker将会取到消息，进行程序执行
    消息中间件：
        Celery本身不提供消息服务，但是可以方便的和第三方提供的消息中间件集成。包括，RabbitMQ, Redis, MongoDB
    任务执行单元
        Worker是Celery提供的任务执行的单元，worker并发的运行在分布式的系统节点中。
    任务结果存储
        Task result store用来存储Worker执行的任务的结果，Celery支持以不同方式存储任务的结果，
        包括 Redis，memcached, MongoDB，SQLAlchemy

3.celery解决了什么问题？
        - 熬夜问题
        - 等待时间长
        通常使用它来实现异步任务（async task）和定时任务（crontab）
        celery可以帮助我们做的事：
        - 立即执行
        - 一次定时执行
        - 周期性定时执行（crontab）
4.celery和tornado的异步非阻塞的区别？
        tornado，程序和第三方做IO请求多。
        celery，程序后台或和第三发做大量的耗时操作（IO、计算）
6.异步执行任务：
        1.定义:tasks.py
            app = Celery('tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')
            @app.task
            def demo(x, y):pass
        2.运行worker
            celery -A tasks worker --loglevel=info  #celery -A celery_app  worker --loglevel=info
            在windows下运行celery -A tasks worker  -l info -P eventlet
        3.向broker中发送任务
        from tasks import demo
        1.立即执行
            result = demo.delay(10, 20)
        2.任务在未来的某一时刻执行
        task = my_background_task.apply_async(args=[10, 20], countdown=60)
        4.携带ID取结果
            from celery.result import AsyncResult
            from tasks import app
            async = AsyncResult(id="380d56b0-b869-480d-86d4-342d4e38272f", app=app)
            if async.successful():
                result = async.get()
                async.forget() # 将结果删除
7. 周期执行和定时开启任务
           CELERYBEAT_SCHEDULE = {
                'task1_scheduler': {
                    'task': 'celery_app.task1.task_add',
                    'schedule': 10.0,  每隔10秒执行x1任务
                    'args': (5, 8)  # 任务函数参数
                },
                'task2_scheduler': {
                    'task': 'celery_app.task2.multiple_add',
                    'schedule': crontab(hour=11, minute=59),  # 每天早上 9 点 50 分执行一次
                    'args': (3, 7)  # 任务函数参数
                }
            }
        1.启动一个定时任务: celery -A tasks(任务名) beat  #celery -A celery_app  beat
        2.启动worker：celery -A celery_app  worker --loglevel=info
        注意：celery4.1.0的时区有问题,设置CELERY_TIMEZONE='Asia/Shanghai后并没有执行
              使用4.2版本


8.celery的配置参数：

    CELERY_BROKER_URL = 'redis://localhost:6379/0'    Broker 地址
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' 结果存储地址
    CELERY_TIMEZONE = 'CST'       指定时区

    CELERY_TASK_RESULT_EXPIRES = 1200  任务过期时间
    CELERYD_PREFETCH_MULTIPLIER = 4
    CELERYD_CONCURRENCY = 2  设置并发的Worker数量
    CELERYD_MAX_TASKS_PER_CHILD = 100  每个worker最多执行100个任务后被销毁，防止内存泄漏

    CELERY_TASK_SERIALIZER='json'    任务执行结果序列化方式
    CELERY_ACCEPT_CONTENT=['json']  指定任务接受的内容类型(序列化)
    CELERY_RESULT_SERIALIZER='json'
    CELERY_QUEUES = (
        Queue(celeryMq, Exchange(celeryMq), routing_key=celeryMq),
    )
    CELERY_IGNORE_RESULT = True
    CELERY_SEND_EVENTS = False

    CELERYD_FORCE_EXECV = True  #防止死锁


9.在Django中集成Cerely
    pip install celery
    pip install django-celery
    需要注意版本兼容：Celery 4.0只支持Django1.8以上的版本
              Celery 3.1支持Django1.8及以下版本

    需要的库：redis  2.10.6
              Django  2.1.5
              django-celery  3.2.2
              celery  3.1.25
              django-celery3.2支持celery 3.1.15以上的版本
    运行环境：Linux
    1.在seetings同级目录下新建配置文件celeryconfig
    2.在settings.py导入配置文件：from .celeryconfig import *
    3.新建任务：在app中新建task.py
    4.在views.py中定义函数调用任务
    5.指定url

    运行：
        1.启动django
        2.启动cerely
            python manage.py help 查看操作cerely的命令
            python manage.py celery worker -l INFO  启动普通的任务
            python manage.py celery beat -l INFO    启动定时任务

    执行出错情况：
        1.在windows下运行：
            File "D:\env\venv\lib\site-packages\djcelery\managers.py", line 108, in ResultManager
            @transaction.commit_manually
            AttributeError: module 'django.db.transaction' has no attribute 'commit_manually'
            不知道是什么原因,解决不了，只好迁移到Linux下运行
        2.redis的版本
            使用redis 3.0以上版本出现以下错误：
             File "/home/jerd/env/envpy3/lib/python3.6/site-packages/redis/_compat.py", line 123, in iteritems
                return iter(x.items())
            AttributeError: 'str' object has no attribute 'items'
            解决方法：更换redis版本
        3.使用celery4.2 运行worker出错，原因未知

10.celery监控工具 flower
    pip install flower
    启动flower：
        1.指定broker并启动
            celery flower --broker=amqp://guest:guest@localhost:5672//  或
            celery flower --broker=redis://guest:guest@localhost:6379/0
        2.指定端口和访问限制：
            celery flower  --address=0.0.0.0 --port=5555 --broker = xxx(broker_url) --basic_auth=jerd:jerd

    django中启动flower
        python manage.py celery flower
        访问时设置用户名和密码：
        python manage.py celery flower  --basic_auth=jerd:jerd

## 使用supervisor管理:
    运行环境：Linux
    pip install supervisor
    supervisord -c /etc/supervisord.conf
    1.在当前目录下新建conf文件夹，用来存放配置文件
        Djangodemo$ mkdir conf

    2.把默认的配置生成到制定位置
        Djangodemo$ echo_supervisord_conf > conf/supervisord.conf

    3.修改配置文件
        1.开启管理服务页面：去掉以下代码前面的；
            ;[inet_http_server]         ; inet (TCP) server disabled by default
            ;port=127.0.0.1:9001        ; (ip_address:port specifier, *:port for all iface)
        2.开启supervisorctl：去掉serverurl前面的；
            [supervisorctl]
            serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket
            ;serverurl=http://127.0.0.1:9001 ; use an http:// url to specify an inet socket
        3.开启include：去掉；并修改files为files = *.ini
            ;[include]
            ;files = relative/directory/*.ini
        4.创建worker的配置文件
            1.在conf下新建
                Djangodemo/conf$ touch supervisor_celery_worker.ini
            2.添加如下内容：
                [program:celery-worker]
                directory=/home/jerd/PycharmProjects/Djangodemo
                command=python manage.py celery worker -l INFO
                environment=PATH='/home/jerd/env/envpy3/bin'
                stdout_logfile=/home/jerd/PycharmProjects/Djangodemo/logs/celery.worker.log
                stderr_logfile=/home/jerd/PycharmProjects/Djangodemo/logs/celery.worker.log
                autostart=true
                autorestart=true
                startsecs=10
                stopwatisecs=60
                priority=998
            3.启动：
                supervisord -c conf/supervisord.conf
                查看进程：
                    Djangodemo$ ps aux|grep supervisor
            4.查看启动的状态
                Djangodemo$ supervisorctl
            5.启动客户端：
                Djangodemo$ sudo supervisorctl -c conf/supervisord.conf

        5.创建beat的配置文件
            1.在conf下新建
                Djangodemo/conf$ touch supervisor_celery_beat.ini
            2.添加如下内容：
                [program:celery-beat]
                directory=/home/jerd/PycharmProjects/Djangodemo
                command=python manage.py celery beat -l INFO
                environment=PATH='/home/jerd/env/envpy3/bin'
                stdout_logfile=/home/jerd/PycharmProjects/Djangodemo/logs/celery.beat.log
                stderr_logfile=/home/jerd/PycharmProjects/Djangodemo/logs/celery.beat.log
                autostart=true
                autorestart=true
                startsecs=10
                stopwatisecs=60
                priority=997

打开flower管理页面的broker出错：Unable to get queues: str' object has no attribute 'name'
解决方法：重启flower


内存泄漏：长时间运行Celery有可能发生内存泄露，可以像下面这样设置
    CELERYD_MAX_TASKS_PER_CHILD = 40 # 每个worker执行了多少任务就会死掉

