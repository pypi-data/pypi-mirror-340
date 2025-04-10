from time import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, Collection, Self
from threading import Thread, Event
from functools import cached_property
import asyncio
from StructResult import result
from DLMSCommunicationProfile.osi import OSI
from DLMS_SPODES.config_parser import get_values
from StructResult.result import T
from .logger import LogLevel as logL
from .client import Client
from . import task

_setting = {
    "depth": 10
}
if toml_val := get_values("DLMSClient", "session", "results"):
    _setting.update(toml_val)


@dataclass(eq=False)
class Session:
    c: Client
    tsk: task.Base
    complete: bool = False
    res: result.Result = field(init=False)

    async def run(self):
        self.c.lock.acquire(timeout=10)  # 10 second, todo: keep parameter anywhere
        self.res = await self.tsk.run(self.c)
        self.c.lock.release()
        self.complete = True
        if results is not None:
            keep_result(self)
        # media close
        if not self.c.lock.locked():
            self.c.lock.acquire(timeout=1)
            if self.c.media.is_open():
                self.c.log(logL.DEB, F"close communication channel: {self.c.media}")
                await self.c.media.close()
            else:
                self.c.log(logL.WARN, F"communication channel: {self.c.media} already closed")
            self.c.lock.release()
            self.c.level = OSI.NONE
        else:
            """opened media use in other session"""

    def __hash__(self):
        return hash(self.c)


@dataclass(frozen=True)
class DistributedTask:
    """The task for distributed execution on several customers."""
    tsk: task.Base
    clients: Collection[Client]

    def __str__(self) -> str:
        return f"{self.tsk.msg}[{len(self.clients)}])"


class TransactionServer:
    __t: Thread
    __non_complete: set[Session]
    __complete: set[Session]
    name: str

    def __init__(self,
                 *dis_tasks: DistributedTask,
                 name: str = None,
                 abort_timeout: int = 1):
        self.__non_complete = set()
        client_tasks: dict[Client, list[task.Base]] = defaultdict(list)
        for dis_tsk in dis_tasks:
            for client in dis_tsk.clients:
                client_tasks[client].append(dis_tsk.tsk)
        for client, tasks in client_tasks.items():
            if len(tasks) == 1:
                self.__non_complete.add(Session(client, tsk=tasks[0]))
            else:
                self.__non_complete.add(Session(client, tsk=task.Sequence(*tasks)))
        self.__complete = set()
        self.name = name
        """common operation name"""
        # self._tg = None
        self.__stop = Event()
        self.__t = Thread(
            target=self.__start_coro,
            args=(abort_timeout,))

    @cached_property
    def all(self) -> set[Session]:
        return self.__non_complete | self.__complete

    def __getitem__(self, item) -> Session:
        return tuple(self.all)[item]

    @cached_property
    def clients(self) -> set[Client]:
        return {sess.c for sess in self.all}

    @property
    def ok_results(self) -> set[Session]:
        """without errors exchange clients"""
        return {sess for sess in self.__complete if sess.res.err is None}

    @cached_property
    def nok_results(self) -> set[Session]:
        """ With errors exchange clients """
        return self.all.difference(self.ok_results)

    def pop(self) -> set[Session]:
        """get and move complete session"""
        to_move = {sres for sres in self.__non_complete if sres.complete}
        self.__complete |= to_move
        self.__non_complete -= to_move
        return to_move

    def is_complete(self) -> bool:
        """check all complete sessions. call <pop> before"""
        return len(self.__non_complete) == 0

    def start(self):
        self.__t.start()

    def abort(self):
        self.__stop.set()

    def __start_coro(self, abort_timeout):
        asyncio.run(self.coro_loop(abort_timeout))

    async def coro_loop(self, abort_timeout: int):
        async def check_stop(tg: asyncio.TaskGroup):
            while True:
                await asyncio.sleep(abort_timeout)
                if self.is_complete():
                    break
                elif self.__stop.is_set():
                    tg._abort()
                    break

        async with asyncio.TaskGroup() as tg:
            for sess in self.__non_complete:
                tg.create_task(sess.run())
            tg.create_task(
                coro=check_stop(tg),
                name="wait abort task")


if _setting.get("depth") > 0:
    from collections import deque


    @dataclass(eq=False)
    class SessionResult:
        msg: str
        tsk: task.Base
        value: Optional[T]
        time: float
        err: Optional[ExceptionGroup]


    results: Optional[dict[Client, deque[SessionResult]]] = dict()
    """exchange results archive"""


    def keep_result(sess: Session):
        global results
        if (entries := results.get(sess.c)) is None:
            results[sess.c] = (entries := deque())
        if _setting["depth"] <= len(entries):
            entries.popleft()
        entries.append(SessionResult(
            msg=sess.res.msg,
            tsk=sess.tsk,
            value=sess.res.value,
            time=time(),
            err=sess.res.err
        ))
else:
    results = None
