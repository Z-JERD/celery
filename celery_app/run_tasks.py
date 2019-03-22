import time

from celery.result import AsyncResult

from celery_app import task1, task2, app
from celery_app.tasks import celeryapp, my_background_task


class Celerydemo(object):

    def get_result(self,taskid,use_config=True):
        """去存储中取结果 """
        if use_config:
            async = AsyncResult(id=taskid, app=app)
        else:
            async = AsyncResult(id=taskid, app=celeryapp)
        if async.successful():
            result = async.get()
            print('result is ',result)
            return result
        #返回详细的信息
        """
           if async.state == 'PENDING':
            # job did not start yet
            response = {
                'state': async.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        
        elif async.state != 'FAILURE':
            response = {
                'state': async.state,
                'current': async.info.get('current', 0),
                'total': async.info.get('total', 1),
                'status': async.info.get('status', '')
            }
            if async.successful():
                response['result'] = async.get()
        
        else:
            # something went wrong in the background job
            response = {
                'state': async.state,
                'current': 1,
                'total': 1,
                'status': str(async.info),  # this is the exception raised
            }
        """


    def immediate_execution(self):
        """普通异步任务，操作tasks中的任务
        向broker中发送任务 delay() 方法是强大的 apply_async() 调用的快捷方式 """
        task = my_background_task.delay(10, 20)
        print('task id is ',task.id)
        while True:
            task_result = self.get_result(task.id)
            if task_result:
                print('Task Delivery Completed time is:',time.time(),'task_result is ',task_result)
                break

    def  timing_task(self):
        """普通异步任务，操作tasks中的任务
        自定义时间想broker中发送任务 apply_async()"""
        task = my_background_task.apply_async(args=[30, 20], countdown=60)
        print('task id is ', task.id)
        while True:
            task_result = self.get_result(task.id)
            if task_result:
                print('Task Delivery Completed time is:', time.time(),'task_result is ',task_result)
                break

    def config_task(self):
        """通过cerely的配置文件的操作celery_app中的任务task1,task2"""
        task1_obj = task1.task_add.delay(10, 20)
        task2_obj = task2.multiple_add.delay(30, 50)

        # countdown：指定多少秒后执行任务
        # task1.task_add.apply_async(args=(2, 23), countdown=5)  # 5 秒后执行任务
        # task1.task_add.apply_async(args=[6, 7], expires=10)  # 10 秒后过期
        print('task1 id is ', task1_obj.id,'task2 id is ',task2_obj.id)
        while True:
            task1_result = self.get_result(task1_obj.id)
            task2_result = self.get_result(task2_obj.id)
            if task1_result and task2_result:
                print('Task Delivery Completed time is:', time.time())
                print( 'task2_result is ', task2_result)
                break


if __name__ == '__main__':
    demo_object = Celerydemo()
    print('start the task now time is：',time.time())
    # demo_object.immediate_execution()
    # # demo_object.timing_task()
    demo_object.config_task()
    print('end the task now time is:',time.time())

