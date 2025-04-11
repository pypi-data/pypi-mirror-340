from time import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, Collection, Iterator
from threading import Thread
import threading
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
    "persistent_depth": 1000,
    "volatile_depth": 100
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
            await results.add(self)
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
    __t: threading.Thread
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
        self.__stop = threading.Event()
        self.__t = threading.Thread(
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


if _setting.get("persistent_depth") > 0:
    from collections import deque


    @dataclass(eq=False)
    class SessionResult:
        c: Client
        msg: str
        tsk: task.Base
        value: Optional[T]
        time: float
        err: Optional[ExceptionGroup]

        def __hash__(self):
            return hash(self.c)


    class UniversalLock:
        def __init__(self):
            self._thread_lock = threading.Lock()
            self._async_lock = asyncio.Lock()

        def __enter__(self):
            self._thread_lock.acquire()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._thread_lock.release()

        async def __aenter__(self):
            await self._async_lock.acquire()
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            self._async_lock.release()


    class DualResultStorage:
        def __init__(self, persistent_depth: int, volatile_depth: int):
            self._persistent = deque(maxlen=persistent_depth)
            self._volatile = deque(maxlen=volatile_depth)
            self._lock = UniversalLock()

        async def add(self, sess: Session):
            s_res = SessionResult(
                c=sess.c,
                msg=sess.res.msg,
                tsk=sess.tsk,
                value=sess.res.value,
                time=time(),
                err=sess.res.err
            )
            async with self._lock:
                self._persistent.append(s_res)
                self._volatile.append(s_res)

        def get_persistent(self) -> list[SessionResult]:
            with self._lock:
                return list(self._persistent)

        def get_volatile(self) -> set[SessionResult]:
            with self._lock:
                old = self._volatile
                self._volatile = deque(maxlen=self._volatile.maxlen)
            return set(old)

        def client2sres(self, c: Client) -> list[SessionResult]:
            with self._lock:
                tmp = list(self._persistent)
            return [res for res in tmp if res.c == c]


    results: DualResultStorage = DualResultStorage(
        persistent_depth=_setting["persistent_depth"],
        volatile_depth=_setting["volatile_depth"]
    )
    """exchange results archive"""

else:
    results: None = None
