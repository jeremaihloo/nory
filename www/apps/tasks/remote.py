from aio_pika import connect_robust
from aio_pika.patterns import Master


class RemoteTaskRunner(object):
    def __init__(self, rabbitmq_url, tasks):
        self.rabbitmq_url = rabbitmq_url
        self.tasks = tasks

    async def run_task(self, cmd_line):
        pass

    async def status_task(self, task_id):
        pass

    async def all_remote_host(self):
        pass

    async def start(self):
        self.connection = await connect_robust(self.rabbitmq_url)

        # Creating channel
        self.channel = await self.connection.channel()

        self.master = Master(self.channel)

        # Creates tasks by proxy object
        for task_id in range(1000):
            await self.master.proxy.my_task_name(task_id=task_id)

    async def stop(self):
        await self.connection.close()


class RemoteTaskExecutor(object):
    def __init__(self, rabbitmq_url, tasks):
        self.rabbitmq_url = rabbitmq_url
        self.tasks = tasks

    async def run_task(self, cmd_line):
        pass

    async def status_task(self, task_id):
        pass

    async def start(self):
        self.connection = await connect_robust("amqp://guest:guest@127.0.0.1/")

        # Creating channel
        self.channel = await self.connection.channel()

        master = Master(self.channel)
        for task in self.tasks:
            await master.create_worker(getattr(task, '__app_fn_name__'), task, auto_delete=True)

    async def stop(self):
        self.connection.close()


class RemoteTaskHost(object):

    def __init__(self, rabbitmq_url, tasks):
        self.rabbitmq_url = rabbitmq_url
        self.tasks = tasks

        self.runner = RemoteTaskRunner(rabbitmq_url, tasks)
        self.executor = RemoteTaskExecutor(rabbitmq_url, tasks)

    async def start(self):
        self.runner.start()
        self.executor.start()

    async def stop(self):
        self.runner.stop()
        self.executor.stop()
