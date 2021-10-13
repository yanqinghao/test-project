# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import abc
import simpy
from enum import Enum
from des.log import logger
from des import error

WorkerStatus = Enum("WorkerStatus", [(i, True if i == "Busy" else False)
                                     for i in ("Free", "Busy")])


class Base(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, env, uuid, name, **kwds):
        self.env = env
        self.uuid = uuid
        self.name = name
        for key, value in kwds.items():
            if value is not None:
                setattr(self, key, value)
        self.worker = int(getattr(self, "worker", 1))
        self.syncReceive = getattr(self, "syncReceive", True)
        self.setupTime = int(getattr(self, "setupTime", 0))
        self.processTime = int(getattr(self, "processTime", 80))
        self.recoveryTime = int(getattr(self, "recoveryTime", 0))
        # recover afterLeave/beforeEnter/afterProcessed
        self.recoveryStep = getattr(self, "recoveryStep", "afterLeave")

    @property
    def workerStatus(self):
        default = {
            f"{self.name}-{self.uuid}-worker{i}": WorkerStatus.Free
            for i in range(self.worker)
        }
        return getattr(self, "_workerStatus", default)

    @workerStatus.setter
    def workerStatus(self, value):
        self._workerStatus = value

    def checkWorkAvailable(self):
        return not all([j.value for _, j in self.workerStatus.items()])

    def updateWorkerStatus(self, worker):
        self.workerStatus.update(
            {worker: WorkerStatus(not self.workerStatus[worker].value)})

    def getAvailableWorker(self):
        for i, j in self.workerStatus.items():
            if not j.value:
                self.updateWorkerStatus(i)
                return i
        return None

    @property
    def nextNodes(self):
        return getattr(self, "_nextNodes", None)

    @nextNodes.setter
    def nextNodes(self, value):
        self._nextNodes = value

    @property
    def lastNodes(self):
        return getattr(self, "_lastNodes", None)

    @lastNodes.setter
    def lastNodes(self, value):
        self._lastNodes = value

    @property
    def inLinks(self):
        return getattr(self, "_inLinks", None)

    @inLinks.setter
    def inLinks(self, value):
        self._inLinks = value

    @property
    def outLinks(self):
        return getattr(self, "_outLinks", None)

    @outLinks.setter
    def outLinks(self, value):
        self._outLinks = value

    def getNextNode(self, nodeId):
        nodes = [node for node in self.nextNodes if node.uuid == nodeId]
        return nodes[0] if nodes else None

    def mechineFault(self):
        pass

    def getFuncList(self):
        self.recoverPos = getattr(self, "recoverPos", "afterLeave")
        if self.recoverPos == "afterLeave":
            return ["setup", "process", "send", "recover"]
        elif self.recoverPos == "beforeEnter":
            return ["recover", "setup", "process", "send"]
        elif self.recoverPos == "afterProcessed":
            return ["setup", "process", "recover", "send"]
        else:
            raise Exception("Unexpected Recover Time Position.")

    def funcExcutor(self, funcName, context, *args, **kwds):
        worker = context["worker"]
        data = context["data"]
        logger.info(
            f"Start At Time: {self.env.now},Node: {self.name}({self.uuid}),Worker: {worker} {funcName.upper()},Data: {data}."
        )
        func = getattr(self, funcName, None)
        yield from func(context, *args, **kwds)
        logger.info(
            f"Finish At Time: {self.env.now} Node: {self.name}({self.uuid}) Worker: {worker} {funcName.upper()},Data: {data}."
        )

    def setup(self, context):
        yield self.env.timeout(self.setupTime)

    def recover(self, context):
        yield self.env.timeout(self.recoveryTime)

    def process(self, context):
        yield self.env.timeout(self.processTime)

    def main(self, *args, **kwds):
        for context in self.getHandler(*args, **kwds):
            for funcName in self.getFuncList():
                yield from self.funcExcutor(funcName, context, *args, **kwds)
            self.updateWorkerStatus(context["worker"])

    def getHandler(self):
        for context in self.get():
            yield context
            worker = context["worker"]
            data = context["data"]
            logger.info(
                f"Get Order At Time: {self.env.now},Node: {self.name}({self.uuid}),WORKER: {worker},Data: {data}."
            )

    @abc.abstractmethod
    def get(self):
        yield self.lastNodes

    def send(self, context):
        sendState = {node.to_node: False
                     for node in self.outLinks} if self.outLinks else None
        if sendState:
            while not all(sendState.values()):
                for outLink in self.outLinks:
                    if self.getNextNode(outLink.to_node).checkWorkAvailable():
                        outLink.put(context["data"])
                        sendState[outLink.to_node] = True
                if not all(sendState.values()):
                    yield self.env.timeout(0.1)


class Order(Base):
    def get(self):
        for i, row in enumerate(range(10)):
            if self.checkWorkAvailable():
                worker = self.getAvailableWorker()
                context = {"data": {"index": i, "data": row}, "worker": worker}
                yield context


class Station(Base):
    def main(self, *args, **kwds):
        for context in self.getHandler(*args, **kwds):
            for funcName in self.getFuncList():
                yield from self.funcExcutor(funcName, context, *args, **kwds)
            self.updateWorkerStatus(context["worker"])

    def send(self, context):
        sendState = {node.uuid: False
                     for node in self.nextNodes} if self.nextNodes else None
        if sendState:
            while not all(sendState.values()):
                for outLink in self.outLinks:
                    if self.getNextNode(outLink.to_node).checkWorkAvailable():
                        outLink.put(context["data"])
                        sendState[outLink.to_node] = True
                if not all(sendState.values()):
                    yield self.env.timeout(0.1)


env = simpy.Environment(initial_time=0)
stations = ["A", "B", "C"]
for station in stations:
    env.process(component.main())
env.run()
