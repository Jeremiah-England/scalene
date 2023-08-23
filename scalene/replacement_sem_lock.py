import multiprocessing
import sys
import threading
from scalene.scalene_profiler import Scalene
from typing import Any

def _recreate_replacement_sem_lock():
    return ReplacementSemLock()

class ReplacementSemLock(multiprocessing.synchronize.Lock):
    def __enter__(self) -> bool:
        timeout = sys.getswitchinterval()
        tident = threading.get_ident()
        while True:
            Scalene.set_thread_sleeping(tident)
            acquired = self._semlock.acquire(timeout=timeout)  # type: ignore
            Scalene.reset_thread_sleeping(tident)
            if acquired:
                return True
    def __exit__(self, *args: Any) -> None:
        super().__exit__(*args)
    def __reduce__(self):
        return (_recreate_replacement_sem_lock, ())
