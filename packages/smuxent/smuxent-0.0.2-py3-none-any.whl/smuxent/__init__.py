import platform
import importlib
import sys

__doc__ = """ 
Smuxent - A lightweight native threading utility for Python.
Written by me starting from 05/04/2025.

This library provides simple, low-level access to native C++ threads from Python.
It's designed for lightweight concurrency and fire-and-forget execution models,
with minimal amount of tools for managing.

Current Features:
- Run Python functions in detached threads
- Track threads and pools by ID
- Kill individual threads or all running threads as well a pools
- Check if a thread is still alive
- Thread pool implementation
- Submit tasks to said thread pool
- A demo function (hello_thread) to test the library

Below will be the useable functions and a short description of each
# === v0.0.1 - Basic Threading ===

def basic_thread(func: Callable, *args: Any) -> int: ...
def hello_thread(loop_count: int = 1) -> int: ...

def is_alive(id: int) -> bool: ...
def kill_thread(id: int) -> None: ...
def kill_all_threads() -> None: ...
def get_all_thread_ids() -> List[int]: ...

# === v0.0.2 - Thread Pools ===

def thread_pool(size: int) -> str: ...
def submit(pool_id: str, func: Callable, *args: Any) -> bool: ...
def get_pool_thread_ids(pool_id: str) -> List[int]: ...
def kill_pool(pool_id: str) -> None: ...

# === Deprecated / Legacy Functions ===

def __basic_threadOld(func: Callable, *args: Any) -> None:
    "[Deprecated] Use basic_thread instead. This version does not return a thread ID."

def __hello_threadOld(loop_count: int = 1) -> None:
    "[Deprecated] Use hello_thread instead. This version does not support thread tracking."





Planned Additions (TODO):
- Thread pool implementation ##DONE AS OF v0.0.2##
- Future/promise support for result retrieval
- Message queues or inter-thread channels
- Shared memory
- Event-driven threading pattern

This project was built for fun, learning, and utility. If you're using this, thanks!
Feedback and suggestions are welcome though not sure where that'd be.


-- Patryk Wrzesniewski
""" 

def _detect_thread_module_name():
    system = platform.system()
    arch = platform.architecture()[0]
    pyver = f"{sys.version_info.major}{sys.version_info.minor}"

    if system != "Windows":
        raise ImportError("Smuxent only supports Windows for now.")

    suffix = "64" if "64" in arch else "32"
    return f"py{pyver}ThreadWin{suffix}"

# Import the correct native module
_threadmod = importlib.import_module(f"smuxent.{_detect_thread_module_name()}")

#v0.0.1 Basic threads
basic_thread = _threadmod.basic_thread
hello_thread = _threadmod.hello_thread
is_alive = _threadmod.is_alive
kill_thread = _threadmod.kill_thread
kill_all_threads = _threadmod.kill_all_threads
get_all_thread_ids = _threadmod.get_all_thread_ids
#v0.0.2 Thread Pool Functions
thread_pool = _threadmod.thread_pool
submit = _threadmod.submit
get_pool_thread_ids = _threadmod.get_pool_thread_ids
kill_pool = _threadmod.kill_pool


# For debugging
def get_loaded_native_module():
    return _threadmod
