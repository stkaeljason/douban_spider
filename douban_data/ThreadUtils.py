# -*- coding:utf-8 -*-
#
# power by Act.yu
import Queue
import threading
import time


"""
    创建线程池
    """


class ThreadPoolManager(object):
    def __init__(self, runConfig):
        self.workQueue = Queue.Queue()
        self.threads = []
        self.runConfig = runConfig
        self.__initQueue()
        self.__initThreadPool(runConfig.getThreadCount())

    def __initQueue(self):
        for line in self.runConfig.getTask():
            self.addWork(self.runConfig.run, str(line).replace("\n", ""))


    def __initThreadPool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.workQueue))

    def addWork(self, func, *args):
        self.workQueue.put((func, list(args)))

    def checkQueue(self):
        return self.workQueue.qsize()

    def waitingForComplete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


"""
    线程实列
    """
class Work(threading.Thread):
    def __init__(self, workQueue):
        threading.Thread.__init__(self)
        self.workQueue = workQueue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.workQueue.get(block=False)
                do(args)
                self.workQueue.task_done()
            except Exception,e:
                print str(e)
                return
"""
    线程配置类
    """
class RunConfig(object):
    def __init__(self):
        self.threadCount = 20
        self.tasks = []

    def getThreadCount(self):
        return self.threadCount

    def setThreadCount(self,num):
        self.threadCount = num

    def setTask(self,tasks):
        self.tasks = tasks
        tasks = []
        del tasks

    def clear(self):
        self.tasks = []

    def getTask (self):
        return self.tasks;

    def run (self, args):
        print args
        pass