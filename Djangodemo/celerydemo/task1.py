import time
from celery.task import Task

class CourseTask(Task):
    """普通异步处理任务"""
    name = 'course-task'
    def run(self,*args,**kwargs):
        print('start course task')
        print('args={},kwargs={}'.format(args, kwargs))
        time.sleep(4)
        result = args[0] + args[1]
        return result

class CycleTask(Task):
    """周期任务"""
    name = 'cycle-task'
    def run(self,*args,**kwargs):
        print('start cycle task')
        print('args={},kwargs={}'.format(args, kwargs))
        time.sleep(4)
        result = args[0] + args[1]
        return result


class TimeTask(Task):
    """定时任务"""
    name = 'time-task'
    def run(self,*args,**kwargs):
        print('start time task')
        print('args={},kwargs={}'.format(args, kwargs))
        time.sleep(4)
        result = args[0] + args[1]
        return result

