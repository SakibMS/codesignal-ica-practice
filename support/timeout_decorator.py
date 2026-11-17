"""
Local stand-in for the `timeout-decorator` package that CodeSignal has
installed. Tests use it as `@timeout(seconds)`.

- macOS / Linux: interrupts a slow test with SIGALRM (like the real package).
- Windows: runs the test in a worker thread and fails it if it overruns.
"""
import functools
import signal
import threading


class TimeoutError(AssertionError):
    """Raised when a test runs longer than its time limit."""


def timeout(seconds):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = f"Timed out after {seconds} seconds"
            use_signals = (
                hasattr(signal, "setitimer")
                and threading.current_thread() is threading.main_thread()
            )

            if use_signals:
                def handler(signum, frame):
                    raise TimeoutError(message)

                previous = signal.signal(signal.SIGALRM, handler)
                signal.setitimer(signal.ITIMER_REAL, seconds)
                try:
                    return func(*args, **kwargs)
                finally:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, previous)

            outcome = {}

            def target():
                try:
                    outcome["value"] = func(*args, **kwargs)
                except BaseException as error:  # re-raised in the main thread
                    outcome["error"] = error

            worker = threading.Thread(target=target, daemon=True)
            worker.start()
            worker.join(seconds)
            if worker.is_alive():
                raise TimeoutError(message)
            if "error" in outcome:
                raise outcome["error"]
            return outcome.get("value")

        return wrapper

    return decorate
