import time

class CSVMonitorThread():

    def __init__(self, app, interval=1):
        self.__app = app
        self.__state = app.events.State()
        self.interval = interval
        self.__uuid_function_success = dict()
        self.__uuid_function_processing = dict()

    def add_uuid_function_pair_success(self, uuid, function):
        self.__uuid_function_success[uuid] = function

    def add_uuid_function_pair_processing(self, uuid, function):
        self.__uuid_function_processing[uuid] = function

    def successful_task(self, event):
        print("Successfulltask worked")
        self.__state.event(event)
        task = self.__state.tasks.get(event['uuid'])
        try:
            print("Before func")
            self.__uuid_function_success[task.uuid]()
            print("After Func")
            print("Data send")
            del self.__uuid_function_success[task.uuid]
        except KeyError:
            print("KeyError")
            pass
        # print('TASK SUCCESS: %s[%s] %s' % (
        #     task.name, task.uuid, task.info(),))

    def task_started(self, event):
        self.__state.event(event)
        task = self.__state.tasks.get(event['uuid'])
        # try:
        #     self.__uuid_function_processing[task.uuid]()
        #     del self.__uuid_function_processing[task.uuid]
        # except KeyError:
        #     pass
        # print('TASK STARTED: %s[%s] %s' % (
        #     task.name, task.uuid, task.info(),))

    def catchall(self, event):

        if event['type'] != 'worker-heartbeat':
            self.__state.event(event)
        # logic here

    def run(self):
        print("Eventcatcher thread started")
        self.__app.control.enable_events()
        while True:
            try:
                with self.__app.connection() as connection:
                    recv = self.__app.events.Receiver(connection, handlers={
                        'task-succeeded': self.successful_task,
                        'task-started': self.task_started,
                        '*': self.catchall,
                    })
                    recv.capture(limit=None, timeout=None, wakeup=True)

            except (KeyboardInterrupt, SystemExit):
                raise

            except Exception:
                # unable to capture
                pass

            time.sleep(self.interval)


# def my_monitor(app):
#     state = app.events.State()
#
#     def announce_failed_tasks(event):
#         state.event(event)
#         # task name is sent only with -received event, and state
#         # will keep track of this for us.
#         task = state.tasks.get(event['uuid'])
#
#         print('TASK FAILED: %s[%s] %s' % (
#             task.name, task.uuid, task.info(),))


