from django.shortcuts import render
from django.http import JsonResponse

from .task1 import CourseTask

def celerytest(request):
    print('start do request')
    CourseTask.delay(2,3)
    #手动指定队列
    #CourseTask.apply_async(args=(2,3),queue = 'work_queue')
    print('end do request')
    return JsonResponse({'result':'ok'})
