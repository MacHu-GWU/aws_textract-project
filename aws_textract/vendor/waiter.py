# -*- coding: utf-8 -*-

import typing as T
import sys
import time
import itertools

__version__ = "0.1.1"

class Waiter:
    """
    Simple retry / polling with progressing status. Usage, it is common to check
    if a long-running job is done every X seconds and timeout in Y seconds.
    This class allow you to customize the polling interval and timeout,.

    Example:

    .. code-block:: python

        print("before waiter")

        for attempt, elapse in Waiter(
            delays=1,
            timeout=10,
            verbose=True,
        ):
            # check if should jump out of the polling loop
            if elapse >= 5:
                print("")
                break

        print("after waiter")
    """
    def __init__(
        self,
        delays: T.Union[int, float],
        timeout: T.Union[int, float],
        indent: int = 0,
        verbose: bool = True,
    ):
        self._delays = delays
        self.delays = itertools.repeat(delays)
        self.timeout = timeout
        self.tab = " " * indent
        self.verbose = verbose

    def __iter__(self):
        if self.verbose: # pragma: no cover
            sys.stdout.write(
                f"start waiter, polling every {self._delays} seconds, "
                f"timeout in {self.timeout} seconds.\n"
            )
            sys.stdout.flush()
            sys.stdout.write(
                f"\r{self.tab}on 0 th attempt, "
                f"elapsed 0 seconds, "
                f"remain {self.timeout} seconds ..."
            )
            sys.stdout.flush()
        start = time.time()
        end = start + self.timeout
        for attempt, delay in enumerate(self.delays, 1):
            now = time.time()
            remaining = end - now
            if remaining < 0:
                raise TimeoutError(f"timed out in {self.timeout} seconds!")
            else:
                time.sleep(min(delay, remaining))
                elapsed = int(now - start + delay)
                if self.verbose: # pragma: no cover
                    sys.stdout.write(
                        f"\r{self.tab}on {attempt} th attempt, "
                        f"elapsed {elapsed} seconds, "
                        f"remain {self.timeout - elapsed} seconds ..."
                    )
                    sys.stdout.flush()
                yield attempt, int(elapsed)
