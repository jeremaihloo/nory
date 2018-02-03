import logging
import uuid

from concurrent.futures import ThreadPoolExecutor
from time import sleep

TASK_STATUS_WAITING = 'TASK_STATUS_WAITING'
TASK_STATUS_RUNNING = 'TASK_STATUS_RUNNING'
TASK_STATUS_FINISHD = 'TASK_STATUS_FINISHD'


class TaskInfo(object):

    def __init__(self, name, status, message):
        self.name = name
        self.status = status
        self.message = message
        self.id = uuid.uuid4()

    def __str__(self):
        return 'id : {} name : {} status : {} message : {}'.format(self.id, self.name, self.status, self.message)


class Task(object):
    def __init__(self, func):
        self.func = func
        self.info = TaskInfo(name=getattr(func, '__name__'),
                             status=TASK_STATUS_WAITING,
                             message='I am waiting !')
        self.executor = ThreadPoolExecutor(max_workers=1)

        def demo():
            return 'hello world !'

        self.feature = self.executor.submit(demo)

    async def start(self, *args, **kwargs):
        try:
            self.feature = self.executor.submit(self.func, *args, **kwargs)
            self.info.status = TASK_STATUS_RUNNING
            self.info.message = 'I am running !'
            return True, self.info
        except Exception as e:
            logging.exception(e)
            self.info.status = TASK_STATUS_FINISHD
            self.info.message = str(e)
            return False, self.info

    def shutdown(self, wait=True):
        self.executor.shutdown(wait=wait)

    def cancel(self):
        self.feature.cancel()

    def status(self):
        try:
            data = self.feature.result()
            self.info.status = TASK_STATUS_FINISHD
            self.info.message = data
            return True, self.info
        except Exception as e:
            logging.exception(e)
            self.info.status = TASK_STATUS_FINISHD
            self.info.message = str(e)
            return False, self.info


class TaskManager(object):
    def __init__(self, task_funcs):
        self.tasks = {}
        for item in task_funcs:
            self.tasks[getattr(item, '__name__')] = Task(item)

    def stop(self, name, wait=True):
        task = self.tasks.get(name, None)
        if task is not None:
            return task.shutdown(wait)
        return False, 'task {} not found'.format(name)

    def start(self, task_name, *args, **kwargs):
        task = self.tasks.get(task_name, None)
        if task is not None:
            return task.start(*args, **kwargs)
        return False, 'Task {} Not Found'.format(task_name)

    def shutdown(self, wait=True):
        for item in self.tasks:
            item.shutdown(wait=wait)

    def status_all(self):
        for item in self.tasks:
            yield item.status()

    def status(self, name):
        task = self.tasks.get(name, None)
        if task is not None:
            return task.status()
        return False, 'Task {} Not Found'.format(task_name)


if __name__ == '__main__':
    def hello_world_from_china():
        sleep(30)
        return 'hello world from china !'


    manager = TaskManager([hello_world_from_china])
    print(manager.status('hello_world_from_china'))
    print(manager.start('hello_world_from_china'))
    print(manager.status('hello_world_from_china'))
    sleep(40)
    print(manager.status('hello_world_from_china'))
