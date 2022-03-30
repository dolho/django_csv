import time
from typing import Callable
import logging

class CSVMonitorThread():

    def __init__(self, app, interval=0):
        self.__app = app
        self.__state = app.events.State()
        self.interval = interval
        self.__uuid_function_success = dict()
        self.__uuid_function_processing = dict()

    def add_uuid_function_pair_success(self, uuid: str, function: Callable) -> None:
        """
        :param uuid: str
        :param function: callable
        :return: None
        Sets function to call, when task with given uuid successfully finished
        """
        self.__uuid_function_success[uuid] = function

    def add_uuid_function_pair_processing(self, uuid: str, function: Callable):
        """
        :param uuid: str
        :param function: callable
        :return: None
        Sets function to call, when task with given uuid started
        """
        self.__uuid_function_processing[uuid] = function

    def successful_task(self, event):
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
        try:
            self.__uuid_function_processing[task.uuid]()
            del self.__uuid_function_processing[task.uuid]
        except KeyError:
            pass
        # print('TASK STARTED: %s[%s] %s' % (
        #     task.name, task.uuid, task.info(),))

    def catchall(self, event):

        if event['type'] != 'worker-heartbeat':
            self.__state.event(event)

    def run(self):
        self.__app.control.enable_events()
        while True:
            try:
                with self.__app.connection() as connection:
                    print("Monitor is working")
                    recv = self.__app.events.Receiver(connection, handlers={
                        'task-succeeded': self.successful_task,
                        'task-started': self.task_started,
                        '*': self.catchall,
                    })
                    print("Monitor worked")
                    recv.capture(limit=None, timeout=None, wakeup=True)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                logging.warning(e)
                pass
            # time.sleep(self.interval)


